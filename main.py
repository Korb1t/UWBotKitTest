from telebot import types
from telebot.types import Message
import telebot

t = open('token.txt','r')
TOKEN = t.readline()
t.close()

bot = telebot.TeleBot(TOKEN)

def parse_db(file):
    f = open(file,'r')
    r = f.readlines()
    for i in range(len(r)):
        tmp = r[i].replace('\n','').split(';')
        r[i] = {'id' : tmp[0], 'title':tmp[1] }
    return r

print('>>>Debug: Bot Started')
print('>>>DataBase:')
print(parse_db('db.txt'))
print(">>>End----------------------------------------------")

def get_title(chat):
    if chat.title:
        return chat.title
    else:
        return chat.username

def get_id_by_title(title):
    #print(title)
    for user in parse_db('db.txt'):
        #print(user['title'])
        if str(user['title']) == str(title):
            return int(user['id'])
    return None

def get_title_by_id(id):
    for user in parse_db('db.txt'):
        if user['id'] == id:
            return user['title']
    return None


@bot.message_handler(func=lambda message: message.reply_to_message != None)
def getmsgtosend(message: Message):
    if message.reply_to_message.text.startswith('What do you want to send to'):
        title = message.reply_to_message.text.replace('What do you want to send to ','')
        print(get_id_by_title(title))
        if get_id_by_title(title) != None:
            bot.send_message(get_id_by_title(title), message.text)
            print('>>>Message sent to ' + title + " and says:" + message.text)



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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    itembtn = None
    users = parse_db('db.txt')
    for i in range(len(users)):
        itembtn = types.KeyboardButton(users[i]['title'])
        markup.add(itembtn)
    bot.send_message(message.chat.id, "Choose reciever:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def getgroupname(message):
    for user in parse_db('db.txt'):
        if message.text == user['title']:
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, 'What do you want to send to ' + user['title'],reply_markup=markup)





bot.polling()