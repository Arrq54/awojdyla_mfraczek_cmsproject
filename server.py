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
    id INTEGER PRIMARY KEY,
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
    records = myCursor.fetchall()
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
    myCursor.execute("SELECT * FROM slider")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


app.config['UPLOAD_FOLDER'] = 'client/public/images'
app.config['IMAGES_LOCATION'] = "../../images/"
app.config['DEFAULT_SLIDER_IMAGE_PATH'] = "../../images/sliderPlaceholder1.png"

@app.route("/uploadSlider", methods=['GET', 'POST'])
def uploadSlider():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *,oid FROM slider")
    records = [dict(row) for row in myCursor.fetchall()]
    htmlSrc = {}
    for i in request.files:
        file = request.files[i]
        if file.filename != '':
            filename = secure_filename(file.filename)
            path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
            file.save(os.path.join(path, filename))
            htmlSrc[file.name] = f"../../images/{filename}"
    print(htmlSrc)

    print(request.form)
    print(request.files)
    for i in range(0,int(request.form['length'])):
        if(i>len(records)-1):
            myCursor = myConnection.cursor()
            sqlLine = ""
            if (request.files[f'sliderFile{i}'] == None or request.files[f'sliderFile{i}'].filename == ""):
                sqlLine = f"INSERT INTO slider (src,label,texts) VALUES('{app.config['DEFAULT_SLIDER_IMAGE_PATH']}','{request.form[f'sliderLabel{i}']}','{request.form[f'sliderText{i}']}')"
            else:
                sqlLine = f"INSERT INTO slider (src,label,texts) VALUES('{htmlSrc[i]}','{request.form[f'sliderLabel{i}']}','{request.form[f'sliderText{i}']}')"
            myCursor.execute()
            myConnection.commit(sqlLine)
            myConnection.close()
            print(request.form[f'sliderText{i}'])
        else:
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute(f"UPDATE slider SET")
            myConnection.commit()
            myConnection.close()







    # myConnection = sqlite3.connect('usersData.sqlite')
    # myCursor = myConnection.cursor()
    # myCursor.execute(f"DELETE FROM slider")
    # myConnection.commit()
    # myConnection.close()
    # for i in range(0,int((len(request.form)-1)/2)) :
    #     if(request.files[f'sliderFile{i}'].filename != ""):
    #         myConnection = sqlite3.connect('usersData.sqlite')
    #         myCursor = myConnection.cursor()
    #         myCursor.execute(f"INSERT INTO slider (src,label,texts) VALUES('{htmlSrc[f'sliderFile{i}']}','{request.form[i]['label']}','{request.form[i]['texts']}')")
    #         myConnection.commit()
    #         myConnection.close()
    #     else:
    #         if(i>len(records)-1):
    #             myConnection = sqlite3.connect('usersData.sqlite')
    #             myCursor = myConnection.cursor()
    #             myCursor.execute(f"INSERT INTO slider (src,label,texts) VALUES('../../images/sliderPlaceholder1.png ','{request.form[i]['label']}','{request.form[i]['texts']}')")
    #             myConnection.commit()
    #             myConnection.close()
    #         else:
    #             myConnection = sqlite3.connect('usersData.sqlite')
    #             myCursor = myConnection.cursor()
    #             myCursor.execute(
    #                 f"INSERT INTO slider (src,label,texts) VALUES('{records[i]['src']}','{records[i]['label']}','{records[i]['texts']}')")
    #             myConnection.commit()
    #             myConnection.close()



    return redirect("/#/configurationuser")


if __name__ == "__main__":
    app.run(debug=True)
