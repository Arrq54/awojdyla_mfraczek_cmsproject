from types import SimpleNamespace
import sqlite3
from flask import Flask, send_from_directory, request, session
import random
import json
import sqlite3

app = Flask(__name__)

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS data(
    username text unique,
    email text,
    password text,
    admin integer
)""")

myConnection = sqlite3.connect('cmsProject.sqlite')
app.config["Loggedin"] = 0

@app.route("/")
def main():
    return send_from_directory('client/public', 'index.html')


@app.route("/test")
def test():
    print("test dziala")
    x = '{ "name":"John", "age":30, "city":"New York"}'
    return x


@app.route("/attemptLogin", methods=['GET', 'POST'])
def attemptLogin():
    data = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    username = data.username
    password = data.password
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM data")
    records = myCursor.fetchall()
    found = False
    admin = 0
    for i in records:
        if username == i[0] and password == i[2]:
            found = True
            admin = i[3]
            app.config["Loggedin"] = 2 if admin == 1 else 1
            ####### WAZNE app.config = session, wedlug tego wyswietlamy rozne wersje strony glownej, 0 = niezalogowany, 1 = normalny user, 2 = admin
    returnAnswer = f'{{"correctData":true, "admin":{admin}}}' if found else f'{{"correctData":false, "admin":{admin}}}'
    print(returnAnswer)
    # true = user istnieje w bazie #false = nie istnieje
    return json.loads(returnAnswer)


@app.route("/register", methods=['GET', 'POST'])
def register():
    myConnection = sqlite3.connect('usersData.sqlite')
    data = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    username = data.username
    password = data.password
    email = data.email
    admin = 0
    myCursor = myConnection.cursor()
    try:
        myCursor.execute("INSERT INTO data VALUES (:username, :email, :password, :admin)", {
            'username': username,
            'email': email,
            'password': password,
            'admin': admin
        })
        myConnection.commit()
        returnAnswer = '{"correctData":true}'
    except Exception as e:
        returnAnswer = '{"correctData":false}'
    # true = success, false = error
    return json.loads(returnAnswer)


@app.route("/checkLoginStatus", methods=['GET', 'POST'])
def getUserType():
    returnAnswer = f'{{"user":{app.config["Loggedin"]}}}'
    return json.loads(returnAnswer)

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


# WEBSITE CONTENT FROM DATABASE

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS news(
    header text,
    title text,
    text_content text,
    button_text text,
    src text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS navbar_menu(
    text_content text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS ffn(
    title text,
    text_content text,
    src text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS slider(
    src text,
    label text,
    texts text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS footer(
    text_content text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS footer_company(
    company text
)""")
@app.route("/getContentFromDatabase")
def getContentFromDatabase():
    output = {}
    # navbar
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM navbar_menu")
    records =  myCursor.fetchall()
    output['navbarItems'] = records
    # slider
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM slider")
    records = [dict(row) for row in myCursor.fetchall()]
    output['slider'] = records
    # news
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM news")
    records = [dict(row) for row in myCursor.fetchall()]
    output['news'] = records

    # ffn
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM ffn")
    records = [dict(row) for row in myCursor.fetchall()]
    output['firstFeaturetteNews'] = records

    # footer
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM footer")
    records = myCursor.fetchall()
    output['footer'] = {}
    output['footer']['links'] = records

    # footer company
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM footer_company")
    records = myCursor.fetchall()
    output['footer']['company'] = records

    return json.dumps(output)

@app.route("/logut")
def logout():
    app.config["Loggedin"] = 0
    returnAnswer = f'{{"user":{app.config["Loggedin"]}}}'
    return json.loads(returnAnswer)

if __name__ == "__main__":
    app.run(debug=True)
