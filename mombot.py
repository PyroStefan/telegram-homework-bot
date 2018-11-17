from datetime import datetime
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utility.db_init as db_init
import utility.db_actions as db_actions

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

with open("API_KEY", "r") as apifile:
    API_KEY = apifile.read()

updater = Updater(token=API_KEY)
dispatcher = updater.dispatcher
engine = create_engine('sqlite:///db/homework.db')
db_init.Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def hw_add(bot, update, args, session=session): 
    """Add homework entry to the database"""
    print("Calling hw_add")
    if not len(args):
        bot.send_message(chat_id=update.message.chat_id,
         text="added nothing: you're missing an argument")
        return False

    subject = args[0]
    homework = " ".join(args[1:])
    db_actions.add_hw(subject, homework, session)

    bot.send_message(chat_id=update.message.chat_id, text="added {} : {} ".format(
        subject, homework
    ))


def which_hw(bot, update, args, session=session): 
    """Lists homework from the database"""
    print("Calling which_hw")

    if not args:
        result = db_actions.query_all_homework(session)
    else:
        result = db_actions.query_homework_by_subject(args[0], session)
    
    header_string = "ID- DATE ADDED - SUBJECT - HOMEWORK\n"
    result_list = [ "{} - {}/{}/{} - {} - {} ".format(
            i.id, 
            i.date_added.day, i.date_added.month, i.date_added.year,
             i.subject, 
             i.todo 
        ) 
        for i in result ]
    result_text = header_string + "\n".join(result_list)
    bot.send_message(chat_id=update.message.chat_id, text=result_text)

def delete_homework(bot, update, args, session=session):
    """Deletes an homework entry to the database"""
    print("Calling delete_homework")
    if not args:
        bot.send_message(chat_id=update.message.chat_id,
        text="You forgot to add an ID. Please try again")
        return False
    try:
        id = int(args[0])
    except: 
        bot.send_message(chat_id=update.message.chat_id,
        text="The ID needs to be a number. Please try again")

    db_actions.del_hw(id, session)
    bot.send_message(chat_id=update.message.chat_id,
    text="Homework ID {} deleted.".format(args[0]))




hw_add_handler = CommandHandler("hw_add", hw_add, pass_args=True)
which_hw_handler = CommandHandler("which_hw", which_hw, pass_args=True)
del_hw_handler = CommandHandler("hw_del", delete_homework, pass_args=True)
dispatcher.add_handler(which_hw_handler)
dispatcher.add_handler(hw_add_handler)
dispatcher.add_handler(del_hw_handler)


updater.start_webhook(listen='127.0.0.1', port=5001, url_path=API_KEY)
updater.bot.set_webhook(
   url='https://aperturect.com:8443/'+API_KEY
)
updater.start_webhook(listen='127.0.0.1', port=5000)


