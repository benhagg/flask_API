import sqlite3

conn = sqlite3.connect("books.sqlite") # connects to and generates sqlite3 file if it does not exist
cursor = conn.cursor() # cursor object is used to execute SQL queries

sql_query = """CREATE TABLE book (
    id integer PRIMARY KEY,
    author text NOT NULL, 
    language text NOT NULL,
    title text NOT NULL
)"""

cursor.execute(sql_query) # execute SQL query with the cursor