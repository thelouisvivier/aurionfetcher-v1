"""
    Config File Checker
"""
import sys

# Credentials
from config.config import *

def configfilechecker():
    if(aurion_url == ""):
        raise NameError('Missing aurion_url')
    if(aurion_username == ""):
        raise NameError('Missing aurion_username')
    if(aurion_password == ""):
        raise NameError('Missing aurion_password')
    if(aurion_startdate == 0):
        raise NameError('Missing aurion_startdate')
    if(aurion_endate == 0):
        raise NameError('Missing aurion_endate')
    if(telegram_token == ""):
        raise NameError('Missing telegram_token')
    if(telegram_chatid == ""):
        raise NameError('Missing telegram_chatid')
    if(caldav_url == ""):
        raise NameError('Missing caldav_url')
    if(caldav_username == ""):
        raise NameError('Missing caldav_username')
    if(caldav_password == ""):
        raise NameError('Missing caldav_password')
    if(refresh_every == ""):
        raise NameError('Missing refresh_every')
