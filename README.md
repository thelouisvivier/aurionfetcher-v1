# AurionFetcher

Programme en python permettant de télécharger le planning d'Aurion, synchroniser les événements sur un serveur CalDav, et notifier l'utilisateur sur telegram en cas de changements.  

**thelouisvivier - 2019**  

---

Ce programme est basé sur le travail de Bdeliers disponible à l'adresse suivante : https://github.com/BDeliers/Python-Planning-Aurion

---

Pour utiliser ce programme, il vous faudra installer Python 3 et Pip3 ainsi que Firefox

Sous linux :

```shell
    sudo apt-get install python3 python3-dev python3-pip firefox
```

Ensuite, quelques modules sont indispensables :

```shell
    sudo pip3 install selenium lxml requests caldav ics uuid python-telegram-bot
```

Enfin, il vous faudra télécharger le driver qui correspond à votre navigateur et le désarchiver dans le répertoire qui contient votre script python (ou bien l'ajouter au PATH).  
Pour Firefox : [geckodriver](https://github.com/mozilla/geckodriver/releases)


Ajoutez ensuite vos infos dans le config.py.


Une fois que tout est prêt, vous pouvez lancer le programme de la manière suivante :

```shell
    python3 runner.py
```

---

Pour installer via docker, l'image est disponible ici https://hub.docker.com/r/thelouisvivier/aurionfetcher/
Montez le dossier /config vers l'emplacement local de votre fichier config.py
Voilà!
