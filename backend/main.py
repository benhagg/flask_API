from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import sqlite3
app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*", "methods": "GET, POST"}})


def db_connection(): # how we communiate with the database
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
         print(e)
    return conn
        

@ app.route('/books', methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def books():
    conn = db_connection()
    cursor = conn.cursor() 

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book WHERE id BETWEEN 1 AND 4") # this is the sql query passed to the db
        books = [
             dict(id=row[0], author =row[1], language = row[2], title = row[3]) # dictionary comprehension
             for row in cursor.fetchall() 
# fetches all rows from executed earlier. It returns a  tuple for each row in the result set.

        ]
        if books is not None:
                return jsonify(books), 200

    elif request.method == 'POST':
        if request.is_json: #checks if json data was submitted
            if isinstance(request.json, list): # checks if json objects are in a list (for multiple objects)
                for item in request.json:
                    new_author = item.get('author') # item is a json dictionary so .get() can be called
                    new_lang = item.get('language')
                    new_title = item.get('title')
                    sql = """INSERT INTO book(author, language, title)
                    VALUES (?, ?, ?)""" # ? are placeholders in parameterized query
                    # Execute the SQL statement with the provided values in place of ?, ?, ?
                    cursor = cursor.execute(sql, (new_author, new_lang, new_title))
                    conn.commit()
                return f"Book with id: {cursor.lastrowid} created successfully", 200 # return needs to be outside the for loop
            else: # for single json object (not in list)
                new_author = request.json.get('author')
                new_lang = request.json.get('language')
                new_title = request.json.get('title')
                sql = """INSERT INTO book(author, language, title)
                VALUES (?, ?, ?)""" # ? are placeholders in parameterized query
                # Execute the SQL statement with the provided values in place of ?, ?, ?
                cursor = cursor.execute(sql, (new_author, new_lang, new_title))
                conn.commit()
                return f"Book with id: {cursor.lastrowid} created successfully", 200
             # no need to request for id because the SQL database automatically creates it as the primary key
        else: # checks if form data was submitted
            new_author = request.form['author'] # author value from the user input form
            new_lang = request.form['language']
            new_title = request.form['title']
            sql = """INSERT INTO book(author, language, title)
            VALUES (?, ?, ?)""" # ? are placeholders in parameterized query
            # Execute the SQL statement with the provided values in place of ?, ?, ?
            cursor = cursor.execute(sql, (new_author, new_lang, new_title))
            conn.commit()
            return f"Book with id: {cursor.lastrowid} created successfully", 200
            # no need to request for id because the SQL database automatically creates it as the primary key

    elif request.method == 'DELETE':
         sql = ("DELETE FROM book WHERE id = ?")
         #sql2 = ("SELECT name FROM books WHERE id = ?")
         del_id =  request.form['id']
         cursor = conn.execute(sql,(del_id,)) # even with one paramter (del_id) it still needs to be passed as a tuple
         conn.commit() # make sure to use this otherwise the change isnt pushed to the db
         return f"book with id:{del_id} deleted"
    
    elif request.method == 'PUT': # used to completely update a record
        sql = ('UPDATE book SET ') # ensure space comes after SET to seperate from fields
        update_id = request.form['id']
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        cursor = cursor.execute(sql, (new_author, new_lang, new_title, update_id))
        conn.commit()
        return f"book with id:{update_id} updated"
    
    elif request.method == 'PATCH': # could also use a put method with same logic?
        sql = 'UPDATE book SET ' # start the sql query (rest will be generated later)
        update_id = request.form.get('id') # use get as to not throw an error if the id is not in the form
        new_values = []
        message = []
        new_columns = []
        if 'author' in request.form:
            new_author = request.form['author']
            new_values.append(new_author)
            new_columns.append('author')
            message.append(f"author updated to {new_author}")
        
        if 'language' in request.form:
            new_language = request.form['language']
            new_values.append(new_language)
            new_columns.append('language')
            message.append(f"language updated to {new_language}")
        
        if 'title' in request.form:
            new_title = request.form['title']
            new_values.append(new_title)
            new_columns.append('title')
            message.append(f"title  updated to {new_title}")
        
        # generate the sql query based on what fields were passed in the form
        # join all fields in the new_values list with comma and space append to sql query
        sql += ', '.join([f"{field} = ?" for field in new_columns])
        sql += " WHERE id = ?"

        # post to the db  
        cursor = cursor.execute(sql, (*new_values, update_id))
        conn.commit()

        return '\n'.join(message), f"book with id:{update_id} updated"


if __name__ == '__main__':
    app.run(debug = True)