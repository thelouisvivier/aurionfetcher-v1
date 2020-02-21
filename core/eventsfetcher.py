"""
    Aurion Events Fetcher
"""
import sys

# Credentials
from config.config import *

#Storage
from core.storage import *

# HTTP requests
import requests

# XML parser
from xml.etree import ElementTree as etree

# JSON parser
import json

def eventsfetcher(trail):
    try:
        #downloads events between two dates (from config.py)

        # x1000
        start = aurion_startdate * 1000
        end = aurion_endate * 1000

        #Cookie
        cookies = {
            "JSESSIONID": trail._sessionId,
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

        # Data
        data = [
          ("javax.faces.partial.ajax", "true"),
          ("javax.faces.source", trail._formId),
          ("javax.faces.partial.execute", trail._formId),
          ("javax.faces.partial.render", trail._formId),
          (trail._formId, trail._formId),
          (trail._formId + "_start", start),
          (trail._formId + "_end", end),
          ("form", "form"),
          ("form:largeurDivCenter", "1606"),
          ("form:j_idt133_view", "week"),
          ("form:offsetFuseauNavigateur", "-7200000"),
          ("form:onglets_activeIndex", "0"),
          ("form:onglets_scrollState", "0"),
          ("javax.faces.ViewState", trail._viewState),
        ]

        #Request
        r = requests.post(aurion_url + "/faces/Planning.xhtml", headers=headers, cookies=cookies, data=data)

        #XML answer
        xml = etree.fromstring(r.text)

        #Parse in Json
        events = json.loads(xml.findall(".//update")[1].text)["events"]

        trail._fetchedEvents = []

        #Format data
        for i in range(0, len(events)):
            tmp = events[i]["title"]
            tmp = tmp.split("\n")
            for j in range(0, len(tmp)):
                #Remove begining and end blank space
                tmp[j] = tmp[j].strip()

            #Teachers name
            #Remove Monsieur/Madame
            #tmp[3] = tmp[3].replace("M ", '')
            #tmp[3] = tmp[3].replace("MME ", '')
            #To lower case
            tmp[3] = tmp[3].lower()
            #First leters upper case
            tmp[3] = tmp[3].title()
            #Remove ISEN
            tmp[0] = tmp[0].replace("- ISEN ", '')
            #Format tittle
            tmp[1] = tmp[1].replace("Cours de ", '')
            tmp[1] = tmp[1].replace("Cours d'", '')
            tmp[1] = tmp[1].replace(" de ", ' ')
            tmp[1] = tmp[1].replace(" d' ", ' ')
            
            #Check if it's a test
            try:
                events[i]["className"]
            except NameError:
            else:
                tmp[1] = "🎓"+tmp[1]
            
            #Final formated events
            tmp = {"debut":events[i]["start"], "fin":events[i]["end"], "cours":tmp[1], "salle":tmp[0], "prof":tmp[3]}
            trail._fetchedEvents.append(tmp)

        return True
    except:
        print("Unexpected error in eventsfetcher:", sys.exc_info()[0])
