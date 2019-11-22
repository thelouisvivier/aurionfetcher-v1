# La classe
from aurion import *

#Configuration
import config

# Modules de temps
from datetime import datetime, timedelta
from time import mktime, sleep, time

#ics
from ics import Calendar, Event
from uuid import uuid4

# Current directory
from os import getcwd

#
import pause


debut = int(1567352828) #first day of school year
fin = int(1593618428) #last day of school year

# On initialise l'objet en supposant que geckodriver est dans le répertoire courant
aurion = Aurion("", "", "firefox", "/home/louis/aurionfetcher/geckodriver")

# On récupère les informations de login
aurion.queryInformations()

# On descend le planning en JSON
fetchedEvents = aurion.queryPlanningOnPeriod(debut, fin)
returnedStats = aurion.syncCaldav(fetchedEvents)
aurion.notifyTelegram(returnedStats)
#print('en pause')
#pause.minutes(1)
#print('en reveil')
