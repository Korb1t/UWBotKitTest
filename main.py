from telebot.types import Message
from telebot import types
import telebot

TOKEN;

bot = telebot.TeleBot(TOKEN)

def parse_db(file):
    f = open(file,'r')
    r = f.readlines()
    for i in range(len(r)):
        r[i] = r[i].replace('\n','')
    return r

#db = parse_db('db.txt')

@bot.message_handler(commands=['start', 'help', 'register'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, 'Hello, my name is dodislav bot. I can send messages to any group I am in.')
    f = open('db.txt','a')
    if str(message.chat.id) in parse_db('db.txt'):
        bot.send_message(message.chat.id, 'you are already registered')
    else:
        f.write(str(message.chat.id) + '\n')
        bot.send_message(message.chat.id, 'your chat successfuly registered')


@bot.message_handler(content_types=['new_chat_members'])
def send_wel(message :Message):
    bot.send_message(message.chat.id, 'zdarova laham, privet petuham')


@bot.message_handler(commands=['sendtoall'])
def send_msg_to_all(message):
    for id in parse_db('db.txt'):
        bot.send_message(int(id), message.text.replace('/sendtoall ', ''))


@bot.message_handler(commands=['sendtochat'])
def send_msg_to_group(message):
    for id in parse_db('db.txt'):
        bot.send_message(int(id), message.text.replace('/sendtochat ', ''))


@bot.message_handler(commands=['unregister'])
def unregister(message):
    bool = False
    for id in parse_db('db.txt'):
        if int(id) == message.chat.id:
            bool = True
    if bool:
        db = parse_db('db.txt')
        f = open('db.txt','w')
        bot.send_message(message.chat.id, 'You successfuly unregisted this chat')
        for id in db:
            if id != str(message.chat.id):
                print(id)
                f.write(id + '\n')
    else:
        bot.send_message(message.chat.id, 'This chat is not registered')


#@bot.message_handler(commands=['scrap'])
#def scrap(message):




bot.polling()