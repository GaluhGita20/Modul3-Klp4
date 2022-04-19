import os
import telebot
from dotenv import load_dotenv
import broadcast 

load_dotenv()
token = str(os.environ.get("token"))
bot = telebot.TeleBot(token)

# text_save ="ya test sih"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Ini adalah bot praktikum IMS')

@bot.message_handler(commands=["tes"])
def send_message(msg):
    
    list = broadcast.groupLists()
    print(text_save)
    broadcast.sendBroadcast(list=list, msg=text_save)
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global text_save 
    text_save = message.text
    
print('Bot Running')
bot.polling()