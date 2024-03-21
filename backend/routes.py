from flask import Blueprint, render_template
import requests
routes_bp = Blueprint('routes', __name__, template_folder='../templates')
# .. to navigate to the parent directory for template and static folders

@routes_bp.route('/')
def book_table():
    api_endpoint = 'http://localhost:5000/api/load_books'
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        response = response.json()
        return render_template('book_table.html', books=response)
    else:
        return f'Error: {response.status_code}'
# books is a list of dictionaries from the GET method in api.py
    
@routes_bp.route('/search_book_title/<title>')
def search_results():
    api_endpoint = 'http://localhost:5000/api/search_book_title/{title}'
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        response = response.json
        return render_template('search_results.html', search_books = response)
    else:
        return render_template('search_results.html', search_books = [], message ="No results")

