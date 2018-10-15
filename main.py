from telebot import types
from telebot.types import Message
import telebot

t = open('token.txt','r')
TOKEN = t.readline()
t.close()

bot = telebot.TeleBot(TOKEN)

print(bot.get_me())

def get_title(chat):
    if chat.title:
        return chat.title
    else:
        return chat.username

def parse_db(file):
    f = open(file,'r')
    r = f.readlines()
    for i in range(len(r)):
        tmp = r[i].replace('\n','').split(';')
        r[i] = {'id' : tmp[0], 'title':tmp[1] }
    return r

print('------------------------------')
print(parse_db('db.txt'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, 'Hello, my name is dodislav bot. I can send messages to any group I am in.')
    f = open('db.txt','a')
    db = parse_db('db.txt')
    id = message.chat.id

    new_user = True
    for pg in db:
        if pg['id'] == str(id):
            new_user = False
            break

    if new_user:
        f.write(str(message.chat.id) + ';' + str(get_title(message.chat)) + '\n')
    f.close()

@bot.message_handler(commands=['register'])
def reg_func(message: Message):
    f = open('db.txt','a')
    db = parse_db('db.txt')
    id = message.chat.id

    new_user = True
    for pg in db:
        if pg['id'] == str(id):
            new_user = False
            break

    if not new_user:
        bot.send_message(message.chat.id, 'you are already registered')
    else:
        f.write(str(message.chat.id) + ';' + str(get_title(message.chat)) + '\n')
        bot.send_message(message.chat.id, 'your chat successfuly registered')

    f.close()

@bot.message_handler(content_types=['new_chat_members'])
def send_wel(message :Message):
    bot.send_message(message.chat.id, 'zdarova laham, privet petuham')


@bot.message_handler(commands=['sendtoall'])
def send_msg_to_all(message):
    for user in parse_db('db.txt'):
        bot.send_message(int(user['id']), message.text.replace('/sendtoall ', ''))


@bot.message_handler(commands=['sendtochat'])
def send_msg_to_group(message):
    for id in parse_db('db.txt'):
        bot.send_message(int('id'), message.text.replace('/sendtochat ', ''))


@bot.message_handler(commands=['unregister'])
def unregister(message):
    bool = False
    for user in parse_db('db.txt'):
        if int(user['id']) == message.chat.id:
            bool = True
    if bool:
        db = parse_db('db.txt')
        f = open('db.txt','w')
        bot.send_message(message.chat.id, 'You successfuly unregisted this chat')
        for user in db:
            if user != str(message.chat.id):
                print(id)
                f.write(user['id'] + ';' + user['title'] +'\n')
    else:
        bot.send_message(message.chat.id, 'This chat is not registered')


@bot.message_handler(commands=['sendtogroup'])
def sendtogroup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itembtn = None
    users = parse_db('db.txt')
    for i in range(len(users)):
        itembtn = types.KeyboardButton(users[i]['title'])
        markup.add(itembtn)
    bot.send_message(message.chat.id, "Choose reciever:", reply_markup=markup)



@bot.message_handler(content_types=['text'])
def getgroupname(message):
    print(message.reply_to_message.from_user, end='@@@')
    for user in parse_db('db.txt'):
        if message.text == user['title']:
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, 'What you want to send',reply_markup=markup)


@bot.message_handler(func=lambda message: message.reply_to_message.from_user == bot.get_me())
def getmsgtosend(message: Message):
    bot.send_message(message.caht.id, 'True')

#@bot.message_handler(commands=['scrap'])
#def scrap(message):




bot.polling()