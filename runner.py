"""
    Run the full program. Get events, Sync events, and Notify
"""

import sys

from core.configfilechecker import *
from core.credfetcher import *
from core.eventsfetcher import *
from core.sync import *
from core.notify import *
from core.storage import *

from datetime import datetime, timedelta

# Sleep
from time import sleep


telegramNotifyOnBoot()
print("######## Booted ########")
print("Refresh every : " + str(refresh_every) + "seconds")

while True:
    try:
        start_time = datetime.now()
        print(start_time)

        #Check values in config file
        configfilechecker()

        # On init Storage
        trail = Storage()

        # On récupère les informations de login
        credfetcher(trail)

        # On descend le planning en JSON
        eventsfetcher(trail)
        caldavSync(trail)
        telegramNotifier(trail)

        now = datetime.now()
        nextrun = start_time + timedelta(0,refresh_every)
        print("        Next run at "+ nextrun)
        sleep(abs(nextrun - now).seconds)

    except NameError:
        print('Config file error')
        raise
        telegramNotifyOnError()
        sys.exit()
    except:
        telegramNotifyOnError()
        print("Unexpected error in runner:", sys.exc_info()[0])
        sys.exit()
