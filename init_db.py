import sqlite3

# create a connection to the db
# execute the schema script : executescript() : executes multiple sql statement at once
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
     connection.executescript(f.read())

#setting a cursor to be able to navigate the rows of the table we create
#cursor object allows us to process rows in a database
cursor = connection.cursor()

# creating dummy content / seed content
cursor.execute("INSERT INTO posts (title,content) VALUES (?, ?)",('First Post', 'content first post'))
cursor.execute("INSERT INTO posts (title,content) VALUES (?, ?)",('Second Post', 'content second post'))

# committing the file
connection.commit()
# close the connection
connection.close()
