# Python + Processing-achtige omgeving (portable, voor les)

## Doel

Deze repository bevat een **didactische programmeeromgeving voor beginners**.
Leerlingen kunnen hiermee **Processing-achtig programmeren in Python** zonder iets te installeren.

Kenmerken:

* werkt **volledig vanaf een USB-stick**
* **geen installatie** nodig
* **geen internet** nodig tijdens de les
* syntax lijkt sterk op **Processing**
* geschikt voor eerste lessen **computational thinking**

Leerlingen programmeren bijvoorbeeld zo:

```python
from processing import *

x = 0

def setup():
    size(800,500)

def draw():
    global x

    background(255)
    rect(x,200,100,100)

    x += 1

run()
```

Het programma draait dan 60× per seconde zoals in Processing.

---

# Didactisch idee

De structuur volgt drie eenvoudige concepten:

**STATE → LOGIC → VIEW**

| concept | betekenis                                                |
| ------- | -------------------------------------------------------- |
| state   | variabelen die de toestand van het programma beschrijven |
| logic   | regels die de toestand veranderen                        |
| view    | wat er op het scherm getekend wordt                      |

Dit helpt leerlingen om **computational thinking** te ontwikkelen voordat ze complexere frameworks gebruiken.

---

# Repository structuur

```
repo/
│
├─ voorbeeld.py
├─ auto.py
│
├─ processing/
│   ├─ __init__.py
│   └─ processing.py
│
├─ python/
│   └─ python313._pth
│
├─ .gitignore
└─ README.md
```

Belangrijk:

* `processing/` bevat een kleine **wrapper rond pygame**
* `python/` bevat **alleen configuratie voor de portable Python**
* de **Python runtime zelf staat niet in Git**

---

# Wat er op de USB-stick moet staan

Op de stick moet uiteindelijk dit staan:

```
USB/
│
├─ voorbeeld.py
├─ auto.py
│
├─ processing/
│
└─ python/
   ├─ python.exe
   ├─ python313.dll
   ├─ python313.zip
   ├─ python313._pth
   └─ Lib/
      └─ site-packages/
         └─ pygame/
```

De runtime staat dus in de map **`python/`**.

---

# Hoe maak je de USB-stick

## 1. Download Python (embeddable)

Download de **Windows embeddable version** van Python:

https://www.python.org/downloads/windows/

Kies bijvoorbeeld:

```
python-3.13.x-embed-amd64.zip
```

Pak deze uit in:

```
python/
```

---

## 2. Installeer pygame in de portable Python

Op een computer met internet:

```
python -m pip install pygame --target python/Lib/site-packages
```

Daarmee wordt pygame lokaal in de stick geplaatst.

---

## 3. Zet deze repository op de stick

Kopieer de inhoud van deze repo naar de stick zodat je krijgt:

```
USB/
  voorbeeld.py
  processing/
  python/
```

---

# Programma starten

Open een terminal in de root van de stick:

```
.\python\python.exe voorbeeld.py
```

Dit werkt ook zonder internet en zonder installatie.

---

# Waarom deze aanpak

Veel onderwijsomgevingen blokkeren:

* installaties
* executables
* package managers

Door Python **portable op een stick** te zetten:

* blijft de omgeving **controleerbaar**
* werkt alles **offline**
* kunnen leerlingen **direct programmeren**

---

# Voorbeeldopdracht

Laat leerlingen een bewegend object maken:

```python
from processing import *

x = 0

def setup():
    size(800,500)

def draw():
    global x

    background(255)
    circle(x,250,50)

    x += 2

run()
```

Concepten:

* variabelen
* herhaling
* grafische feedback

---

# Mogelijke uitbreidingen

Later kunnen leerlingen toevoegen:

* toetsenbordinput
* meerdere objecten
* simpele games
* simulaties

Omdat alles gewoon **Python** is, kunnen ze later eenvoudig doorgroeien naar:

* pygame
* matplotlib
* numpy
* webontwikkeling

---

# Samenvatting

Dit project biedt:

* een **lichte Processing-achtige omgeving**
* **Python als programmeertaal**
* **geen installatie nodig**
* geschikt voor **introductie programmeren**

Het doel is om leerlingen **snel visuele feedback te geven**, zodat programmeren meteen leuk en begrijpelijk wordt.
