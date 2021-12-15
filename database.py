import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "botuser",
    password = "Bendeguz01",
    database = "vikbot"
)

mycursor = mydb.cursor()

print(mydb)