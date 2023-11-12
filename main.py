import telebot
from telebot import types
import json

import db

token='6637453852:AAHcU8sDCa8HyILGHXrXQvVgSq_daBDLvlI'
bot=telebot.TeleBot(token)

questions = json.load(open("questions.json","rb"))
question = questions[0]

print('Бот работает!\n')

def delete_previous(message):
    bot.delete_message(message.chat.id,message.id)

@bot.message_handler(commands=['start'])
def start(message):
    # Add user to database if it's a newbie
    db.execute("INSERT IGNORE INTO completions (chat_id, username) VALUES (%s, %s)",message.chat.id,message.chat.username)
    print("("+str(message.chat.id)+") "+str(message.chat.username)+" начал играть!")
    
    db.cursor.execute("SELECT current FROM completions WHERE chat_id = %s",(message.chat.id,))
    query_result = db.cursor.fetchall()
    
    current = 0
    if query_result:
        current = query_result[0][0]
    else:
        print("=== в первый раз!")

    global question
    question = questions[current]

    delete_previous(message)
    new_question(message)

def new_question(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)

    if "answers" in question:
        for button in question['answers']:
            keyboard.add(types.InlineKeyboardButton(button[0], callback_data=str(button[1])))

    bot.send_photo(message.chat.id, open("images/"+question["image"]+".png", "rb"),question["text"], parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def answer(message):
    global question
    
    print("("+str(message.chat.id)+") "+str(message.chat.username)+" ответил: "+message.text)
    for answer in question['answers']:
        if message.text == answer[0]:
            question = questions[int(answer[1])]
            db.execute("UPDATE completions SET current = (%s) WHERE chat_id = (%s)",int(answer[1]),message.chat.id)
            if int(answer[1])==1:
                print("=== и прошел квест!")
                db.execute("INSERT IGNORE INTO competitors (chat_id, username) VALUES (%s, %s)",message.chat.id,message.chat.username)
                db.execute("UPDATE completions SET endings_count=endings_count+1 WHERE chat_id = (%s)",message.chat.id)
            new_question(message)
            return
    bot.send_message(message.chat.id,"Не понял че сказал")

if __name__=='__main__':
    bot.infinity_polling()