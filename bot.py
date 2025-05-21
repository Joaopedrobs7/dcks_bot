import telebot
from telebot import types
from scraper import fetch_img
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv('API_KEY')
bot = telebot.TeleBot(api_key)
chat_id = '-1002332064031'


#GET IMAGE
asyncio.run(fetch_img())
card = open('card.png','rb')
bot.send_photo(chat_id=chat_id,photo=card)

#pega resto das msgs
# @bot.message_handler()
# def getall(msg: types.Message):
#     print(f"Msg: {msg.text} Chat ID: {msg.chat.id} thread_id:{msg.message_thread_id}")
#     if msg.text == '/card':
#         asyncio.run(fetch_img())
#         with open ('card.png', 'rb') as card:
#             bot.send_photo(msg.chat.id,card)


# bot.infinity_polling()