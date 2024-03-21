from flask import jsonify, request, Blueprint
import sqlite3

api_bp = Blueprint('api', __name__, url_prefix='/api')

def db_connection(): # how we communiate with the database
    conn = None
    try:
        conn = sqlite3.connect('backend/books.sqlite')
    except sqlite3.error as e:
         print(e)
    return conn
        
# this will return the books from the db
@ api_bp.route('/load_books', methods = ['GET'])
def get_books():
    conn = db_connection() # connection to the db (local function)
    if conn is None:
        return jsonify("Database connection failed"), 500
    cursor = conn.cursor() # cursor bookect interacts with the db
# GET
    if request.method == 'GET':
        # this is the sql query passed to the db
        cursor = conn.execute("SELECT * FROM book") 
        books = [row for row in cursor.fetchall()]
        conn.close()
        return books, 200

# GET by title (not used yet)
@ api_bp.route('/search_book_title/<title>', methods = ['GET'])
def get_indivtitleual_book(title):
    conn = db_connection()
    if conn is None:
        return jsonify({'Error': "Database connection failed"}), 500
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM book WHERE title LIKE ?', ('%' + title + '%',))
        books = cursor.fetchall()
        if books:
            book_list = []
            for book in books:
                book = {
                    'id': book[0],
                    'author': book[1],
                    'language': book[2],
                    'title': book[3]
                }   
                book_list.append(book)
            return jsonify(book_list)
        else:
            return jsonify({'message':'book not found'}), 404
            


# delete by title (for button)
@api_bp.route('/del_books/<int:title>', methods=['DELETE'])
def del_books(title):
    conn = db_connection()
    if conn is None:
        return jsonify({'Error': "Database connection failed"}), 500
    cursor = conn.cursor()
    if request.method == 'DELETE':
        cursor.execute('DELETE FROM book WHERE title = ?', (title,))
        conn.commit()
        return jsonify({'message': f"Book with title {title} was deleted"})



    
        
# this is the edit method for the books (not used on frontend yet)
@api_bp.route('/edit_books', methods = ['POST', 'DELETE', 'PUT', 'PATCH'])
def edit_books():
    conn = db_connection()
    cursor = conn.cursor()
# POST
    if request.method == 'POST':
        if request.is_json: #checks if json data was submitted
            if isinstance(request.json, list): # checks if json bookects are in a list (for multiple bookects)
                for item in request.json:
                    new_author = item.get('author') # item is a json dictionary so .get() can be called
                    new_lang = item.get('language')
                    new_title = item.get('title')
                    sql = """INSERT INTO book(author, language, title)
                    VALUES (?, ?, ?)""" # ? are placeholders in parameterized query
                    # Execute the SQL statement with the provtitleed values in place of ?, ?, ?
                    cursor = cursor.execute(sql, (new_author, new_lang, new_title))
                    conn.commit()
                return f"Books created successfully", 200  # return needs to be outstitlee the for loop
            else: # for single json bookect (not in list)
                new_author = request.json.get('author')
                new_lang = request.json.get('language')
                new_title = request.json.get('title')
                sql = """INSERT INTO book(author, language, title)
                VALUES (?, ?, ?)""" # ? are placeholders in parameterized query
                # Execute the SQL statement with the provtitleed values in place of ?, ?, ?
                cursor = cursor.execute(sql, (new_author, new_lang, new_title))
                conn.commit()
                return f"Book with title: {cursor.lastrowtitle} created successfully", 200
             # no need to request for title because the SQL database automatically creates it as the primary key
        else: # checks if form data was submitted
            new_author = request.form['author'] # author value from the user input form
            new_lang = request.form['language']
            new_title = request.form['title']
            sql = """INSERT INTO book(author, language, title)
            VALUES (?, ?, ?)""" # ? are placeholders in parameterized query
            # Execute the SQL statement with the provtitleed values in place of ?, ?, ?
            cursor = cursor.execute(sql, (new_author, new_lang, new_title))
            conn.commit()
            return f"Book with title: {cursor.lastrowtitle} created successfully", 200
            # no need to request for title because the SQL database automatically creates it as the primary key
# DELETE
    elif request.method == 'DELETE':
         sql = ("DELETE FROM book WHERE title = ?")
         #sql2 = ("SELECT name FROM books WHERE title = ?")
         del_title =  request.form['title']
         cursor = conn.execute(sql,(del_title,)) # even with one paramter (del_title) it still needs to be passed as a tuple
         conn.commit() # make sure to use this otherwise the change isnt pushed to the db
         return f"book with title:{del_title} deleted"
# PUT  
    elif request.method == 'PUT': # used to completely update a record
        sql = ('UPDATE book SET ') # ensure space comes after SET to seperate from fields
        update_title = request.form['title']
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        cursor = cursor.execute(sql, (new_author, new_lang, new_title, update_title))
        conn.commit()
        return f"book with title:{update_title} updated"
# PATCH   
    elif request.method == 'PATCH': # could also use a put method with same logic?
        sql = 'UPDATE book SET ' # start the sql query (rest will be generated later)
        update_title = request.form.get('title') # use get as to not throw an error if the title is not in the form
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
        sql += " WHERE title = ?"

        # post to the db  
        cursor = cursor.execute(sql, (*new_values, update_title))
        conn.commit()

        return '\n'.join(message), f"book with title:{update_title} updated"