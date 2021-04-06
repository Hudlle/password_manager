import mysql.connector
import sys
import pyperclip
import login
import crypto
import random

try:
    db = login.getConnection()
    cursor = db.cursor()
except:
    sys.exit()

QNewPassword = "INSERT INTO passwords (websiteName, password, username, eMail, telefonNumber, websiteAddress) VALUES (%s,%s,%s,%s,%s,%s)"
QChangeEntry = "INSERT INTO passwords (passwordId, websiteName, password, username, eMail, telefonNumber, websiteAddress) VALUES (%s,%s,%s,%s,%s,%s,%s)"
QDeleteEntryWebsiteName = "DELETE FROM passwords WHERE websiteName = %s"
QDeleteEntryPasswordId = "DELETE FROM passwords WHERE passwordId = %s"
QSelectWhere = "SELECT * FROM passwords WHERE websiteName = %s"
QSelectAll = "SELECT * FROM passwords"

def newEntry():
    print("--> New Password")
    websiteName = input("Website Name : ")

    cursor.execute(QSelectAll)
    for i in cursor:
        if i[1] == websiteName:
            print("Cannot create Password with the website name '" + websiteName + "'.")
            return 

    password = input("Password : ")
    password = crypto.encryptMessage(password)
    username = input("Username : ")
    eMail = input("E-Mail : ")
    telefonNumber = input("Telefon Number : ")
    websiteAddress = input("Website Address : ")

    val = (websiteName, password, username, eMail, telefonNumber, websiteAddress)
    cursor.execute(QNewPassword, val)
    db.commit()
    print("S: Command executed successfully.")

def changeEntry():
    print("--> Change Entry")
    websiteName = input("Website Name : ")

    cursor.execute(QSelectWhere, (websiteName, ))

    counter = 0
    for i in cursor:
        print("")
        printRow(i)
        print("")

        print("[1] Website Name\n[2] Password\n[3] Username\n[4] E-Mail\n[5] Telefon Number\n[6] Website Address\n[B] Back")
        answer = input("> ")
        if answer != "B":
            changeCommands[answer](i)
            print("S: Command executed successfully.")
        counter += 1

    if counter < 1:
        print("E: There is no entry with the website name : '" + websiteName + "'.")

def changeWebsiteName(row):
    print("[B] Back")
    websiteName = input("New Website Name : ")
    if websiteName == "B":
        return
    val = (row[0], websiteName, row[2], row[3], row[4], row[5], row[6])
    cursor.execute(QDeleteEntryPasswordId, (row[0], ))
    cursor.execute(QChangeEntry, val)
    db.commit()
    print("S: Command executed successfully.")
def changePassword(row):
    print("[B] Back")
    password = input("New Password : ")
    if password == "B":
        return
    password = crypto.encryptMessage(password)
    val = (row[0], row[1], password, row[3], row[4], row[5], row[6])
    cursor.execute(QDeleteEntryPasswordId, (row[0], ))
    cursor.execute(QChangeEntry, val)
    db.commit()
def changeUsername(row):
    print("[B] Back")
    username = input("New Username : ")
    if username == "B":
        return
    val = (row[0], row[1], row[2], username, row[4], row[5], row[6])
    cursor.execute(QDeleteEntryPasswordId, (row[0], ))
    cursor.execute(QChangeEntry, val)
    db.commit()
def changeEMail(row):
    print("[B] Back")
    eMail = input("New E-Mail : ")
    if eMail == "B":
        return
    val = (row[0], row[1], row[2], row[3], eMail, row[5], row[6])
    cursor.execute(QDeleteEntryPasswordId, (row[0], ))
    cursor.execute(QChangeEntry, val)
    db.commit()
def changeTelefonNumber(row):
    print("[B] Back")
    telefonNumber = input("New Telefon Number : ")
    if telefonNumber == "B":
        return
    val = (row[0], row[1], row[2], row[3], row[4], telefonNumber, row[6])
    cursor.execute(QDeleteEntryPasswordId, (row[0], ))
    cursor.execute(QChangeEntry, val)
    db.commit()
def changeWebsiteAddress(row):
    print("[B] Back")
    websiteAddress = input("New Website Address : ")
    if websiteAddress == "B":
        return
    val = (row[0], row[1], row[2], row[3], row[4], row[5], websiteAddress)
    cursor.execute(QDeleteEntryPasswordId, (row[0], ))
    cursor.execute(QChangeEntry, val)
    db.commit()
changeCommands = {
    "1" : changeWebsiteName,
    "2" : changePassword,
    "3" : changeUsername,
    "4" : changeEMail,
    "5" : changeTelefonNumber,
    "6" : changeWebsiteAddress
}

def deleteEntry():
    print("--> Delete Entry")
    websiteName = input("Website Name : ")

    cursor.execute(QSelectWhere, (websiteName, ))
    counter = 0
    for i in cursor:
        if str(i[1]) == websiteName:
            cursor.execute(QDeleteEntryWebsiteName, (websiteName, ))
            db.commit()
            counter += 1
            print("S: " + websiteName + " deleted successfully.")

    if counter < 1:
        print("E: There is no password according to the website name : '" + websiteName + "'.")

def printEntry():
    print("--> Print Entry")
    websiteName = input("Website Name : ")
    print("")

    cursor.execute(QSelectWhere, (websiteName, ))
    
    counter = 0
    for i in cursor:
        printRow(i)
        print("")
        answer = input("Copy Password To Clipboard? [y/n] : ")
        if answer == "y":
            pyperclip.copy(crypto.decryptMessage(i[2]))
            print("S: Command executed successfully.")
        counter += 1

    if counter < 1:
        print("E: There is no entry with the website name : '" + websiteName + "'.")     

def printTable():
    print("--> Print Table")
    cursor.execute(QSelectAll)
    entrys = cursor.fetchall()
    print("Total Password Count : ", cursor.rowcount, "\n")
    
    for i in entrys:
        printRow(i)
        print("")
    
    print("S: Command executed successfully.")
def printRow(row):
    print("Website Name : " + row[1])
    print("----------------------------")
    print("Password : " + crypto.decryptMessage(row[2]))
    print("Username : " + row[3])
    print("E-Mail : " + row[4])
    print("Telefon Number : " + row[5])
    print("Website Address : " + row[6])

def genPassword():
    try:
        n = int(input("How long sould the password be? : "))
    except:
        print("E: Not a number. Try again.")
        genPassword()
        return
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u", "v", "w", "x", "y", "z"]
    extra = ["!", "§", "$", "%", "&", "/", "(", ")", "=", "?", "<", ">"]

    while True:
        pw = []
        
        for i in range(n):
            pw.append(alphabet[random.randint(0, len(alphabet) - 1)])
            pw.append(extra[random.randint(0, len(extra) - 1)])
            pw.append(str(random.randint(0, 9)))
        
        while len(pw) > n:
            pw.pop()
        
        random.shuffle(pw)
        password = ''.join(pw)
        print(f"Generated Password: {password}")
        answer = input("Copy Password To Clipboard? [y/n] : ")
        if answer == "y":
            pyperclip.copy(password)
            print("S: Command executed successfully.")
            return
        else:
            answer = input("Generate again or leave? [g/l] : ")
            if answer == "g":
                continue
            else:
                return

def quitApp():
    db.commit()
    print("Bye.")
    sys.exit()

commands = {
    "1" : newEntry,
    "2" : changeEntry,
    "3" : deleteEntry,
    "4" : printEntry,
    "5" : printTable,
    "6" : genPassword,
    "Q" : quitApp,
}
def menu():
    print("\n--> Main Menu")
    print("[1] Create New Entry\n[2] Change An Existing Entry\n[3] Delete An Entry\n[4] Print An Entry\n[5] Print All Entrys\n[6] Generate A Password\n[Q] Quit\n")
    answer = input("> ")
    commands[answer]()
    menu()

menu()
