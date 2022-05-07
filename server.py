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
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM data WHERE username='" + request.get_json()["username"] +"'")
    answer = myCursor.fetchall()[0][3]
    returnAnswer = f'{{"permission":{answer}}}'
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
    content text,
    category text,
    newsOrder number,
    pictures text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS navbar_menu(
    text_content text,
    id INTEGER PRIMARY KEY,
    content text
)""")

myConnection = sqlite3.connect('usersData.sqlite')
myCursor = myConnection.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS comments(
    user text,
    content text,
    time text,
    articleid integer
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
    text_content text,
    id INTEGER PRIMARY KEY,
    content text
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
    myCursor.execute("SELECT * FROM news ORDER BY newsOrder")
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
app.config['UPLOAD_FOLDER_ARTICLES'] = 'client/public/images/articles'
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
                    password =  :password,
                    admin = :admin

                    WHERE oid = :oid""",
                     {
                         'username': data["username"],
                         'email': data["email"],
                         'password': data["password"],
                         'admin': data["admin"],
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


@app.route("/getNewsToEdit", methods=['GET', 'POST'])
def getNewsToEdit():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute(f"SELECT * FROM news")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/updateArticles", methods=['GET', 'POST'])
def updateArticles():
    newRecords = []
    for i in range(0, int(request.form['length'])):
        pictures = []
        filelist = request.files.getlist(f'articleImages{i}')
        for file in filelist:
            if file.filename != '':
                filename = secure_filename(file.filename)
                path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER_ARTICLES"])
                file.save(os.path.join(path, filename))
                pictures.append(f"../../images/articles/{filename}")

        pictures = json.dumps(pictures)
        header = request.form[f'articleHeader{i}']
        title = request.form[f'articleTitle{i}']
        summary = request.form[f'articleSummary{i}']
        button_text = request.form[f'articleButtonText{i}']
        text = request.form[f'articleText{i}']
        category = request.form[f'category{i}']
        newsOrder = request.form[f'newsOrder{i}']
        if (category == "other"):
            category = request.form[f'otherCategory{i}']
        newRecord = {}
        newRecord['header'] = header
        newRecord['title'] = title
        newRecord['text_content'] = summary
        newRecord['button_text'] = button_text
        newRecord['content'] = text
        newRecord['category'] = category
        newRecord['newsOrder'] = newsOrder
        newRecord['previousPictures'] = request.form[f'articleFiles{i}']
        print(newRecord['previousPictures'])
        if (pictures != "[]"):
            newRecord['pictures'] = pictures
        else:
            newRecord['pictures'] = "x"
        newRecords.append(newRecord)
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM news")
    myConnection.commit()
    myConnection.close()
    for i in newRecords:
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        if (i['pictures'] == "x"):
            myCursor.execute(
                "INSERT INTO NEWS (header,title,text_content,button_text,content,category, newsOrder, pictures) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (i['header'], i['title'], i['text_content'], i['button_text'], i['content'], i['category'],
                 i['newsOrder'], i['previousPictures']))
        else:
            myCursor.execute(
                "INSERT INTO NEWS (header,title,text_content,button_text,content,category, newsOrder, pictures) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (i['header'], i['title'], i['text_content'], i['button_text'], i['content'], i['category'],
                 i['newsOrder'], i['pictures']))
        myConnection.commit()
        myConnection.close()
    return redirect("/#/configurationuser")


@app.route("/getArticles")
def getArticles():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM news ORDER BY newsOrder")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/changeOrderOfArticles", methods=['GET', 'POST'])
def changeOrderOfArticles():
    req = request.get_json()
    body = req['body']
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM news")
    myConnection.commit()
    myConnection.close()
    for i in body:
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(
            "INSERT INTO NEWS (header,title,text_content,button_text,content,category, newsOrder) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (i['header'], i['title'], i['text_content'], i['button_text'], i['content'], i['category'], i['newsOrder']))
        myConnection.commit()
        myConnection.close()
    return redirect("/#/configurationuser")


@app.route("/getffn")
def getffn():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM ffn")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/uploadFfn", methods=['GET', 'POST'])
def uploadFfn():
    files = request.files
    file = files['photo']
    texts = request.form
    title = texts['title']
    text_content = texts['summary']
    fName = ""
    if file.filename != '':
        filename = secure_filename(file.filename)
        path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
        file.save(os.path.join(path, filename))
        fName = f"../../images/{filename}"
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(f"UPDATE ffn SET title=?, text_content=?, src=?", (title, text_content, fName))
        myConnection.commit()
        myConnection.close()
        return redirect("/#/configurationuser")
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"UPDATE ffn SET title=?, text_content=?", (title, text_content))
    myConnection.commit()
    myConnection.close()
    return redirect("/#/configurationuser")


@app.route("/getMenuItems")
def getMenuItems():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM navbar_menu")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/getMenuItemById", methods=['GET', 'POST'])
def getMenuItemById():
    req = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute(f"SELECT * FROM navbar_menu WHERE id={req.body}")
    records = [dict(row) for row in myCursor.fetchall()]
    print(records)
    return json.dumps(records)


@app.route("/changeMenuItems", methods=['GET', 'POST'])
def changeMenuItems():
    length = int(request.form['menuLength'])
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM navbar_menu")
    myConnection.commit()
    myConnection.close()
    for i in range(length):
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(
            "INSERT INTO navbar_menu (text_content, content) VALUES (?, ?)",
            (request.form[f'menuTextContent{i}'], request.form[f'menuContent{i}']))
        myConnection.commit()
        myConnection.close()

    return redirect("/#/configurationuser")


@app.route("/getFooterItems")
def getFooterItems():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM footer")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/getFooterCompany")
def getFooterCompany():
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT * FROM footer_company")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route("/changeCompanyName", methods=['GET', 'POST'])
def changeCompanyName():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    companyName = request.form['companyName']
    print(companyName)
    myCursor.execute(f"UPDATE footer_company SET company=?", (companyName,))
    myConnection.commit()
    myConnection.close()
    return redirect("/#/configurationuser")


@app.route("/uploadFooter", methods=['GET', 'POST'])
def uploadFooter():
    length = int(request.form['footerLength'])
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"DELETE FROM footer")
    myConnection.commit()
    myConnection.close()
    for i in range(length):
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute(
            "INSERT INTO footer (text_content, content) VALUES (?, ?)",
            (request.form[f'footerTextContent{i}'], request.form[f'footerContent{i}']))
        myConnection.commit()
        myConnection.close()

    return redirect("/#/configurationuser")


@app.route("/getFooterItemById", methods=['GET', 'POST'])
def getFooterItemById():
    req = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: SimpleNamespace(**d))
    myConnection = sqlite3.connect('usersData.sqlite')
    myConnection.row_factory = sqlite3.Row
    myCursor = myConnection.cursor()
    myCursor.execute(f"SELECT * FROM footer WHERE id={req.body}")
    records = [dict(row) for row in myCursor.fetchall()]
    return json.dumps(records)


@app.route('/addComment', methods=['GET', 'POST'])
def addComment():
    print(request.get_json())
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    time = str(request.get_json()['date']) + ' ' + str(request.get_json()['hour'])
    myCursor.execute(
        f"INSERT INTO comments (user, content, time, articleid) VALUES ('{request.get_json()['user']}', '{request.get_json()['content']}', '{time}', '{int(request.get_json()['articleid'])}')")

    myConnection.commit()
    myConnection.close()
    return redirect("/#/article/" + request.get_json()['articleid'])


@app.route('/getComments', methods=['GET', 'POST'])
def getComments():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(
        "SELECT *, oid FROM comments WHERE articleid=" + request.get_json()['articleid'])
    return json.dumps(myCursor.fetchall())




@app.route('/importSettings', methods=['GET', 'POST'])
def importSettings():
    data = request.get_json()
    content = data['body']
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    with open(path, 'w') as f: f.close()
    with open(path, 'w') as f:
        f.write(json.dumps(content))
    return redirect("/#/configurationuser")






@app.route('/importSettingsWithDatabase', methods=['GET', 'POST'])
def importSettingsWithDatabase():
    data = request.get_json()
    template = data['body']['template']
    databaseContent = data['body']['database']
    path = os.path.join(app.root_path, "client/public/data/settings.json")
    with open(path, 'w') as f: f.close()
    with open(path, 'w') as f:
        f.write(json.dumps(template))

    for i in databaseContent:
        if(i['type']=='navbarItems'):
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute("DELETE FROM navbar_menu")
            myConnection.commit()
            myConnection.close()
            for item in i['content']:
                myConnection = sqlite3.connect('usersData.sqlite')
                myCursor = myConnection.cursor()
                myCursor.execute(
                    "INSERT INTO navbar_menu (text_content, content) VALUES (?, ?)",(item[1], item[2]))
                myConnection.commit()
                myConnection.close()
        elif(i['type']=='slider'):
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute("DELETE FROM slider")
            myConnection.commit()
            myConnection.close()
            for item in i['content']:
                myConnection = sqlite3.connect('usersData.sqlite')
                myCursor = myConnection.cursor()
                myCursor.execute(
                    f"INSERT INTO slider (src,label,texts,sliderOrder) VALUES(?, ?, ?, ?)",(item['src'],item['label'],item['texts'],item['sliderOrder']))
                myConnection.commit()
                myConnection.close()
        elif (i['type'] == 'news'):
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute("DELETE FROM news")
            myConnection.commit()
            myConnection.close()
            for item in i['content']:
                myConnection = sqlite3.connect('usersData.sqlite')
                myCursor = myConnection.cursor()
                myCursor.execute(
                    "INSERT INTO NEWS (header,title,text_content,button_text,content,category, newsOrder, pictures) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (item['header'], item['title'], item['text_content'], item['button_text'], item['content'], item['category'],
                    item['newsOrder'], item['pictures']))
                myConnection.commit()
                myConnection.close()
        elif (i['type'] == 'firstFeaturetteNews'):
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute(f"UPDATE ffn SET title=?, text_content=?, src=?", (i['content'][0]['title'], i['content'][0]['text_content'], i['content'][0]['src']))
            myConnection.commit()
            myConnection.close()
        elif (i['type'] == 'footer'):
            company = i['content']['company'][0][0]
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute(f"UPDATE footer_company SET company=?", (company,))
            myConnection.commit()
            myConnection.close()
            links = i['content']['links']
            myConnection = sqlite3.connect('usersData.sqlite')
            myCursor = myConnection.cursor()
            myCursor.execute("DELETE FROM footer")
            myConnection.commit()
            myConnection.close()
            for item in links:
                myConnection = sqlite3.connect('usersData.sqlite')
                myCursor = myConnection.cursor()
                myCursor.execute(
                    "INSERT INTO footer (text_content, content) VALUES (?, ?)", (item[1], item[2]))
                myConnection.commit()
                myConnection.close()
    return redirect("/#/configurationuser")



if __name__ == "__main__":
    app.run(debug=True)
