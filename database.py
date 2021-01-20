from list import List
from task import Task
import mysql.connector
from flask import session
import hashlib

class Database:
    def __init__(self):# constructor
        self.lists = {} # dictionary
        self.tasks = {} # dictionary
        self.users = {} # dictionary
        self._last_list_key = 0
        self.last_task_key = 0
        self.last_user_key = 0
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='todoapp'
        )

    def add_list(self, list):
        self._last_list_key += 1 # array gibi dusun, eleman sayisini arttirdi
        self.lists[self._last_list_key] = list #lists in ilk elemani list oldu
        return self._last_list_key

    def delete_list(self, list_key):
        if list_key in self.lists:
            del self.lists[list_key]

    def md5(self,string):
        return hashlib.md5(string.encode()).hexdigest()

    def GetList(self, list_key):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM list where ListId = %s"
        cursor.execute(sql, (list_key,))  
        selectedList = cursor.fetchone()
        list_ = List(selectedList['Title'], selectedList['DueDate'],selectedList['OwnerId'],selectedList['CreatedDate'],selectedList['ListId'])
        return list_

    def get_lists(self):
        lists = []
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM list WHERE OwnerId = %s ORDER BY CreatedDate DESC"
        userId = session['user_id']
        cursor.execute(sql, (userId,))  
        lists = cursor.fetchall()
        return lists    

    def createUser(self,newUser):
        cursor = self.db.cursor(dictionary=True)
        sql = "INSERT INTO user SET Name = %s, LastName = %s, Password = %s, Email = %s"
        cursor.execute(sql, (newUser.name, newUser.lastname, self.md5(newUser.password), newUser.email))
        self.db.commit()
        if cursor.rowcount:
            session['user_id'] = cursor.lastrowid
            return True
        else:
            return False

    def Login(self,email,password):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE Email = %s AND Password = %s"
        cursor.execute(sql, (email, self.md5(password),))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['UserId']
            return True
        else:
            return False

    def isUserExist(self,email):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE Email=%s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        if(user is not None):
            return True
        else:
            return False

    def IsUserLoggedIn(self):
        if 'user_id' in session:
            return True
        else:
            return False 
        
    def createList(self, newList):
        cursor = self.db.cursor(dictionary=True)
        sql = "INSERT INTO list SET Title = %s, DueDate = %s, OwnerId = %s"
        userId = session['user_id']
        cursor.execute(sql, (newList.title, newList.dueDate, userId))
        self.db.commit()
        if cursor.rowcount:
            sql = "INSERT INTO listmembers SET ListId = %s, UserId = %s"
            cursor.execute(sql, (cursor.lastrowid, userId))
            self.db.commit()
            return True
        else:
            return False

    def createTask(self, newTask):
            cursor = self.db.cursor(dictionary=True)
            sql = "INSERT INTO task SET Content = %s, Point = %s, ListId = %s"
            cursor.execute(sql, (newTask.content, newTask.point,newTask.listId))
            self.db.commit()
            if cursor.rowcount:
                return True
            else:
                return False

    def GetTasks(self, listId):
        cursor = self.db.cursor(dictionary=True)
        user_id = session['user_id']
        sql =   "SELECT CONCAT(taskOwner.Name,' ',taskOwner.LastName) as TaskOwnerName, t.Content, t.Point, t.IsCompleted, t.AssignedUserId, t.ListId, t.TaskId, " \
                "CASE WHEN l.OwnerId = %s THEN 1 ELSE 0 " \
                "END As IsListOwner, " \
                "CASE WHEN t.AssignedUserId = %s THEN 1 " \
                "ELSE 0 " \
                "END As IsTaskAssignedToMe " \
                "FROM `task` t " \
                "JOIN list l on l.ListId = t.ListId "  \
                "LEFT JOIN `user` taskOwner on taskOwner.UserId = t.`AssignedUserId` "  \
                "where l.ListId = %s" 
        cursor.execute(sql, (user_id,user_id,listId,))
        tasks = cursor.fetchall()
        return tasks
    
    def DeleteTask(self,taskId):
        cursor = self.db.cursor(dictionary=True)
        sql = "DELETE FROM task WHERE TaskId = %s"
        cursor.execute(sql, (taskId,))
        self.db.commit()   

    def AssignToMe(self,task_id):
        cursor = self.db.cursor(dictionary=True)
        user_id = session['user_id']
        sql = "UPDATE task SET AssignedUserId = %s WHERE TaskId = %s"
        cursor.execute(sql, (user_id,task_id,)) # db'de işlemi gerçekleştir
        self.db.commit() # db'de işlemi tamamla  

    def SetTaskStatus(self,task_id):
        cursor = self.db.cursor(dictionary=True)
        sql = "UPDATE task SET IsCompleted = true where TaskId = %s"
        cursor.execute(sql, (task_id,))
        user_id = session['user_id']
        self.db.commit() # db'de işlemi tamamla  

    def AddMember(self,list_id,user_id):
        cursor = self.db.cursor(dictionary=True)
        sql = "INSERT INTO listmembers Set UserId = %s, ListId = %s"
        cursor.execute(sql, (user_id, list_id))
        self.db.commit()

    def IsUserInList(self,list_id,user_id):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM listmembers WHERE UserId = %s AND ListId = %s"
        cursor.execute(sql, (user_id,list_id,))
        user = cursor.fetchone()
        if(user is None):
            return False
        else:
            return True 

    def GetUser(self,email):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE Email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        return user
        
    def GetAllList(self):
        cursor = self.db.cursor(dictionary=True)    
        sql = "SELECT l.* from listmembers lm "  \
              "JOIN list l on lm.ListId = l.ListId " \
              "where lm.UserId = %s" 
        user_id = session['user_id']
        cursor.execute(sql, (user_id,))
        lists = cursor.fetchall()
        return lists

    def DeleteList(self,list_id):
        cursor = self.db.cursor(dictionary=True)
        sql = "DELETE FROM list WHERE ListId = %s"
        cursor.execute(sql, (list_id,))
        self.db.commit()

        sql = "DELETE FROM task WHERE ListId = %s"
        cursor.execute(sql, (list_id,))
        self.db.commit()

        sql = "DELETE FROM listmembers WHERE ListId = %s"
        cursor.execute(sql, (list_id,))
        self.db.commit()