# render_template : allows us to return a html output with desired data
import sqlite3
from flask import Flask, render_template
# app references the object from the Flask Package
# creating a flask application instance
app = Flask(__name__)
# by creation of the instance above . We can use it to handle incoming web requests and send responses to users

# app.route this is called a decorator , turns a regular python function into a flask view(user can see elements) function
# The flask view function : converts the function return value into a HTTP response to be displayed by a HTTP client
# such as a web browser.
# decorator markup : @app.route('/')
# @app.route('/')
# def hello_world():  # put application's code here
#     return '<h4>Hello World!</h4>'
#
# @app.route('/newroute')
# def hello_route():  # put application's code here
#     return '<h4>New Route!</h4>'

# create a connection to our sqlite db
# we define a row_factory : gives name-based access to columns in a database table
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# DEFINING THE ROUTE FOR DISPLAYING THE POSTS
# fetchall() returns our rows from the sql query as a regular python dictionary
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run()























