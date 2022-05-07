# -*- coding: utf-8 -*-
"""
Created on Fri May  6 23:35:01 2022

@author: Adrià Oriol
"""

import telebot
import math
from telebot import *

bot = telebot.TeleBot("TELEGRAM-BOT-TOKEN")

textConsultList = 'Consultar llista de la compra'
textAddToList = 'Afegir a la llista de la compra'
textRemoveFromList = 'Eliminar de la llista de la compra'
textEndOperation = "Fi"

llistaCompra = []
listCommands = []
userAdding = False
userRemoving = False

@bot.poll_handler(func=lambda update: True)
def member_status(update):
    if(update.chat_member.new_chat_member.status == "member"):
        bot.send_message(update.chat.id, "Tests")
        #bot.send_list_2(member.chat.id)

@bot.message_handler(regexp = textConsultList)
def send_items(message):
    textBot = ""
    
    delete_user_message(message)
    for i in range(len(llistaCompra)):
        textBot = textBot + "- " + llistaCompra[i] + "\n"
        
    bot.send_message(message.chat.id, textBot)
    
@bot.message_handler(regexp = textAddToList)
def add_items(message):
    global userAdding 
    userAdding = True
    
    delete_user_message(message)
    adding_items(message)
   
@bot.message_handler(regexp = textRemoveFromList)
def remove_items(message):
    global userRemoving
    userRemoving = True
        
    delete_user_message(message)
    removing_items(message)
        
    
    
@bot.message_handler(regexp = textEndOperation)
def finalitzar(message):
    global userAdding, userRemoving
    userAdding = False
    userRemoving = False
    
    start_request(message)

@bot.message_handler(func = lambda message: not userAdding and not userRemoving)
def start_request(message):
    delete_user_message(message)
    bot.send_message(message.chat.id, "Seleccioni una opció", reply_markup=markup_1)
    
@bot.message_handler(func = lambda message: userAdding)
def add_one_item(message):
    item = str(message.text)
    delete_user_message(message)
    llistaCompra.append(item)
    bot.send_message(message.chat.id, "S'ha afegit " + item + " a la llista.")
    
@bot.message_handler(func = lambda message: userRemoving and message.text.isdigit())
def remove_one_item(message):
    item = int(message.text)
    
    delete_user_message(message)
    if(item - 1 < 0 or item - 1 > len(llistaCompra) - 1):
        bot.send_message(message.chat.id, "No existeix la opció seleccionada")
    else:
        llistaCompra.pop(item - 1)
        bot.send_message(message.chat.id, "S'ha eliminat " + str(item) + " de la llista.") 
        removing_items(message)
    

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.reply_to(message, "Howdy, how are you doing?")
    bot.send_message(message.chat.id, "Test", reply_markup=markup)
    
@bot.message_handler(commands=listCommands)
def removeItem(message):
	#bot.reply_to(message, "Howdy, how are you doing?")
    remove_one_item(message)
    
    







def echo_all(message):
	bot.reply_to(message, message.text)
    
def send_list_1(message):
    bot.send_message(message.chat.id, "", reply_markup=markup_1)

def send_list_2(message):
    bot.send_message(message.chat.id, "", reply_markup=markup_2)

def adding_items(message):
    bot.send_message(message.chat.id, "Escrigui que vol afegir", reply_markup=markup_end)

def removing_items(message):
    textBot = ""     
    listCommands.clear()
    for i in range(len(llistaCompra)):
        textBot = textBot + "/" + str(i+1) + " - " + llistaCompra[i] + "\n"
        listCommands.append(i)
    bot.send_message(message.chat.id, "Seleccioni que vol eliminar:\n" + textBot, reply_markup=markup_end)  
    
def delete_user_message(m):
    bot.delete_message(m.chat.id, m.id)

markup = types.ReplyKeyboardMarkup()
markup_1 = types.ReplyKeyboardMarkup()
markup_2 = types.ReplyKeyboardMarkup()
markup_end = types.ReplyKeyboardMarkup()
markup_delete = types.ReplyKeyboardMarkup()

btn_1_1 = types.KeyboardButton(textConsultList)
btn_1_2 = types.KeyboardButton(textAddToList)
btn_1_3 = types.KeyboardButton(textRemoveFromList)

#btn_1_2 = types.KeyboardButton('[...]')
markup_1.row(btn_1_1)
markup_1.row(btn_1_2)
markup_1.row(btn_1_3)

btn_2_1 = types.KeyboardButton('Consultar Llista')
btn_2_2 = types.KeyboardButton("Afegir a la Llista")
btn_2_3 = types.KeyboardButton("Eliminar de la Llista")
markup_2.row(btn_2_1)
markup_2.row(btn_2_2, btn_2_3)

markup_end.row(types.KeyboardButton(textEndOperation))

itembtna = types.KeyboardButton('Llistes de la Compra')
itembtnv = types.KeyboardButton('Afegir / Eliminar a la Llista')
itembtnc = types.KeyboardButton('Altres Opcions')
itembtnd = types.KeyboardButton('d')
itembtne = types.KeyboardButton('e')
markup.row(itembtna, itembtnv)
markup.row(itembtnc)




bot.infinity_polling(allowed_updates = util.update_types)