import os
import urllib
from types import SimpleNamespace
import sqlite3
from flask import Flask, send_from_directory, request, redirect
import random
import json
import sqlite3
from werkzeug.utils import secure_filename

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
    src text,
    idnews INTEGER PRIMARY KEY,
    content text
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
    id INTEGER PRIMARY KEY,
    src text,
    label text,
    texts text,
    sliderOrder integer
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

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS sectionOrder(
    name text,
    sectionOrder integer
)""")


@app.route("/getContentFromDatabase")
def getContentFromDatabase():
    output = {}
    # navbar
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM navbar_menu")
    records = myCursor.fetchall()
    output['navbarItems'] = records
    # slider
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM slider ORDER BY sliderOrder")
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

    res = []

    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM sectionOrder ORDER BY sectionOrder")
    records = [dict(row) for row in myCursor.fetchall()]

    obj = {}
    obj['type'] = 'navbarItems'
    obj['content'] = output['navbarItems']
    res.append(obj)
    for i in records:
        obj = {}
        obj['type'] = i['name']
        obj['content'] = output[i['name']]
        res.append(obj)
    obj = {}
    obj['type'] = 'footer'
    obj['content'] = output['footer']
    res.append(obj)
    return json.dumps(res)


@app.route("/logout")
def logout():
    print("logout")
    app.config["Loggedin"] = 0
    returnAnswer = f'{{"user":{app.config["Loggedin"]}}}'
    return json.loads(returnAnswer)


@app.route("/getSlider")
def getSlider():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM slider ORDER BY sliderOrder")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/getUsers")
def getUsers():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM data")
    records = [dict(row) for row in myCursor.fetchall()]
    print(records)
    return json.dumps(records)


app.config['UPLOAD_FOLDER'] = 'client/public/images'
app.config['IMAGES_LOCATION'] = "../../images/"
app.config['DEFAULT_SLIDER_IMAGE_PATH'] = "../../images/sliderPlaceholder1.png"


@app.route("/uploadSlider", methods=['GET', 'POST'])
def uploadSlider():
    htmlSrc = {}
    for i in request.files:
        file = request.files[i]
        if file.filename != '':
            filename = secure_filename(file.filename)
            path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
            file.save(os.path.join(path, filename))
            htmlSrc[file.name] = f"../../images/{filename}"
    newRecords = []
    for i in range(0, int(request.form['length'])):
        newRecord = {}
        newRecord['id'] = i + 1
        if (f'sliderFile{i}' in htmlSrc):
            newRecord['src'] = htmlSrc[f'sliderFile{i}']
        else:
            newRecord['src'] = request.form[f'sliderFileName{i}']
        newRecord['label'] = request.form[f'sliderLabel{i}']
        newRecord['texts'] = request.form[f'sliderText{i}']
        newRecord['sliderOrder'] = request.form[f'sliderOrder{i}']
        newRecords.append(newRecord)
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM slider")
    myConnection.commit()
    myConnection.close()
    for i in newRecords:
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(
            f"INSERT INTO slider (src,label,texts,sliderOrder) VALUES('{i['src']}','{i['label']}','{i['texts']}',{i['sliderOrder']})")
        myConnection.commit()
        myConnection.close()
    return redirect("/#/configurationuser")


@app.route("/getSettings", methods=['GET', 'POST'])
def getSettings():
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    with open(path, 'r+') as f:
        temp = json.dumps(f.read())
        return json.loads(temp)


@app.route("/saveColors", methods=['GET', 'POST'])
def saveColors():
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    content = {}
    with open(path, 'r') as f:
        content = json.loads(f.read())
    with open(path, 'w') as f: f.close()
    with open(path, 'w') as f:
        object = {}
        object['colors'] = request.get_json()
        object['blocks'] = content['blocks']
        object['sliderTimeSpan'] = content['sliderTimeSpan']
        object['fonts'] = content['fonts']
        f.write(json.dumps(object))
    return redirect("/#/configurationuser")


@app.route("/changeOrder", methods=['GET', 'POST'])
def changeOrder():
    data = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    body = data.body
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM slider")
    myConnection.commit()
    myConnection.close()
    for i in body:
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(
            f"INSERT INTO slider (src,label,texts,sliderOrder) VALUES('{i.src}','{i.label}','{i.texts}',{i.sliderOrder})")
        myConnection.commit()
        myConnection.close()
    return redirect("/#/configurationuser")


@app.route("/saveFont", methods=['GET', 'POST'])
def saveFont():
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    font = request.get_json()
    content = {}
    with open(path, 'r') as f:
        content = json.loads(f.read())
    with open(path, 'w') as f: f.close()
    with open(path, 'w') as f:
        object = {}
        object['colors'] = content['colors']
        object['blocks'] = content['blocks']
        object['fonts'] = font['fontFamily']
        object['sliderTimeSpan'] = content['sliderTimeSpan']
        print(json.dumps(object))

        f.write(json.dumps(object))
    return redirect("/#/configurationuser")


@app.route("/changeBlockSettings", methods=['GET', 'POST'])
def changeBlockSettings():
    print(request.get_json()['id'])
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    font = request.get_json()
    content = {}
    with open(path, 'r') as f:
        content = json.loads(f.read())
    with open(path, 'w') as f: f.close()
    with open(path, 'w') as f:
        object = {}
        object['colors'] = content['colors']
        object['fonts'] = content['fonts']
        object['sliderTimeSpan'] = content['sliderTimeSpan']
        tempSettings = content['blocks']
        tempSettings[request.get_json()['id']] = 1 if request.get_json()['value'] == True else 0
        object['blocks'] = tempSettings
        print(json.dumps(object))
        f.write(json.dumps(object))
    return redirect("/#/configurationuser")

@app.route("/deleteUser", methods=['GET', 'POST'])
def deleteUser():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute('DELETE FROM data WHERE oid=' + str(request.get_json()))
    myConnection.commit()
    myConnection.close()
    return True


@app.route("/editUser", methods=['GET', 'POST'])
def editUser():
    data = request.get_json()
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("""UPDATE data SET
                    username = :username,
                    email = :email,
                    password =  :password

                    WHERE oid = :oid""",
                     {
                         'username': data["username"],
                         'email': data["email"],
                         'password': data["password"],
                         'oid': data["id"]
                     })
    myConnection.commit()
    myConnection.close()
    return True


@app.route("/getCurrentSectionOrder", methods=['GET', 'POST'])
def getCurrentSectionOrder():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM sectionOrder ORDER BY sectionOrder")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/changeOrderOfSections", methods=['GET', 'POST'])
def changeOrderOfSections():
    data = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    body = data.body
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM sectionOrder")
    myConnection.commit()
    myConnection.close()
    for i in body:
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(
            f"INSERT INTO sectionOrder (name, sectionOrder) VALUES('{i.name}','{i.sectionOrder}')")
        myConnection.commit()
        myConnection.close()
    return redirect("/#/configurationuser")

@app.route("/updateSliderTime", methods=['GET', 'POST'])
def updateSliderTime():
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    data = request.get_json()
    content = {}
    with open(path, 'r') as f:
        content = json.loads(f.read())
    with open(path, 'w') as f: f.close()
    with open(path, 'w') as f:
        object = {}
        object['colors'] = content['colors']
        object['fonts'] = content['fonts']
        object['blocks'] = content['blocks']
        object['sliderTimeSpan'] = data['body']
        f.write(json.dumps(object))
    return redirect("/#/configurationuser")



@app.route("/getArticleById", methods=['GET', 'POST'])
def getArticleById():
    req = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute(f"SELECT * FROM news WHERE idnews={req.body}")
    records = [dict(row) for row in myCursor.fetchall()]
    print(records)
    return json.dumps(records)


if __name__ == "__main__":
    app.run(debug=True)