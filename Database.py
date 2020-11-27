import sqlite3
import requests
import pandas as pd
import os


conn=sqlite3.connect("ranking.db")
pd.set_option('display.max_rows', None)
    
def createTableCorona():
    conn=sqlite3.connect("ranking.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Corona (Country TEXT, Today_Cases INTEGER, Today_Deaths INTEGER)")
    conn.commit()
    conn.close()
    

def insertCorona(country, todayCases, todayDeaths):
    conn=sqlite3.connect("ranking.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO Corona VALUES(?,?,?)", (country, todayCases, todayDeaths))
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect("ranking.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Corona ORDER BY country")
    dataCases = cur.fetchall()
    conn.close()
    return dataCases

def delete():
    conn=sqlite3.connect("ranking.db")
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
        insertCorona(country, cases, death)
    
ans=True
while ans:
    print ("""
    1.Update
    2.View
    3.Exit/Quit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1":
      if os.path.isfile('.\ranking.db'):
        print("Deleting old records")
        delete()
        print("Request for newer data")
        getData()
        print("Data updated")
      else:  
        createTableCorona()
        print("Request for data")
        getData()
        print("Data downloaded")
      
    elif ans=="2":
      print(pd.read_sql_query("SELECT * FROM Corona", conn))
      input("Press any button to go back") 
    elif ans=="3":
      print("\n Goodbye")
      break 
    elif ans !="":
      print("\n Not Valid Choice Try again") 




