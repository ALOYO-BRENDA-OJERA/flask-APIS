import mysql.connector

try:
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your actual password
    database="flaskapi"
  )
  print("Connection successful!")
except mysql.connector.Error as err:
  print("Connection failed:", err)

mydb.close()  # Close the connection
