#!/usr/bin/python3
# -*-encoding:utf-8 -*

# HTTP requests
import requests

# Selenium for Firefox/Chrome control
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# XML parser
from xml.etree import ElementTree as etree

# JSON parser
import json

# Sleep
from time import sleep

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

# Telegram
import telegram

# Array
import array



class Aurion:
    """
        Sur la base du travail de Bdeliers : https://github.com/BDeliers/Python-Planning-Aurion

        Par thelouisvivier
    """

    def __init__(self, username, password, browser, driver):
        self._url = "https://aurion.yncrea.fr"
        self._username = username
        self._password = password
        self._browser = browser
        self._driver = driver
        self._caluser = ''
        self._calpass = ''
        self._calurl = '' + self._caluser
        self._telegramtoken = ""
        self._telegramchatid = ""

        if ((self._browser != "firefox") and (self._browser != "chrome")):
            print("Invalid browser")
            exit()

    def queryPlanningOnPeriod(self, start, end):
        """
            Télécharge les données du planning entre un timestamp start et un timestamp end
        """

        # x1000 nénécessaire
        start = start * 1000
        end = end * 1000

        # Cookie à envoyer
        cookies = {
            "JSESSIONID": self._sessionId,
        }

        # Headers
        headers = {
            "Host": "aurion.yncrea.fr",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Language": "fr-FR,fr;q=0.5",
            "Referer": "https://aurion.yncrea.fr/faces/Planning.xhtml",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
        }

        # Données
        data = [
          ("javax.faces.partial.ajax", "true"),
          ("javax.faces.source", self._formId),
          ("javax.faces.partial.execute", self._formId),
          ("javax.faces.partial.render", self._formId),
          (self._formId, self._formId),
          (self._formId + "_start", start),
          (self._formId + "_end", end),
          ("form", "form"),
          ("form:largeurDivCenter", "1606"),
          ("form:j_idt133_view", "week"),
          ("form:offsetFuseauNavigateur", "-7200000"),
          ("form:onglets_activeIndex", "0"),
          ("form:onglets_scrollState", "0"),
          ("javax.faces.ViewState", self._viewState),
        ]

        # La requête
        r = requests.post(self._url + "/faces/Planning.xhtml", headers=headers, cookies=cookies, data=data)

        # Retour en XML
        xml = etree.fromstring(r.text)
        # On parse la parti intéressante en JSON
        events = json.loads(xml.findall(".//update")[1].text)["events"]

        eventsFormatted = []
        # On formatte un peu tout ça
        for i in range(0, len(events)):
            tmp = events[i]["title"]
            tmp = tmp.split("\n")
            for j in range(0, len(tmp)):
                # Espaces en début/fin
                tmp[j] = tmp[j].strip()
            # Les noms de profs
            # On enlève Monsieur/Madame
            #tmp[3] = tmp[3].replace("M ", '')
            #tmp[3] = tmp[3].replace("MME ", '')
            # En minuscule
            tmp[3] = tmp[3].lower()
            # Première lettre en majuscule
            tmp[3] = tmp[3].title()
            # On enlève ISEN devant le nom de salles
            tmp[0] = tmp[0].replace("- ISEN ", '')
            #Formatage titre
            tmp[1] = tmp[1].replace("Cours de ", '')
            tmp[1] = tmp[1].replace("Cours d'", '')
            tmp[1] = tmp[1].replace(" de ", ' ')
            tmp[1] = tmp[1].replace(" d' ", ' ')
            # Un bel évènement formaté
            tmp = {"debut":events[i]["start"], "fin":events[i]["end"], "cours":tmp[1], "salle":tmp[0], "prof":tmp[3]}
            # On l'ajoute à la liste
            eventsFormatted.append(tmp)

        return eventsFormatted

    def queryInformations(self):
        """
            Récupère les informations vitales au programme : le cookie de session et le ViewState, ne retourne rien
        """

        # Propre à Firefox
        if self._browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            # Options Firefox sans interface
            options = Options()
            options.add_argument("--headless")

            # On initialise le driver
            driver = webdriver.Firefox(options=options, executable_path=self._driver)

        # Propre à Chrome
        if self._browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            # Options Chrome sans interface
            options = Options()
            options.add_argument("-headless")
            options.add_argument("-disable-gpu")

            # On initialise le driver
            driver = webdriver.Chrome(options=options, executable_path=self._driver)

        # On se connecte au formulaire de login
        driver.get(self._url + "/faces/Login.xhtml")

        # On attend le chargement de la page de login d'Aurion
        while True:
            try:
                print ("        Page de connexion chargée")
                driver.find_element_by_id("username")
                break
            except:
                sleep(1)
                continue

        # On le remplit avec les infos de l'utilisateur et on le valide
        driver.find_element_by_id("username").send_keys(self._username)
        driver.find_element_by_id("password").send_keys(self._password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        print ("        Connecté")
        # On attend le chargement de la page d'accueil d'Aurion
        #while True:
        #    try:
        #        # On clicke sur l'onglet Scolarité
        #        driver.find_element_by_xpath("//*[contains(text(), 'Scolarité')]").click()
        #        break
        #    except:
        #        sleep(1)
        #        continue

        # On attend le chargement de l'onglet scolarité' d'Aurion
        while True:
            try:
                # On clicke sur l'onglet Planning
                driver.find_element_by_xpath("//*[contains(text(), 'My Schedule')]").click()
                break
            except:
                sleep(1)
                continue

        # Quand le planning est chargé
        while True:
            try:
                print ("        Planning chargé")
                driver.find_element_by_class_name("fc-month-button")
                break
            except:
                sleep(1)
                continue

        # On récupère la valeur du ViewState
        self._viewState = driver.find_element_by_xpath("//input[@name='javax.faces.ViewState']").get_attribute("value")

        # On récupère l'id du form (form:j_idtxxx)
        self._formId = driver.find_element_by_class_name("schedule").get_attribute("id")

        # On récupère le cookie
        cookies = driver.get_cookies()
        self._sessionId = ""

        # On garde l'ID de session
        for c in cookies:
            if c["name"] == "JSESSIONID":
                self._sessionId = c["value"]

        # On ferme le navigateur
        driver.close()

        return True

    def syncCaldav(self,newEvents):

        def createICS(deb,fin,matiere,salle,prof,uid):
            e = Event()
            e.name = "{}".format(matiere)
            e.begin = deb
            e.end = fin
            e.location = salle
            e.description = "{} en {} par {}".format(matiere,salle,prof)
            e.uid = uid
            return e


        clientCalDav = caldav.DAVClient(url=self._calurl, username=self._caluser, password=self._calpass)
        principalCalDav = clientCalDav.principal()
        calendarsCalDav = principalCalDav.calendars()
        calendarCalDav = calendarsCalDav[0]
        print("        Check des évènements déjà ajoutés/à ajouter")
        countFetched = len(newEvents)
        countEdited = 0
        countPassed = 0
        countDeleted = 0
        editedEvents = []
        for actualEvent in calendarCalDav.events():
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
            for newEvent in newEvents:
                toAdd = createICS(newEvent['debut'],newEvent['fin'],newEvent['cours'],newEvent['salle'],newEvent['prof'],str(uuid4()))
                local_tz = pytz.timezone ("Europe/Paris")
                debUTC = parse(str(toAdd.begin)).astimezone(pytz.utc)
                strdeb = debUTC.strftime("%Y%m%d")+"T"+debUTC.strftime("%H%M%S")+"Z"
                finUTC = parse(str(toAdd.end)).astimezone(pytz.utc)
                strfin = finUTC.strftime("%Y%m%d")+"T"+finUTC.strftime("%H%M%S")+"Z"
                if (actualDTSART == strdeb and actualDTEND == strfin):
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
                    #delete actualevent because not found in newevents
            if (founded == 0):
                countDeleted+=1
                actualEvent.delete()

        countAdded = 0
        addedEvents = []
        for newEvent in newEvents:
            vcal = Calendar()
            toAdd = createICS(newEvent['debut'],newEvent['fin'],newEvent['cours'],newEvent['salle'],newEvent['prof'],str(uuid4()))
            vcal.events.add(toAdd)
            calendarCalDav.add_event(str(vcal))
            addedEvents.append(toAdd)
            countAdded+=1

        print("        {} total fetched. {} edited. {} deleted. {} passed. {} added.".format(countFetched,countEdited,countDeleted,countPassed,countAdded))
        print ("        Done !")
        statsResults = {}
        statsResults["countFetched"] = countFetched
        statsResults["countEdited"] = countEdited
        statsResults["countDeleted"] = countDeleted
        statsResults["countPassed"] = countPassed
        statsResults["countAdded"] = countAdded
        statsResults["addedEvents"] = addedEvents
        statsResults["editedEvents"] = editedEvents
        return statsResults

    def notifyTelegram(self, returnedStats):
        now = datetime.now()
        if (returnedStats["countEdited"] != 0 or returnedStats["countAdded"] != 0 or returnedStats["countDeleted"] != 0) or now.hour ==23:
            bot = telegram.Bot(token=self._telegramtoken)
            msgCounter = 0
            message = "📥{} ✔️{} ✏️{} 🗑{} ➕{}\n\n".format(returnedStats["countFetched"],returnedStats["countPassed"],returnedStats["countEdited"],returnedStats["countDeleted"],returnedStats["countAdded"])
            for editedEvent in returnedStats["editedEvents"]:
                if (msgCounter > 25):
                    bot.sendMessage(chat_id=self._telegramchatid, text=message,parse_mode=telegram.ParseMode.HTML)
                    message = ''
                    msgCounter = 1
                    message += "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)
                else:
                    msgCounter += 1
                    message += "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)
            for addedEvent in returnedStats["addedEvents"]:
                if (msgCounter > 25):
                    bot.sendMessage(chat_id=self._telegramchatid, text=message,parse_mode=telegram.ParseMode.HTML)
                    message = ''
                    msgCounter = 1
                    message += "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
                else:
                    message += "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
                    msgCounter += 1
            bot.sendMessage(chat_id=self._telegramchatid, text=message,parse_mode=telegram.ParseMode.HTML)
            if(now.hour ==23):
                print("        Daily Notification. Sent")
            else:
                print("        Changes Detected. Notification Sent")

        else:
            print("        Nothing Changed. No Notification Sent.")
