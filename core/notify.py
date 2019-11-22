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

    now = datetime.now()

    #If there are changes, or it's time for dayly notification
    if (trail._countEdited != 0 or trail._countAdded != 0 or trail._countDeleted != 0) or now.hour ==23:

        #Init bot
        bot = telegram.Bot(token=telegram_token)
        msgCounter = 0

        #Summed informations/stats
        message = "📥{} ✔️{} ✏️{} 🗑{} ➕{}\n\n".format(trail._countFetched,trail._countPassed,trail._countEdited,trail._countDeleted,trail._countAdded)

        #Loop in edited events
        for editedEvent in trail._editedEvents:
            #Check if message is not too long for telegram, else split it
            if (msgCounter > 25):
                bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
                message = ''
                msgCounter = 1
                message += "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)
            else:
                msgCounter += 1
                message += "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)

        #Loop in added events
        for addedEvent in trail._addedEvents:
            #Check if message is not too long for telegram, else split it
            if (msgCounter > 25):
                bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
                message = ''
                msgCounter = 1
                message += "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
            else:
                message += "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
                msgCounter += 1

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
