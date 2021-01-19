from datetime import  datetime
from flask import render_template, current_app, request, redirect,  url_for,  session
import mysql.connector
from user import User
from list import List
from task import Task
import hashlib

# db = current_app.config["db"]
# cursor = db.cursor(dictionary=True)
def getDb():
    return current_app.config["db"]

def md5(string):
    return hashlib.md5(string.encode()).hexdigest()

def home_page():
    db = getDb()
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day = day_name)

def lists_page(): # kullanıcının listelerini sırala ve tıklayınca listeye git
    if request.method == "GET":
        db = getDb()
        lists = db.get_lists()
        return render_template("lists.html", lists=lists)
    else: #delete
        form_list_keys = request.form.getlist("list_keys")
        for form_list_key in form_list_keys:
            db.delete_list(int(form_list_key))
        return redirect(url_for("lists_page"))


def task_page():
    db = getDb()
    error = ''
    if request.method == 'POST':
        if request.form['content'] == '' or request.form['point'] is None or request.form['listId'] == 0:
            error = 'Please fill all required fields.'
        elif int(request.form["point"]) < 0 or int(request.form["point"])  > 10:
            error = 'Max and min values of a point is 10 and 0'
        else:
            newTask = Task(request.form['content'],request.form['point'],request.form['listId'])
            isSuccess = db.createTask(newTask)
            if(isSuccess):
                return redirect(url_for("task_page", list_key = request.form['listId']))
            else:
                error = 'Problem occured.'
    elif request.method == 'GET':
        listId = request.args.get('list_key')
        currentList = []
        currentList = db.GetList(listId)
        tasks = []
        tasks = db.GetTasks(listId)
        return render_template("tasks.html", tasks = tasks, listName=currentList.title, listId = currentList.listId)
        
    return render_template("tasks.html",error = error)

# def list_add_page():
#     if request.method == "GET":
#         return render_template("list_edit.html", min_year=1887, max_year=datetime.now().year)
#     else:
#         form_title = request.form["title"]
#         form_year = request.form["year"]
#         list = List(form_title, year=int(form_year) if form_year else None)
#         db = current_app.config["db"]
#         list_key = db.add_list(list)
#         return redirect(url_for("task_page", list_key=list_key))

def list_add_page():
    db = getDb()
    error = ''
    if request.method == "POST":
        if request.form['title'] == '' or request.form["year"] is None:
            error = 'Please fill all required fields.'
            return render_template("list_edit.html", min_year = datetime.now().year, error = error)
        else:
            newList = List(request.form['title'], dueDate = request.form["year"])
            isSuccess = db.createList(newList)
            if(isSuccess):
                return redirect("/lists")
            else:
                error = 'Problem occured.'
                return render_template("list_edit.html", min_year = datetime.now().year, error = error)
    else:
        return render_template("list_edit.html", min_year = datetime.now().year, error = error)

def register_page():
    db = getDb()
    error = ''  
    if request.method == 'POST':
        if request.form['name'] == '' or request.form["lastname"] == '' or request.form["password"] == '' or request.form["re_password"] == '' :
            error = 'Please fill all required fields.'
        elif request.form['password'] != request.form['re_password']:
            error = 'Passwords do not match'
        else:
            isUserExists = db.isUserExist(request.form['email'])
            # sql = "SELECT * FROM user WHERE Email=%s"
            # cursor.execute(sql, (request.form['email'],))
            # user = cursor.fetchone()       
            if(isUserExists):
                error = 'Bu email ile kayıtlı kullanıcı var'
            else:
                newUser = User(request.form['name'],request.form['lastname'],request.form['email'],request.form['password'])
                isSuccess = db.createUser(newUser)
                if(isSuccess):
                    return redirect(url_for('home_page'))
                else:
                    error = 'Problem occured.'
    return render_template("register.html", error = error)
    #else:
    #    form_name = request.form.get("name")
    #    form_surname = request.form.get("surname")
    #    form_mail = request.form.get("mail")
    #    form_password = request.form.get("password")
    #    new_user = User(form_name,form_password) #burayı düzelt
    #    db = current_app.config["db"]
    #    user_key = db.add_user(new_user)
    #    return redirect(url_for("home_page")

def login_page():
    db = getDb()
    if(db.IsUserLoggedIn()):  #cannot login again
        return redirect(url_for("home_page"))
    error = ''
    if request.method == 'POST':
        isSuccess = db.Login(request.form['email'],request.form['password'])
        if(isSuccess):
            return redirect(url_for("home_page"))
        else:
            error = 'Wrong email or password'
    else:
        return render_template("login.html",error = error)