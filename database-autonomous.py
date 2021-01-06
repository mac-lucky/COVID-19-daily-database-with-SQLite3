import sqlite3
import requests
import os
import datetime
import sys
import time

dateNow = datetime.datetime.now()
dateNowStr = dateNow.strftime("%d-%m-%Y ")

conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")

compareDateNew = datetime.date.today()

c = conn.cursor()

def createTableCorona():
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS Corona (Date TEXT, Country TEXT, Today_Cases INTEGER, Today_Deaths INTEGER)")
  conn.commit()
  conn.close()

def createTableSaveVar():
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS SaveVar (String TEXT, Variable INTEGER)")
  conn.commit()
  conn.close()

def insertVar(lastUpdate, isUpdated):
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  columnValues = (lastUpdate, isUpdated)
  cur.execute("INSERT OR REPLACE INTO SaveVar VALUES(?,?)", columnValues)
  conn.commit()
  conn.close()

def updateVar(lastUpdate, isUpdated):
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  cur.execute("UPDATE SaveVar SET String=?, Variable=?", (lastUpdate, isUpdated))
  conn.commit()
  conn.close()

def viewVar():
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  cur.execute("SELECT Variable FROM SaveVar")
  global upToDate
  upToDate = cur.fetchone()

def viewStr():
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  cur.execute("SELECT String FROM SaveVar")
  global dateUpdate
  dateUpdate = cur.fetchone()


def update(country, cases, deaths):
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  columnValues = (country, cases, deaths, country, dateNowStr)
  cur.executemany("UPDATE Corona SET Country=?, Today_Cases=?, Today_Deaths=? WHERE Country = ? AND Date = ?" , (columnValues,))
  conn.commit()
  conn.close()


def insertCorona(dateNowStr, country, cases, deaths):
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  columnValues = (dateNowStr, country, cases, deaths)
  cur.execute("INSERT INTO Corona VALUES(?,?,?,?)", columnValues)
  conn.commit() 
  conn.close()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def view():
  conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
  cur=conn.cursor()
  cur.execute("SELECT * FROM Corona ORDER BY country")
  dataCases = cur.fetchall()
  conn.close()
  return dataCases

def delete():
    conn=sqlite3.connect("/home/pi/Downloads/COVID/ranking.db")
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

while 1:
  c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Corona' ''')
  if c.fetchone()[0]==0 :
    cls()
    createTableCorona()
    createTableSaveVar()
    print("Request for data")
    getData()
    print("Data downloaded")
    upToDate = 1
    dateUpdate = dateNowStr
    insertVar(dateUpdate, upToDate)
  else:
    checkDate()
    if compareDateOld < compareDateNew:
      print("Last update: ", compareDateOld)
      print("Todays date: ", compareDateNew)
      print("Data update started")
      getData()
      upToDate = 1
      dateUpdate = dateNowStr
      updateVar(dateUpdate, upToDate)
      sys.exit()
    else:
      print("Request for newer data")
      getDataUpdate()
      print("Data updated")
      dateUpdate = dateNowStr
      upToDate = 1
      updateVar(dateUpdate, upToDate)
      sys.exit()
