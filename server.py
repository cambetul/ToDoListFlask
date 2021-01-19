from flask import Flask, render_template
import views
from database import Database
from list import List
import mysql.connector
#from flask_login import LoginManager

    

#lm = LoginManager()
#@lm.user_loader
# def load_user(user_id):
#     return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.secret_key = "betulcam"
    app.config.from_object("settings")
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET","POST"])
    app.add_url_rule("/", view_func=views.home_page)
    # app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/lists", view_func=views.lists_page, methods=["GET", "POST"])
    app.add_url_rule("/tasks", view_func=views.task_page, methods=["GET", "POST"])
    app.add_url_rule("/add-list", view_func=views.list_add_page, methods=["GET","POST"])
    app.add_url_rule("/register",view_func=views.register_page,methods=["GET","POST"])
    app.add_url_rule("/delete-task",view_func=views.deleteTask,methods=["GET","POST"])
    app.add_url_rule("/assign-to-me",view_func=views.AssignToMe,methods=["GET","POST"])
    app.add_url_rule("/set-task-status",view_func=views.SetTaskStatus,methods=["GET","POST"])
    app.add_url_rule("/add-member",view_func=views.AddMember,methods=["GET","POST"])
    app.add_url_rule("/delete-list",view_func=views.DeleteList,methods=["POST"])





    # app.add_url_rule("/test",view_func=views.home_page,methods=["GET","POST"])
    app.add_url_rule("/logout",view_func=views.logout,methods=["GET","POST"])

    db = Database()
    app.config["db"] = db   #store the database object in the configuration to make it accessible to all components in the application
    
    return app



if __name__ == "__main__":
 
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="localhost",debug=True)

@app.errorhandler(404)
def error_not_found(error):
    return render_template  ('error.html'),404