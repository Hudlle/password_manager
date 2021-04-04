import mysql.connector

connection = None

def getConnection():
    global connection

    username = input("User : ")
    password = input("Password : ")

    try:
        if not connection:
            connection = mysql.connector.connect(
                host='localhost',
                user=username,
                password=password,
                database='passwords'
            )
        print("Access granted. Welcome " + username + ".")
        return connection
    except:
        print("Access denied. Wrong username or password.")