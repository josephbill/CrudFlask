# render_template : allows us to return a html output with desired data
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
# app references the object from the Flask Package
# creating a flask application instance
app = Flask(__name__)
# we need a secret key : key is used to create a session , flash will store messages in this session
app.config['SECRET_KEY'] = 'f2233668a56b2f44f270557980e4ebe8950bb4f3a4d4504b'
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
#returning a specific post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    # validating is the post id exists
    if post is None:
        abort(404)
        # if record is found
        return post

# DEFINING THE ROUTE FOR DISPLAYING THE POSTS
# fetchall() returns our rows from the sql query as a regular python dictionary
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


# Posting data
# GET requests are used to retrieve data from a server/ POST is used to post data to a specific route
@app.route('/create/', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        #pick up the values from the form
        title = request.form['title']
        content = request.form['content']
        # validating the values are not empty

        if not title:
            flash("Title is required")
        elif not content:
            flash("content is required")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title,content) VALUES (?, ?)",(title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


# route for editing
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete/', methods=('GET', 'POST'))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    if post is not None:
        flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()







































