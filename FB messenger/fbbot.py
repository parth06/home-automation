from flask import Flask, request
import requests, json
import os
import re
from sys import argv
from wit import Wit
import time
import RPi.GPIO as GPIO       ## Import GPIO library

app = Flask(__name__)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      ## Use board pin numbering

ACCESS_TOKEN = "***" #copy access token from fb page
VERIFY_TOKEN = "hello_token" #same as on fb page
WIT_TOKEN = '***' #copy wit token from wit account

def reply(user_id, msg):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)
    print(urls)




@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message)
    client.run_actions(session_id=sender, message=message)
    

    return "ok",200

def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    """
    Sender function
    """
    # We use the fb_id as equal to session_id
    sender = request['session_id']
    message = response['text']
    # send message
    reply(sender, message)

def get_default(request):
    context = request['context']
    entities = request['entities']
    greetings = "I am a persnoal assitent of Parth Shah he is busy makeing somthing.\nOh i didt tell you\nYou can connect and control Parth's home\nYou can do the following\n\n1) Switch on or off the lights \n2) Get house temperature"
    context['greetings'] = greetings
    return context

def getWork(request):
    context = request['context']
    entities = request['entities']
    work = "Developer In Progress and Hardware Enthusiast"
    context['work'] = work
    return context

def getLight(request):
    context = request['context']
    entities = request['entities']
    pin = 18 # GPIO PIN 18
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    work = "light is on!!"
    context['lightson'] = work
    return context

def getLightoff(request):
    context = request['context']
    entities = request['entities']
    pin = 18 # GPIO PIN 18
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    work = "light is off now!!!\nCan sleep peacefully now.."
    context['loff'] = work
    return context

def getTemp(request):
    context = request['context']
    entities = request['entities']
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Vadodara&APPID=cab0f79f26e17e450393a077c8350425'
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    temp = data['main']['temp'] - 273.15
    context['temp'] = temp
    return context


actions = {
    'send': send,
    'getDefault': get_default,
    'getWork'   : getWork,
    'getLightOn'  : getLight,
    'getLightOff'  : getLightoff,
    'getTemp'  : getTemp,

}

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)


if __name__ == '__main__':
    app.run(debug=True)
