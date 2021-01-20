from datetime import  datetime
from flask import render_template, current_app, request, redirect,  url_for,  session, jsonify
import mysql.connector
from user import User
from list import List
from task import Task
import hashlib

# db = current_app.config["db"]
def getDb():
    return current_app.config["db"]

def md5(string):
    return hashlib.md5(string.encode()).hexdigest()

def home_page():
    if 'user_id' in session: # if user logged in
        db = getDb()
        today = datetime.today()
        day_name = today.strftime("%A")
        return render_template("home.html", day = day_name)
    else:
        return redirect(url_for('login_page'))

def lists_page(): # kullanıcının listelerini sırala ve tıklayınca listeye git
    if 'user_id' in session:
        if request.method == "GET":
            db = getDb()
            lists = db.GetAllList()
            return render_template("lists.html", lists=lists)
        else: #delete
            form_list_keys = request.form.getlist("list_keys")
            for form_list_key in form_list_keys:
                db.delete_list(int(form_list_key))
            return redirect(url_for("lists_page"))
    else:
        return redirect(url_for("login_page"))

def task_page():
    if 'user_id' in session: # if user logged in
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
    else:
        return redirect(url_for("login_page"))

def list_add_page():
    if 'user_id' in session:
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
    else:
        return redirect(url_for('login_page'))

def register_page():
    if 'user_id' in session:
        return redirect(url_for('home_page'))
    else:
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

def login_page():
    if('user_id' in session):  #cannot login again
        return redirect(url_for("home_page"))
    db = getDb()
    error = ''
    if request.method == 'POST':
        isSuccess = db.Login(request.form['email'],request.form['password'])
        if(isSuccess):
            return redirect(url_for("home_page"))
        else:
            error = 'Wrong email or password'
            return render_template("login.html",error = error)
    else:
        return render_template("login.html",error = error)

def logout():
    session.clear()
    return redirect(url_for('login_page'))

def deleteTask():
    if request.method == 'POST':
        taskId = request.form['TaskId']
        db = getDb()
        db.DeleteTask(taskId)
    return jsonify(success=True) #başarılı mesajı dön

def SetTaskStatus():
    if request.method == 'POST':
        task_Id = request.form['TaskId']
        db = getDb()
        db.SetTaskStatus(task_Id)
    return jsonify(success=True) #başarılı mesajı dön

def AssignToMe():
    if request.method == 'POST':
        task_id = request.form['TaskId']
        db = getDb()
        db.AssignToMe(task_id)
    return jsonify(success=True) #başarılı mesajı dön
    
def AddMember():
    db = getDb()
    message = ''
    if request.method == 'POST':
        list_id = request.form['list_id']
        member_email = request.form['member_email']
        user = db.GetUser(member_email.strip())
        if(user is None):
            message = 'There is no user registered with this email.'
        elif(db.IsUserInList(list_id,user['UserId'])):
            message = 'This user is already in list.'
        else:
            db.AddMember(list_id, user['UserId'])
            message = 'User is added to list successfully'
        
    lists = db.get_lists()
    return render_template("add_member.html", lists=lists, message = message)
            
def DeleteList():
    db=getDb()
    if(request.method == 'POST'):
        list_id = request.form['ListId']
        db.DeleteList(list_id)
    return jsonify(success=True) #başarılı mesajı dön