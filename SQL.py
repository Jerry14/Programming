import sqlite3
import random
import qrcode
import requests
import os
import os.path
from tkinter import *

f = os.path.isfile("Reizigers.db")
conn = sqlite3.connect('Reizigers.db')
c = conn.cursor()
random_number = random.randint(10000, 99000)

def tableCreate():
    if f == False:
        c.execute("CREATE TABLE ReizigersDB(ID INT, Naam TEXT, OVnummer INT, Beginstation TEXT, Eindstation TEXT)")
    elif f == True:
        print("")


def dataEntry():
    with conn:
        c.execute("INSERT INTO ReizigersDB (ID, Naam, OVnummer, Beginstation, Eindstation) VALUES (?, ?, ?, ?, ?)",
                  (random_number, gegevens[0], gegevens[1], gegevens[2], gegevens[3]))


tableCreate()




def nsAPI():
    """
    Doormiddel van deze functie worden de stations uit nsAPI gehaald.
    Deze stations worden later in de functie controleerstations() gebruikt
    om de input van de gebruiker te controleren
    """
    auth_details = ("hjr.tielemans@gmail.com", "sz3XpDnQ5EVcA8Gg4FhuWICzhJgmMOnehAIoElLW3iVP1wyJ5p8OuQ")
    response = requests.get('http://webservices.ns.nl/ns-api-stations-v2',
                            auth=auth_details)
    global stations
    stations = response.text


nsAPI()


def welkomprint():
    print("Welkom bij de NS. \nVoer nu onderstaande informatie in om verder te gaan.")


welkomprint()


def input_integer(prompt):
    """
    De input moet bestaan uit enkel getallen, als dit niet het geval is wordt dit aangegeven.
    De functie zal dan vragen om een nieuwe input.
    """
    invoer = input(prompt)
    if invoer and invoer.isdigit():
        return int(invoer)
    else:
        print("De invoer is niet correct. Probeer het opnieuw.")
        return input_integer(prompt)


def input_character(prompt):
    """
    De input moet bestaan uit enkel letters, als dit niet het geval is wordt dit aangegeven.
    De functie zal dan vragen om een nieuwe input.
    """
    invoer = input(prompt)
    if invoer and invoer.isalpha():
        return str(invoer)
    else:
        print("De invoer is niet correct. Probeer het opnieuw.")
        return input_character(prompt)


def controleerstations():
    """
    In deze functie worden de:
    naam, ovnummer, beginstation en eindstation ingevoerd door de gebruiker.
    Bij ovnummer is alleen een input geldig van nummers
    Daarnaast moet het begin en eindstation niet hetzelfde zijn en moeten beide in nsAPI voorkomen
    Al deze bovenstaande gegevens worden opgeslagen in gegevens

    """
    naam = input("Voer uw naam in: ")
    ovnummer = input_integer("Voer uw ov-chipkaartnummer in: ")
    beginstation = input_character("Voer uw beginstation in: ")
    while beginstation not in stations:
        print("Het beginstation is niet bekend.")
        beginstation = input_character("Voer uw beginstation in: ")
    eindstation = input("Voer uw eindstation in: ")
    while eindstation not in stations:
        print("Het eindstation is niet bekend.")
        eindstation = input("Voer uw eindstation in: ")
    while beginstation == eindstation:
        print("Het eindstation mag niet hetzelfde zijn als het beginstation zijn.")
        eindstation = input_character("Voer uw eindstation in: ")
    global gegevens
    gegevens = naam, ovnummer, beginstation, eindstation
    dataEntry()

controleerstations()


def generateQR():
    """
    Deze functie genereert een QR-code op basis van de bovenstaande code(controleerstations())
    Dit gebeurt op basis van de input van de gebruiker. De input is opgeslagen in gegevens.
    """
    global gegevens
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=10,
                       border=4,
    )
    qr.add_data(gegevens)
    qr.make(fit=True)
    return(qr.get_matrix())
    img = qr.make_image()
    img.show()
generateQR()

def invoer_incheckzuil():
    global e1
    master = Tk()
    Label(master, text="Voer ov-chipkaartnummer in").grid(row=0)
    e1 = Entry(master)
    e1.grid(row=0, column=1)
    Button(master, text='Invoeren', command=master.quit).grid(row=0, column=4 , sticky=W, pady=20)
    mainloop()
    Z = e1.get()
    return Z
invoer_incheckzuil()

def vergelijk_database():
    global Z
    global conn
    # for row in conn:
    #     if f == row:
    #         print( row[0])
    #     else:
    #         print("werkt niet")
    #
    with conn:

        cur = conn.cursor()
        cur.execute("SELECT * FROM ReizigersDB")

    while True:
        row = cur.fetchone()
        if row == None:
            break

        print(row[0], row[1], row[2])


vergelijk_database()

