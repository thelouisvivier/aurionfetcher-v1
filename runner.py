"""
    Run the full program. Get events, Sync events, and Notify
"""

from core.credfetcher import *
from core.eventsfetcher import *
from core.sync import *
from core.notify import *
from core.storage import *

from datetime import datetime
import pause

while True:
    now = datetime.now()
    print(now)
    # On init Storage
    trail = Storage()
    # On récupère les informations de login
    credfetcher(trail)

    # On descend le planning en JSON
    eventsfetcher(trail)
    caldavSync(trail)
    telegramNotifier(trail)
    print("         En pause")
    pause.minutes(60)
