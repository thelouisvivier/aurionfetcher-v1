"""
    Telegram Notifier
"""
# Credentials
from config.config import *

# Telegram
import telegram

# Datetime
from datetime import datetime
from dateutil.parser import parse


def telegramNotifier(trail):
    try:
        now = datetime.now()

        #If there are changes, or it's time for dayly notification
        if (trail._countEdited != 0 or trail._countAdded != 0 or trail._countDeleted != 0) or now.hour ==23:

            #Init bot
            bot = telegram.Bot(token=telegram_token)

            #Summed informations/stats
            message = "📥{} ✔️{} ✏️{} 🗑{} ➕{}\n\n".format(trail._countFetched,trail._countPassed,trail._countEdited,trail._countDeleted,trail._countAdded)

            #Loop in edited events
            for editedEvent in trail._editedEvents:
                temp_message = "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)
                #Check if message is not too long for telegram, else split it
                if((len(message)+len(temp_message))>4096):
                    bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
                    message = ''
                    message += temp_message
                else:
                    message += temp_message

            #Loop in added events
            for addedEvent in trail._addedEvents:
                temp_message = "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
                #Check if message is not too long for telegram, else split it
                if((len(message)+len(temp_message))>4096):
                    bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
                    message = ''
                    message+=temp_message
                else:
                    message+=temp_message

            #send message
            bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)

            #Log informations
            if(now.hour ==23):
                print("        Daily Notification. Sent")
            else:
                print("        Changes Detected. Notification Sent")

        #0 changes. Don't send a notification
        else:
            #Log informations
            print("        Nothing Changed. No Notification Sent.")
    except:
        print("Unexpected error in notify:", sys.exc_info()[0])

def telegramNotifyOnBoot():
    try:
        #Init bot
        bot = telegram.Bot(token=telegram_token)
        message = "<b>🤖BIP BIP AurionFetcher has started</b>\n⏰ Going to refresh every {} seconds.\n📆 Sync with {}.".format(str(refresh_every),caldav_url)
        bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
    except:
        print("Unexpected error in notifyOnBoot:", sys.exc_info()[0])

def telegramNotifyOnError():
    try:
        #Init bot
        bot = telegram.Bot(token=telegram_token)
        message = "<b>🤖BIP BIP AurionFetcher have an error</b>\nSTOPPING NOW"
        bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
    except:
        print("Unexpected error in notifyOnError:", sys.exc_info()[0])
