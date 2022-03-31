from types import SimpleNamespace
import sqlite3
from flask import Flask, send_from_directory, request
import random
import json

app = Flask(__name__)

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS data(
    username text unique,
    email text,
    password text,
    admin integer
)""")

@app.route("/")
def main():
    return send_from_directory('client/public', 'index.html')


@app.route("/test")
def test():
    print("test dziala")
    x = '{ "name":"John", "age":30, "city":"New York"}'
    return json.loads(x)


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
    admin = 0;
    for i in records:
        if username == i[0] and password == i[2]:
            found = True
            admin = i[3]
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


@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


if __name__ == "__main__":
    app.run(debug=True)
