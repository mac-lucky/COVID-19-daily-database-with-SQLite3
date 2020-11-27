import sqlite3
import requests



def createTable():
    conn=sqlite3.connect("ranking.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Ranking (Code INTEGER, Model TEXT, Price INTEGER, Points INTEGER, Year INTEGER)")
    conn.commit()
    conn.close()

def insert(Code, Model, Price, Points, Year):
    conn=sqlite3.connect("ranking.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO Ranking VALUES(?,?,?,?,?)", (Code, Model, Price, Points, Year))
    conn.commit()
    conn.close()

    
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
    cur.execute("SELECT * FROM Corona")
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
    


createTableCorona()
delete()
getData()
print(view())








