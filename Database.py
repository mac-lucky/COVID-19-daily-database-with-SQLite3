import sqlite3
import requests
import pandas as pd
import os
import datetime
import sys

dateNow = datetime.datetime.now()
dateNowStr = dateNow.strftime("%d-%m-%Y ")

conn=sqlite3.connect("./ranking.db")
pd.set_option('display.max_rows', None)

compareDateNew = datetime.date.today()

c = conn.cursor()

def createTableCorona():
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS Corona (Date TEXT, Country TEXT, Today_Cases INTEGER, Today_Deaths INTEGER)")
  conn.commit()
  conn.close()

def createTableSaveVar():
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS SaveVar (String TEXT, Variable INTEGER)")
  conn.commit()
  conn.close()

def insertVar(lastUpdate, isUpdated):
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  columnValues = (lastUpdate, isUpdated)
  cur.execute("INSERT OR REPLACE INTO SaveVar VALUES(?,?)", columnValues)
  conn.commit()
  conn.close()

def updateVar(lastUpdate, isUpdated):
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  cur.execute("UPDATE SaveVar SET String=?, Variable=?", (lastUpdate, isUpdated))
  conn.commit()
  conn.close()

def viewVar():
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  cur.execute("SELECT Variable FROM SaveVar")
  global upToDate
  upToDate = cur.fetchone()

def viewStr():
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  cur.execute("SELECT String FROM SaveVar")
  global dateUpdate
  dateUpdate = cur.fetchone()


def update(country, cases, deaths):
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  columnValues = (country, cases, deaths, country, dateNowStr)
  cur.executemany("UPDATE Corona SET Country=?, Today_Cases=?, Today_Deaths=? WHERE Country = ? AND Date = ?" , (columnValues,))
  conn.commit()
  conn.close()


def insertCorona(dateNowStr, country, cases, deaths):
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  columnValues = (dateNowStr, country, cases, deaths)
  cur.execute("INSERT INTO Corona VALUES(?,?,?,?)", columnValues)
  conn.commit() 
  conn.close()

def cls():
    os.system('#cls' if os.name == 'nt' else 'clear')

def view():
  conn=sqlite3.connect("./ranking.db")
  cur=conn.cursor()
  cur.execute("SELECT * FROM Corona ORDER BY country")
  dataCases = cur.fetchall()
  conn.close()
  return dataCases

def delete():
    conn=sqlite3.connect("./ranking.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM Corona")
    conn.commit()
    conn.close()

def getData():
  coronaData=requests.get('https://coronavirus-19-api.herokuapp.com/countries')
  db = coronaData.json()
  for dr in range(0, len(db) - 1 ):
    cases = db[dr]["todayCases"]
    country = db[dr]['country']
    death = db[dr]['todayDeaths']
    insertCorona(dateNowStr, country, cases, death)

def getDataUpdate():
  coronaData=requests.get('https://coronavirus-19-api.herokuapp.com/countries')
  db = coronaData.json()
  for dr in range(0, len(db) - 1 ):
    cases = db[dr]["todayCases"]
    country = db[dr]['country']
    death = db[dr]['todayDeaths']
    update(country, cases, death)

def checkDate():
  viewStr()
  s = dateUpdate[0]
  s = s.split('-')
  for i in range(0, len(s)): 
    s[i] = int(s[i]) 
  global compareDateOld
  compareDateOld = datetime.date(s[2], s[1], s[0])


c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Corona' ''')
if c.fetchone()[0]==0 :
  cls()
  print("""
       1. Update data of current cases and create database
       2. Exit
       """)
  option = input("Choose number, what would you like to do ")
  if option == "1":
    cls()
    createTableCorona()
    createTableSaveVar()
    print("Request for data")
    getData()
    print("Data downloaded")
    upToDate = 1
    dateUpdate = dateNowStr
    insertVar(dateUpdate, upToDate)
  elif option == "2":
    print("\n Goodbye")
    sys.exit() 
  else:
    print("\n Not Valid Choice Try again") 


ans=True
while ans:
    cls()
    checkDate()
    if compareDateOld < compareDateNew:
      print("Last update: ", compareDateOld)
      print("Todays date: ", compareDateNew)
      ask = input("1. Would you like to update database to this day Y/N ")
      if ask == 'Y' or 'y':
        cls()
        print("Data update started")
        getData()
        upToDate = 1
        dateUpdate = dateNowStr
        updateVar(dateUpdate, upToDate)
      else:
        cls()
        print("Update canceled")
    print ("""
    1.Update
    2.View
    3.Exit/Quit
    """)
    ans=input("Choose number, what would you like to do ") 
    if ans=="1":
      cls()
      if os.path.isfile('./ranking.db'):
        print("Request for newer data")
        getDataUpdate()
        print("Data updated")
        dateUpdate = dateNowStr
        upToDate = 1
        updateVar(dateUpdate, upToDate)
      else:  
        createTableCorona()
        print("Request for data")
        getData()
        print("Data downloaded")
        dateUpdate = dateNowStr
        upToDate = 1
        updateVar(dateUpdate, upToDate)
    elif ans=="2":
      cls()
      print(pd.read_sql_query("SELECT * FROM Corona ORDER BY date, country", conn))
      print(" ")
      print("Date:", dateNowStr)
      print(" ")
      input("Press any button to go back") 
    elif ans=="3":
      print("\n Goodbye")
      break 
    else:
      print("\n Not Valid Choice Try again") 




