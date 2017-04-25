import sys
import time
import random
import datetime
import RPi.GPIO as GPIO
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
LIST_OF_ADMINS = [**,**] #chat id of user 


def handle(msg):
	chat_id = msg['chat']['id']
	command = msg['text']
        print 'Got command %s' %command
        user_id = chat_id
        if user_id not in LIST_OF_ADMINS:
                print("Unauthorized access denied for {}.".format(chat_id))
                return
        else:
                print("Access approved for {}.".format(chat_id))
                if command == '/start':
                        markup = ReplyKeyboardMarkup(keyboard=[['/parth','/time','/roll'],['/on','/blink']],one_time_keyboard=True)
                        bot.sendMessage(chat_id,chat_id,reply_markup=markup)
                if command == '/roll':
                        markup = ReplyKeyboardRemove()
                        bot.sendMessage(chat_id,random.randint(1,6))
	       
                elif command == '/time':
                        bot.sendMessage(chat_id,str(datetime.datetime.now()))
                elif command == '/parth':
                        bot.sendMessage(chat_id,str('Yes Your owner!!!'))
                elif command == '/on':
                        markup = ReplyKeyboardMarkup(keyboard=[['/off'],['/blink']])
                        bot.sendMessage(chat_id,str('LED is on'),reply_markup=markup)
                        GPIO.output(18,GPIO.HIGH)
                        time.sleep(1)
                elif command == '/off':
                        markup = ReplyKeyboardMarkup(keyboard=[['/on'],['/blink']])
                        bot.sendMessage(chat_id,str('LED is off'),reply_markup=markup)
                        GPIO.output(18,GPIO.LOW)
                        time.sleep(1)
                elif command == '/blink':
                        markup = ReplyKeyboardMarkup(keyboard=[['/on'],['/off']])
                        bot.sendMessage(chat_id,str('LED is blinking'),reply_markup=markup)
                        for x in range(0,5):
                                GPIO.output(18,GPIO.HIGH)
                                time.sleep(0.5)
                                GPIO.output(18,GPIO.LOW)
                                time.sleep(0.5)

bot = telepot.Bot('**') #Insert your telegram bot API key
bot.message_loop(handle)
print 'I am listening...'

while 1:
	time.sleep(10)
