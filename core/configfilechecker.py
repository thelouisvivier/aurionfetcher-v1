"""
    Config File Checker
"""
import sys

# Credentials
from config.config import *

def configfilechecker():
    if(aurion_url == ""):
        raise BrokenConfigFile('Missing aurion_url')
    if(aurion_username == ""):
        raise BrokenConfigFile('Missing aurion_username')
    if(aurion_password == ""):
        raise BrokenConfigFile('Missing aurion_password')
    if(aurion_startdate == 0):
        raise BrokenConfigFile('Missing aurion_startdate')
    if(aurion_endate == 0):
        raise BrokenConfigFile('Missing aurion_endate')
    if(telegram_token == ""):
        raise BrokenConfigFile('Missing telegram_token')
    if(telegram_chatid == ""):
        raise BrokenConfigFile('Missing telegram_chatid')
    if(caldav_url == ""):
        raise BrokenConfigFile('Missing caldav_url')
    if(caldav_username == ""):
        raise BrokenConfigFile('Missing caldav_username')
    if(caldav_password == ""):
        raise BrokenConfigFile('Missing caldav_password')
    if(refresh_every == ""):
        raise BrokenConfigFile('Missing refresh_every')
