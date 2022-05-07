import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
# logW = loginWindow
from tkinter.ttk import Separator
from werkzeug.utils import secure_filename
import pathlib

logW = Tk()
logW.title("Login")
logW.geometry("220x140")
logW.resizable(0, 0)

username = StringVar()
password = StringVar()

robiwrazeniepaddings = {'padx': 30, 'pady': 30}
biggerpaddings = {'padx': 15, 'pady': 10}
paddings = {'padx': 5, 'pady': 5}
tinypaddings = {'padx': 2, 'pady': 2}

Label(logW, text="Username:").grid(column=0, row=0, sticky=W, **paddings)
Entry(logW, textvariable=username).grid(column=1, row=0, sticky=E, **paddings)
Label(logW, text="Password:").grid(column=0, row=1, sticky=W, **paddings)
Entry(logW, textvariable=password, show="*").grid(column=1, row=1, sticky=E, **paddings)
Button(logW, text="Login", command=lambda: loginAttempt(username.get(), password.get())).grid(column=1, row=2, sticky=E,
                                                                                              **paddings)
ifEditingCurrently = 0

editArr = [None] * 3

newsCategories = [
    "Sport",
    "Fashion",
    "Business",
    "Science",
    "Technology",
    "Art & Culture",
    "Current Affairs",
    "Health & Medicine",
    "Lifestyle",
    "Style",
    "Law",
    "Other"
]


def loginAttempt(username, password):
    global logW
    global b1, b2, b3, b4, b5
    records = getAllUserRecords()
    found = False
    for i in records:
        if username == i[0] and password == i[2]:
            found = True
    if not found:
        Label(logW, text="Admin not found", fg='red').grid(column=1, row=3, **paddings)
    else:
        logW.destroy()
        settW = Tk()
        settW.title("Settings")
        settW.geometry("220x250")
        b1 = Button(settW, text="User Management", command=lambda: showUsers(), width=20)
        b1.place(x=40, y=20)
        b2 = Button(settW, text="Slider", command=lambda: showSlider(), width=20)
        b2.place(x=40, y=60)
        b3 = Button(settW, text="Footer", command=lambda: showFooter(), width=20)
        b3.place(x=40, y=140)
        b4 = Button(settW, text="News", command=lambda: showNews(), width=20)
        b4.place(x=40, y=100)
        b5 = Button(settW, text="Menu", command=lambda: showMenu(), width=20)
        b5.place(x=40, y=180)
        settW.mainloop()


def on_closing(button, window):
    button["state"] = "normal"
    window.destroy()


#######################################################################
##USERS ###############################################################
#######################################################################
#######################################################################


def showUsers():
    global usersW
    b1["state"] = "disabled"
    usersW = Toplevel()
    usersW.title("Registered users")
    usersW.geometry("580x700")
    usersW.protocol("WM_DELETE_WINDOW", lambda arg=usersW, b=b1: on_closing(b, arg))
    createUserTable(False, 0)
    usersW.mainloop()


def createUserTable(isEditing, item_id):
    records = getAllUserRecords()
    for widget in usersW.winfo_children():
        widget.destroy()
    Label(usersW, text="Username", font='Helvetica 14 bold').grid(column=0, row=0, **biggerpaddings)
    Label(usersW, text="Email", font='Helvetica 14 bold').grid(column=1, row=0, **biggerpaddings)
    Label(usersW, text="Password", font='Helvetica 14 bold').grid(column=2, row=0, **biggerpaddings)
    for index, item in enumerate(records):
        if item[4] == item_id and isEditing == True:
            for index2, item2 in enumerate(item):
                if index2 != 4 and index2 != 3:
                    createEntry(item2, index2, index)
            if item[3] != 2:
                createButtonDel(index, item)
                createButtonSave(index, item)
            else:
                Label(usersW, text="Admin", fg='red').grid(column=4, row=index + 1, **biggerpaddings)
        else:
            for index2, item2 in enumerate(item):
                if index2 != 4 and index2 != 3:
                    Label(usersW, text=item2).grid(column=index2, row=index + 1, **biggerpaddings)
            if item[3] != 2:
                createButtonDel(index, item)
                createButtonEdit(index, item, isEditing)
            else:
                Label(usersW, text="Admin", fg='red').grid(column=4, row=index + 1, **biggerpaddings)


def createEntry(item2, index2, index):
    # e = Entry(usersW, textvariable=editArr[index2])
    e = Entry(usersW, width=15)
    e.grid(column=index2, row=index + 1, **biggerpaddings)
    e.insert(0, str(item2))
    editArr[index2] = e


def createButtonDel(index, item):
    Button(usersW, text="Delete", command=lambda: deleteUser(item[4])).grid(column=4, row=index + 1, **biggerpaddings)


def createButtonEdit(index, item, isEditing):
    if isEditing:
        Button(usersW, text="Edit", command=lambda: editUser(item[4]), state=DISABLED).grid(column=5, row=index + 1,
                                                                                            **biggerpaddings)
    else:
        Button(usersW, text="Edit", command=lambda: editUser(item[4])).grid(column=5, row=index + 1, **biggerpaddings)


def createButtonSave(index, item):
    Button(usersW, text="Save", command=lambda: saveChanges(item[4])).grid(column=5, row=index + 1, **biggerpaddings)


def saveChanges(item_id):
    global ifEditingCurrently
    Continue = True
    for index, item in enumerate(editArr):
        if not item.get():
            Continue = False
            showEmptyError(index)
    if Continue:
        ifEditingCurrently = 0
        myConnection = sqlite3.connect('usersData.sqlite')
        myCursor = myConnection.cursor()
        myCursor.execute("""UPDATE data SET
                username = :username,
                email = :email,
                password =  :password
    
                WHERE oid = :oid""",
                         {
                             'username': editArr[0].get(),
                             'email': editArr[1].get(),
                             'password': editArr[2].get(),
                             'oid': item_id
                         })
        myConnection.commit()
        myConnection.close()
        createUserTable(False, 0)


def editUser(item_id):
    global ifEditingCurrently
    if ifEditingCurrently == 0:
        createUserTable(True, item_id)
        ifEditingCurrently = 1


def deleteUser(item_id):
    global ifEditingCurrently
    if ifEditingCurrently == 1:
        ifEditingCurrently = 0
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute('DELETE FROM data WHERE oid=' + str(item_id))
    myConnection.commit()
    myConnection.close()
    createUserTable(False, 0)


def showEmptyError(index):
    records = getAllUserRecords()
    Label(usersW, text="This must be filled!", fg='red').grid(column=index, row=len(records) + 3, padx='30')


def getAllUserRecords():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM data")
    records = myCursor.fetchall()
    myConnection.close()
    return records


#######################################################################
##SLIDER ###############################################################
#######################################################################
#######################################################################

def getAllSliderRecords():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM slider")
    records = myCursor.fetchall()
    myConnection.close()
    return records


def showSlider():
    global sliderW
    b2["state"] = "disabled"
    sliderW = Toplevel()
    sliderW.title("Slider settings")
    sliderW.geometry("580x640")
    sliderW.protocol("WM_DELETE_WINDOW", lambda arg=sliderW, b=b2: on_closing(b, arg))
    genSliderNavFrame()
    sliderW.mainloop()


def genSliderNavFrame():
    global navFrame
    global SepNav
    navFrame = Frame(sliderW)
    navFrame.pack(side=TOP)
    for idx, i in enumerate(getAllSliderRecords()):
        createSliderButton(navFrame, i, idx)
    Button(navFrame, text="Add", **tinypaddings, command=lambda: addSlide()).pack(side=LEFT, **paddings)
    SepNav = Separator(sliderW, orient='horizontal')
    SepNav.pack(fill='x')
    if not getAllSliderRecords():
        addSlide()
    else:
        displaySlideFrame(min([i[0] for i in getAllSliderRecords()]))


def createSliderButton(frame, i, idx):
    Button(frame, text="Slide " + str(idx + 1), **tinypaddings, command=lambda: displaySlideFrame(i[0])).pack(side=LEFT,
                                                                                                              **paddings)


def displaySlideFrame(id):
    global pathdb
    global frameAdd
    try:
        frameAdd.destroy()
    except NameError:
        frameAdd = None
    frameAdd = Frame(sliderW, **robiwrazeniepaddings)
    frameAdd.pack()

    records = getAllSliderRecords()
    for idx, i in enumerate(records):
        if i[0] == id:
            index = idx

    Label(frameAdd, text="Label: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryLabel = Text(frameAdd, width=30, height=1, font='Helvetica 10')
    EntryLabel.pack()
    EntryLabel.insert(INSERT, records[index][2])
    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(15, 5))

    Label(frameAdd, text="Texts: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryTexts = Text(frameAdd, width=50, height=3, font='Helvetica 10')
    EntryTexts.pack()
    EntryTexts.insert(INSERT, records[index][3])
    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(13, 20))

    pathdb = records[index][1]
    Label(frameAdd, text="Image: ", font='Helvetica 12 bold').pack(**tinypaddings)
    path = os.path.join(pathlib.Path().resolve(), 'client\public\images\\', split(str(records[index][1]), '/', 3)[1])
    try:
        img = Image.open(path)
    except:
        img = Image.open(os.path.join(pathlib.Path().resolve(), 'client\public\images\sliderPlaceholder1.png'))
    img = ImageTk.PhotoImage(img.resize((250, 100), Image.Resampling.LANCZOS))
    imgDisplay = Label(frameAdd, image=img, borderwidth=2, relief="groove")
    imgDisplay.photo = img
    imgDisplay.pack()
    Button(frameAdd, text="Upload", width=20, padx=15, pady=5, command=lambda: upload_file(frameAdd, imgDisplay)).pack(
        **paddings)
    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(13, 20))

    records = [i[4] for i in getAllSliderRecords()]
    recordsIdx = [records.index(i) + 1 for i in sorted(records)]
    Label(frameAdd, text="Order: ", font='Helvetica 12 bold').pack(**tinypaddings)
    selectedOrder = StringVar(frameAdd)
    selectedOrder.set(recordsIdx[index])
    orderSelect = OptionMenu(frameAdd, selectedOrder, *recordsIdx)
    orderSelect.pack(**tinypaddings)
    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(13, 20))

    Button(frameAdd, text="Save changes", width=15, padx=15, pady=5,
           command=lambda: saveCh(pathdb, EntryTexts, EntryLabel, id, sorted(records)[int(selectedOrder.get()) - 1],
                                  records[index])).pack(side=LEFT,
                                                        **paddings)
    Button(frameAdd, text="Delete slide", width=15, padx=15, pady=5,
           command=lambda: deleteSlide(id)).pack(side=RIGHT,
                                                 **paddings)


def deleteSlide(id):
    global frameAdd
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute('DELETE FROM slider WHERE id=' + str(id))
    myConnection.commit()
    navFrame.destroy()
    SepNav.pack_forget()
    try:
        frameAdd.destroy()
    except NameError:
        frameAdd = None
    genSliderNavFrame()


def saveCh(path, texts, label, id, order, previousOrder):
    records = [i[4] for i in getAllSliderRecords()]
    tochange = getAllSliderRecords()[records.index(order)][0]
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("""UPDATE slider SET
                        sliderOrder = :sliderOrder
                        WHERE id = :id""",
                     {
                         'sliderOrder': previousOrder,
                         'id': tochange
                     })
    myConnection.commit()

    myCursor.execute("""UPDATE slider SET
                    src = :src,
                    label = :label,
                    texts =  :texts,
                    sliderOrder = :sliderOrder
                    WHERE id = :id""",
                     {
                         'src': path,
                         'label': label.get('1.0', 'end-1c'),
                         'texts': texts.get('1.0', 'end-1c'),
                         'sliderOrder': order,
                         'id': id
                     })
    myConnection.commit()


def addSlide():
    global frameAdd
    try:
        frameAdd.destroy()
    except NameError:
        frameAdd = None
    frameAdd = Frame(sliderW, **robiwrazeniepaddings)
    frameAdd.pack()

    Label(frameAdd, text="Label: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryLabel = Text(frameAdd, width=30, height=1, font='Helvetica 10')
    EntryLabel.pack()
    EntryLabel.insert(INSERT, "Label")
    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(15, 40))

    Label(frameAdd, text="Texts: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryTexts = Text(frameAdd, width=50, height=3, font='Helvetica 10')
    EntryTexts.pack()
    EntryTexts.insert(INSERT, "Some representative placeholder content for the first side")
    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(15, 40))

    Label(frameAdd, text="Upload image: ", font='Helvetica 12 bold').pack(**tinypaddings)
    Button(frameAdd, text="Upload", width=20, padx=15, pady=5, command=lambda: upload_file(frameAdd, imgDisplay)).pack(
        **paddings)

    path = os.path.join(pathlib.Path().resolve(), 'client\public\images\sliderPlaceholder1.png')
    img = Image.open(path)
    img = ImageTk.PhotoImage(img.resize((250, 100), Image.Resampling.LANCZOS))
    imgDisplay = Label(frameAdd, image=img, borderwidth=2, relief="groove")
    imgDisplay.photo = img
    imgDisplay.pack()

    Separator(frameAdd, orient='horizontal').pack(fill='x', pady=(15, 40))

    Button(frameAdd, text="Add slide", font='Helvetica 12 bold', width=25, **paddings,
           command=lambda: saveNewSlide(EntryLabel, EntryTexts, pathdb)).pack(side=BOTTOM,
                                                                              **biggerpaddings)


def upload_file(frame, imgDisplay):
    global pathdb
    f_types = [('Pictures', '*.jpg *.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    path = os.path.join(pathlib.Path().resolve(), 'client\public\images')
    path = os.path.join(path, filename.rsplit('/', 1)[1])
    pathdb = '../../images/' + filename.rsplit('/', 1)[1]
    img.save(path)

    img_display = ImageTk.PhotoImage(img.resize((250, 100), Image.Resampling.LANCZOS))

    imgDisplay.config(image=img_display)
    imgDisplay.photo = img_display


def saveNewSlide(label, text, filepath):
    global frameAdd
    records = getAllSliderRecords()
    recordsOrder = [i[4] for i in records]
    if not recordsOrder:
        recordsOrder = [0]
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(
        f"INSERT INTO slider (src,label,texts,sliderOrder) VALUES('{filepath}','{label.get('1.0', 'end-1c')}','{text.get('1.0', 'end-1c')}',{max(recordsOrder) + 1})")
    myConnection.commit()
    myConnection.close()
    navFrame.destroy()
    SepNav.pack_forget()
    try:
        frameAdd.destroy()
    except NameError:
        frameAdd = None
    genSliderNavFrame()


#######################################################################
##NEWS ###############################################################
#######################################################################
#######################################################################


def showNews():
    global newsW
    b4["state"] = "disabled"
    newsW = Toplevel()
    newsW.title("News")
    newsW.geometry("600x620")
    newsW.protocol("WM_DELETE_WINDOW", lambda arg=newsW, b=b4: on_closing(b, arg))
    genNewsNav()
    newsW.mainloop()


def genNewsNav():
    global SepNavN
    global navNewsFrame
    navNewsFrame = Frame(newsW)
    navNewsFrame.pack(side=TOP)
    for idx, i in enumerate(getAllNewsRecords()):
        createNewsButton(navNewsFrame, i, idx)
    Button(navNewsFrame, text="Add", **tinypaddings, command=lambda: addNews()).pack(side=LEFT, **paddings)
    SepNavN = Separator(newsW, orient='horizontal')
    SepNavN.pack(fill='x')
    if not getAllNewsRecords():
        addNews()
    else:
        displayNewsFrame(min([i[4] for i in getAllNewsRecords()]))


def createNewsButton(frame, i, idx):
    Button(frame, text="News " + str(idx + 1), **tinypaddings, command=lambda: displayNewsFrame(i[4])).pack(side=LEFT,
                                                                                                            **paddings)


def displayNewsFrame(id):
    global frameNews
    try:
        frameNews.destroy()
    except NameError:
        frameNews = None
    frameNews = Frame(newsW, **robiwrazeniepaddings)
    frameNews.pack()

    record = getAllNewsRecords()[[i[4] for i in getAllNewsRecords()].index(id)]

    Label(frameNews, text="Header: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryH = Text(frameNews, width=30, height=1, font='Helvetica 10')
    EntryH.pack()
    EntryH.insert(INSERT, record[0])
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Label(frameNews, text="Title: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryT = Text(frameNews, width=40, height=1, font='Helvetica 9')
    EntryT.pack()
    EntryT.insert(INSERT, record[1])
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Label(frameNews, text="Text content: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryTC = Text(frameNews, width=50, height=4, font='Helvetica 9')
    EntryTC.pack()
    EntryTC.insert(INSERT, record[2])
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Label(frameNews, text="Button text: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryBT = Text(frameNews, width=20, height=1, font='Helvetica 10')
    EntryBT.pack(**biggerpaddings)
    EntryBT.insert(INSERT, record[3])

    Label(frameNews, text="Category: ", font='Helvetica 12 bold').pack(**tinypaddings)
    selectedOrder = StringVar(frameNews)
    selectedOrder.set(record[6])
    orderSelect = OptionMenu(frameNews, selectedOrder, *newsCategories)
    orderSelect.pack(**tinypaddings)
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Button(frameNews, text="Save changes", width=15, padx=15, pady=5,
           command=lambda: saveChN(EntryH.get('1.0', 'end-1c'), EntryT.get('1.0', 'end-1c'),
                                   EntryTC.get('1.0', 'end-1c'), EntryBT.get('1.0', 'end-1c'), selectedOrder.get(),
                                   id)).pack(side=LEFT,
                                             **paddings)
    Button(frameNews, text="Delete news", width=15, padx=15, pady=5,
           command=lambda: deleteNews(id, frameNews)).pack(side=RIGHT,
                                                           **paddings)


def saveChN(Header, Title, Text_Content, Button_Text, Category, id):
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute(f"select * from news where idnews ={id}")
    records = myCursor.fetchall()
    record = records[0]
    content = record[2]
    pictures = record[8]
    myConnection.commit()
    myConnection.close()
    

    

    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("UPDATE news SET header = ?, title = ?, text_content =  ?, button_text = ?, category = ?, content = ?, pictures = ? WHERE idnews = ?",(Header,Title,Text_Content,Button_Text,Category,id,content,pictures))
    myConnection.commit()


def deleteNews(id, frameNews):
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute('DELETE FROM news WHERE idnews=' + str(id))
    myConnection.commit()
    navNewsFrame.destroy()
    SepNavN.pack_forget()
    try:
        frameNews.destroy()
    except NameError:
        frameAdd = None
    genNewsNav()


def addNews():
    global frameNews
    try:
        frameNews.destroy()
    except NameError:
        frameNews = None
    frameNews = Frame(newsW, **robiwrazeniepaddings)
    frameNews.pack()

    Label(frameNews, text="Header: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryH = Text(frameNews, width=30, height=1, font='Helvetica 10')
    EntryH.pack()
    EntryH.insert(INSERT, "Header")
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Label(frameNews, text="Title: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryT = Text(frameNews, width=40, height=1, font='Helvetica 9')
    EntryT.pack()
    EntryT.insert(INSERT, "News title")
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Label(frameNews, text="Text content: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryTC = Text(frameNews, width=50, height=4, font='Helvetica 9')
    EntryTC.pack()
    EntryTC.insert(INSERT, "Placeholder text for article summary")
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Label(frameNews, text="Button text: ", font='Helvetica 12 bold').pack(**tinypaddings)
    EntryBT = Text(frameNews, width=20, height=1, font='Helvetica 10')
    EntryBT.pack(**biggerpaddings)
    EntryBT.insert(INSERT, "Show")

    Label(frameNews, text="Category: ", font='Helvetica 12 bold').pack(**tinypaddings)
    selectedOrder = StringVar(frameNews)
    selectedOrder.set(newsCategories[0])
    orderSelect = OptionMenu(frameNews, selectedOrder, *newsCategories)
    orderSelect.pack(**tinypaddings)
    Separator(frameNews, orient='horizontal').pack(fill='x', pady=(15, 20))

    Button(frameNews, text="Add news", font='Helvetica 12 bold', width=25, **paddings,
           command=lambda: saveNewNews(EntryH.get('1.0', 'end-1c'), EntryT.get('1.0', 'end-1c'),
                                       EntryTC.get('1.0', 'end-1c'), EntryBT.get('1.0', 'end-1c'), selectedOrder.get(),
                                       frameNews)).pack(side=BOTTOM,
                                                        **biggerpaddings)


def saveNewNews(Header, Title, Text_Content, Button_Text, Category, frameNews):
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    pictures = []
    content = ""
    print(
        f"INSERT INTO news (header,title,text_content,button_text, category, idnews) VALUES('{Header}','{Title}','{Text_Content}','{Button_Text}','{Category}','{max([i[4] for i in getAllNewsRecords()]) + 1}'")
    myCursor.execute(
        f"INSERT INTO news (header,title,text_content,button_text, category, idnews, pictures, content) VALUES('{Header}','{Title}','{Text_Content}','{Button_Text}','{Category}','{max([i[4] for i in getAllNewsRecords()]) + 1}','{pictures}','{content}')")
    myConnection.commit()
    myConnection.close()
    navNewsFrame.destroy()
    SepNavN.pack_forget()
    try:
        frameNews.destroy()
    except NameError:
        frameNews = None
    genNewsNav()


def getAllNewsRecords():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM news")
    records = myCursor.fetchall()
    myConnection.close()
    return records


#######################################################################
##FOOTER ###############################################################
#######################################################################
#######################################################################

def showFooter():
    global footerW
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM footer")
    recordsLinks = myCursor.fetchall()
    windowLength = str(180 + len(recordsLinks) * 130)

    b3["state"] = "disabled"
    footerW = Toplevel()
    footerW.title("Footer content")
    footerW.geometry("250x" + windowLength)
    footerW.protocol("WM_DELETE_WINDOW", lambda arg=footerW, b=b3: on_closing(b, arg))
    genFooterWContent()
    footerW.mainloop()


def genFooterWContent():
    global InputArr
    mainframe = Frame(footerW, **biggerpaddings)
    mainframe.pack()

    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM footer")
    recordsLinks = myCursor.fetchall()
    myCursor.execute("SELECT *, oid FROM footer_company")
    recordsCompany = myCursor.fetchall()[0][0]
    myConnection.close()

    InputArr = []

    Label(mainframe, text="Company Name: ", font='Helvetica 12 bold').pack(**tinypaddings)
    CompLabel = Text(mainframe, width=25, height=1, font='Helvetica 10')
    CompLabel.pack()
    CompLabel.insert(INSERT, recordsCompany)

    Label(mainframe, text="Links: ", font='Helvetica 12 bold').pack(pady=(20, 5))
    for i in recordsLinks:
        genFooterLinkInput(i, mainframe)

    Button(mainframe, text="Save Changes", command=lambda: saveFooterCh(), width=30, **tinypaddings).pack(**paddings)


def saveFooterCh():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    for i in InputArr:
        myCursor.execute("""UPDATE footer SET
                        text_content = :text_content,
                        content = :content 
                        WHERE id = :id""",
                         {
                             'text_content': i.getTextContent(),
                             'content': i.getContent(),
                             'id': i.getId()
                         })
        myConnection.commit()


class FooterLink:
    def __init__(self, input1, input2, id):
        self.input1 = input1
        self.input2 = input2
        self.id = id

    def getTextContent(self):
        return self.input1.get('1.0', 'end-1c')

    def getContent(self):
        return self.input2.get('1.0', 'end-1c')

    def getId(self):
        return self.id


def genFooterLinkInput(data, frame):
    Label(frame, text="Text: ", font='Helvetica 7 bold').pack()
    Input = Text(frame, width=25, height=1, font='Helvetica 10')
    Input.pack(**tinypaddings)
    Input.insert(INSERT, data[1])

    Label(frame, text="Content: ", font='Helvetica 7 bold').pack()
    Input2 = Text(frame, width=25, height=3, font='Helvetica 9')
    Input2.pack(**tinypaddings)
    Input2.insert(INSERT, data[2])

    FLink = FooterLink(Input, Input2, data[0])
    InputArr.append(FLink)
    Separator(frame, orient='horizontal').pack(fill='x', pady=(10, 10))


#######################################################################
##MENU ################################################################
#######################################################################
#######################################################################

def showMenu():
    global menuW
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM navbar_menu")
    recordsLinks = myCursor.fetchall()
    windowLength = str(120 + len(recordsLinks) * 130)

    b4["state"] = "disabled"
    menuW = Toplevel()
    menuW.title("Footer content")
    menuW.geometry("250x" + windowLength)
    menuW.protocol("WM_DELETE_WINDOW", lambda arg=menuW, b=b4: on_closing(b, arg))
    genMenuWContent()
    menuW.mainloop()

def genMenuWContent():
    global InputArrM
    mainframe = Frame(menuW, **biggerpaddings)
    mainframe.pack()

    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    myCursor.execute("SELECT *, oid FROM navbar_menu")
    recordsLinks = myCursor.fetchall()
    myConnection.close()

    InputArrM = []

    Label(mainframe, text="Links: ", font='Helvetica 12 bold').pack()
    for i in recordsLinks:
        genMenuLinkInput(i, mainframe)

    Button(mainframe, text="Save Changes", command=lambda: saveMenuCh(), width=30, **tinypaddings).pack(**paddings)


def genMenuLinkInput(data, frame):
    Label(frame, text="Text: ", font='Helvetica 7 bold').pack()
    Input = Text(frame, width=25, height=1, font='Helvetica 10')
    Input.pack(**tinypaddings)
    Input.insert(INSERT, data[1])

    Label(frame, text="Content: ", font='Helvetica 7 bold').pack()
    Input2 = Text(frame, width=25, height=3, font='Helvetica 9')
    Input2.pack(**tinypaddings)
    Input2.insert(INSERT, data[2])

    MLink = FooterLink(Input, Input2, data[0])
    InputArrM.append(MLink)
    Separator(frame, orient='horizontal').pack(fill='x', pady=(10, 10))


def saveMenuCh():
    myConnection = sqlite3.connect('usersData.sqlite')
    myCursor = myConnection.cursor()
    for i in InputArrM:
        myCursor.execute("""UPDATE navbar_menu SET
                        text_content = :text_content,
                        content = :content 
                        WHERE id = :id""",
                         {
                             'text_content': i.getTextContent(),
                             'content': i.getContent(),
                             'id': i.getId()
                         })
        myConnection.commit()


######
def split(strng, sep, pos):
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])


logW.mainloop()
