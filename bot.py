# -*- coding: utf-8 -*-
import telebot

token ="371478199:AAFnBBn2d79tIT0ut6Pj4ZKYHHh8PILbij8"
bot = telebot.TeleBot(token)
#https://api.vk.com/method/wall.get?domain=kaspercareer&count=10&filter=owner

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
    
# # -*- coding: utf-8 -*-

# import time
# import eventlet
# import requests
# import logging
# import telebot
# from time import sleep

#  # Каждый раз получаем по 10 последних записей со стены
# URL_VK = 'https://api.vk.com/method/wall.get?domain=c.music&count=10&filter=owner'
# FILENAME_VK = 'last_known_id.txt'
# BASE_POST_URL = 'https://vk.com/wall-39270586_'

# BOT_TOKEN = '371478199:AAFnBBn2d79tIT0ut6Pj4ZKYHHh8PILbij8'
# CHANNEL_NAME = '@канал'

# bot = telebot.TeleBot(BOT_TOKEN)

