"""
    Caldav Sync
"""

# Credentials
from config import *

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

def caldavSync(trail,newEvents):

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
    countFetched = len(newEvents)
    countEdited = 0
    countPassed = 0
    countDeleted = 0
    editedEvents = []

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
        founded = 0

        #Loop in fetched events
        for newEvent in newEvents:
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
                    editedEvents.append(toEdit)
                    countEdited+=1
                #Delete already checked events
                founded = 1
                newEvents.remove(newEvent)
                countPassed+=1
                break
                #Delete actualevent because not found in newevents

        #If no match, then delete from caldav
        if (founded == 0):
            countDeleted+=1
            actualEvent.delete()

    countAdded = 0
    addedEvents = []

    #Add new events
    for newEvent in newEvents:
        vcal = Calendar()
        toAdd = createICS(newEvent['debut'],newEvent['fin'],newEvent['cours'],newEvent['salle'],newEvent['prof'],str(uuid4()))
        vcal.events.add(toAdd)
        calendarCalDav.add_event(str(vcal))
        addedEvents.append(toAdd)
        countAdded+=1

    #Log informations
    print("        {} total fetched. {} edited. {} deleted. {} passed. {} added.".format(countFetched,countEdited,countDeleted,countPassed,countAdded))
    print ("        Sync done !")

    #Make stats for notifier
    statsResults = {}
    statsResults["countFetched"] = countFetched
    statsResults["countEdited"] = countEdited
    statsResults["countDeleted"] = countDeleted
    statsResults["countPassed"] = countPassed
    statsResults["countAdded"] = countAdded
    statsResults["addedEvents"] = addedEvents
    statsResults["editedEvents"] = editedEvents
    return statsResults
