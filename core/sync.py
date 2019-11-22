"""
    Caldav Sync
"""

# Credentials
from config.config import *

# Calddav connection
import caldav
from caldav.elements import dav, cdav

# iCal Object
from datetime import datetime
from ics import Calendar, Event
from uuid import uuid4
from dateutil.parser import parse
import pytz

# Regex
import re

def caldavSync(trail):

    def createICS(deb,fin,matiere,salle,prof,uid):
        e = Event()
        e.name = "{}".format(matiere)
        e.begin = deb
        e.end = fin
        e.location = salle
        e.description = "{} en {} par {}".format(matiere,salle,prof)
        e.uid = uid
        return e

    #Init caldav connection
    clientCalDav = caldav.DAVClient(url=caldav_url, username=caldav_username, password=caldav_password)
    principalCalDav = clientCalDav.principal()
    calendarsCalDav = principalCalDav.calendars()
    calendarCalDav = calendarsCalDav[0]

    #Log information
    print("        Check events to add/edit/delete")
    trail._countFetched = len(trail._fetchedEvents)
    trail._countEdited = 0
    trail._countPassed = 0
    trail._countDeleted = 0
    trail._editedEvents = []

    #Loop in existing events
    for actualEvent in calendarCalDav.events():

        #Parse informations from ics
        if (re.findall(r"SUMMARY:(.*)",actualEvent.data)):
            actualSummary = re.findall(r"SUMMARY:(.*)",actualEvent.data)[0].replace("\\", '')
        else:
            actualSummary = ''
        actualLocation = re.findall(r"LOCATION:(.*)",actualEvent.data)[0]
        actualDescription = re.findall(r"DESCRIPTION:((.|\n)*)LOCATION",actualEvent.data)[0][0].replace('\n ', '').replace('\r ', '').replace('\n', '').replace('\r', '').replace("\\", '')
        actualDTSART = re.findall(r"DTSTART:(.*)",actualEvent.data)[0]
        actualDTEND = re.findall(r"DTEND:(.*)",actualEvent.data)[0]
        actualUID = re.findall(r"UID:(.*)",actualEvent.data)[0]
        trail._founded = 0

        #Loop in fetched events
        for newEvent in trail._fetchedEvents:
            #Create ics file
            toAdd = createICS(newEvent['debut'],newEvent['fin'],newEvent['cours'],newEvent['salle'],newEvent['prof'],str(uuid4()))
            local_tz = pytz.timezone ("Europe/Paris")
            debUTC = parse(str(toAdd.begin)).astimezone(pytz.utc)
            strdeb = debUTC.strftime("%Y%m%d")+"T"+debUTC.strftime("%H%M%S")+"Z"
            finUTC = parse(str(toAdd.end)).astimezone(pytz.utc)
            strfin = finUTC.strftime("%Y%m%d")+"T"+finUTC.strftime("%H%M%S")+"Z"

            #Compare each event, if match one dates then compare info
            if (actualDTSART == strdeb and actualDTEND == strfin):
                #Compare infos
                if (actualSummary != toAdd.name or actualLocation != toAdd.location or actualDescription != toAdd.description):
                    toEdit = createICS(newEvent['debut'],newEvent['fin'],newEvent['cours'],newEvent['salle'],newEvent['prof'],actualUID)
                    vcal = Calendar()
                    #print(actualEvent.data)
                    vcal.events.add(toEdit)
                    actualEvent.data = str(vcal)
                    #print(actualEvent.data)
                    actualEvent.save()
                    trail._editedEvents.append(toEdit)
                    trail._countEdited+=1
                #Delete already checked events
                trail._founded = 1
                trail._fetchedEvents.remove(newEvent)
                trail._countPassed+=1
                break
                #Delete actualevent because not found in trail._fetchedEvents

        #If no match, then delete from caldav
        if (trail._founded == 0):
            trail._countDeleted+=1
            actualEvent.delete()

    trail._countAdded = 0
    trail._addedEvents = []

    #Add new events
    for newEvent in trail._fetchedEvents:
        vcal = Calendar()
        toAdd = createICS(newEvent['debut'],newEvent['fin'],newEvent['cours'],newEvent['salle'],newEvent['prof'],str(uuid4()))
        vcal.events.add(toAdd)
        calendarCalDav.add_event(str(vcal))
        trail._addedEvents.append(toAdd)
        trail._countAdded+=1

    #Log informations
    print("        {} total fetched. {} edited. {} deleted. {} checked. {} added.".format(trail._countFetched,trail._countEdited,trail._countDeleted,trail._countPassed,trail._countAdded))
    print ("        Sync done !")
    return True
