import json
from flask import Flask, jsonify, request, render_template, redirect
import my_db
import khmernltk
import text_normalization
import os
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)


def from_txt(text_file):
    """
    Convert text from a file into a list of normalized text chunks.

    Args:
        text_file (str): The path to the text file.

    Returns:
        list: A list of normalized text chunks.

    """
    # Replace Khmer punctuation marks with spaces
    text = text_file.replace('។', ' ')
    
    # Tokenize the text into words using khmernltk
    text = khmernltk.word_tokenize(text)
    
    # Connect text in every 20 words
    text = [''.join(text[i:i+20]) for i in range(0, len(text), 20)]
    
    # Normalize each text chunk using text_normalization module
    text = [text_normalization.text_normalize(t, text_token_by_space=True) for t in text if t != None or t != '']
    
    return text


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_text', methods=['GET'])
def add_text():
    return render_template('add_text.html')

@app.route('/add_text', methods=['POST'])
def add_text_post():
    # This route handles the POST request for adding a text file.
    # It reads the content of the text file and saves it to the server.
    # It also normalizes the text and inserts it into the database.
    # If the file is successfully processed, it returns a success message.
    # If there is an error, it returns an error message.
    
    file = request.files['text_file']
    
    if file and file.filename.endswith('.txt'):
        # Read the content of the text file
        file_content = file.read().decode('utf-8')
        
        # Create necessary directories if they don't exist
        baseRoot = os.getenv('BASE_ROOT', '/var/www/api/')
        if not os.path.exists(os.path.join(baseRoot, 'upload')):
            os.mkdir(os.path.join(baseRoot, 'upload'))
        if not os.path.exists(os.path.join(baseRoot, 'upload/raw')):
            os.mkdir(os.path.join(baseRoot, 'upload/raw'))
        if not os.path.exists(os.path.join(baseRoot, 'upload/normalized')):
            os.mkdir(os.path.join(baseRoot, 'upload/normalized'))
        
        # Save the raw text file
        open(os.path.join(baseRoot, 'upload/raw/') + file.filename, 'w', encoding='UTF-8').write(file_content)
        
        # Normalize the text and save the normalized text file
        texts = from_txt(file_content)
        open(os.path.join(baseRoot, 'upload/normalized/') + file.filename, 'w', encoding='UTF-8').write('\n'.join(texts))
        
        # Insert the normalized text into the database
        for text in texts:
            my_db.insert(text, file.filename)

        return render_template('add_text.html', message='ការបញ្ចូលបានជោគជ័យ', status='primary')

    # If the file is not a valid text file, return an error message
    return render_template('add_text.html', message='ការបញ្ចូលបរាជ័យ', status='danger')

@app.route('/text_normalize', methods=['GET']) 
def text_normalize():
    return render_template('text_normalization.html')  

@app.route('/text_normalize', methods=['POST'])
def text_normalize_post():
    text = request.form['text']
    text = text_normalization.text_normalize(text)
    return jsonify({'text': text})

@app.route('/add_user', methods=['GET'])
def add_user():
    users = my_db.get_users()

    return render_template('add_user.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user_post():
    name = request.form['name']
    my_db.add_user(name)
    users = my_db.get_users()
    return render_template('add_user.html',users = users, message='ការបញ្ចូលបានជោគជ័យ', status='primary')

@app.route('/assign_text/<user_id>', methods=['GET'])
def assign_text(user_id):
    my_db.assign_text_to_user(user_id)
    return redirect('/get_texts_by_user/' + user_id)


# START API
@app.route('/get_text', methods=['GET'])
def get_text():
    """
    Retrieves a text from the database.

    This function retrieves a text from the database and returns it as a JSON response.

    Returns:
        A JSON response containing the text and its ID.
    """
    data = my_db.get_text()
    text = data[1]
    id = data[0]
    return jsonify({'text': text, 'id': id})

@app.route('/set_free', methods=['GET'])
def set_free():
    """
    Sets the status to 'free' in the database.

    This function updates the status of a resource to 'free' in the database.

    Returns:
        A JSON response indicating the status of the operation.
    """
    my_db.status_to_free()
    return jsonify({'status': 'ok'})

@app.route('/saved_text', methods=['POST'])
def saved_text():
    """
    Updates the status of a text to 'saved' in the database.

    This function is called when a text is saved. It updates the status of the text to 'saved' and also saves the name of the WAV file associated with the text.

    Returns:
        A JSON response indicating the status of the operation.
    """
    id = request.form['id']
    wav_name = request.form['name']
    my_db.update_status(id, 'saved', wav_name)
    return jsonify({'status': 'ok'})

@app.route('/get_all_texts', methods=['GET'])
def get_all_texts():
    """
    Retrieves all texts from the database.

    Returns:
        A JSON response containing the retrieved data.
    """
    data = my_db.get_all_texts()
    return jsonify({'data': data})  # Return the retrieved data as a JSON response

@app.route('/get_users', methods=['GET'])
def get_user():
    """
    Retrieves a list of users from the database.

    This function retrieves a list of users from the database and returns it as a JSON response.
    It supports pagination by accepting 'start' and 'limit' parameters in the query string.
    If 'start' and 'limit' parameters are provided, it returns a paginated list of users.
    If 'start' and 'limit' parameters are not provided, it returns the complete list of users.

    Returns:
        A JSON response containing the list of users.
    """
    user = my_db.get_users()
    url = request.base_url
    start = request.args.get('start')
    limit = request.args.get('limit')
    if start == None or limit == None:
        return jsonify({'user': user})
    return jsonify(get_paginated_list(user, url, start, limit))

@app.route('/get_texts_by_user/<user_id>', methods=['GET'])
def get_texts_by_user(user_id):
    """
    Retrieve a list of texts associated with a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        A JSON response containing a paginated list of texts.

    """
    # Retrieve texts from the database based on the user ID
    data = my_db.get_texts_by_user_id(user_id)

    # Get the base URL of the request
    url = request.base_url

    # Get the 'start' and 'limit' query parameters from the request
    start = request.args.get('start', 1)
    limit = request.args.get('limit', 20)

    # Return a JSON response with a paginated list of texts
    return jsonify(get_paginated_list(data, url, start, limit))


@app.route('/get_text_by_user/<user_id>', methods=['GET'])
def get_text_by_user(user_id):
    """
    Retrieves a text associated with a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        A JSON response containing the ID and text of the retrieved text.
    """
    data = my_db.get_text_by_user_id(user_id)
    id = data[0]
    text = data[1]
    return jsonify({'id': id, 'text': text})

@app.route('/skip_text', methods=['POST'])
def update_text_status():
    """
    Updates the status of a text entry to 'skip' in the database.

    Returns:
        A JSON response indicating the status of the update.
    """
    id = request.form['id']
    my_db.update_status(id, 'skip')
    return jsonify({'status': 'ok'})  # Returns a JSON response with the status


def get_paginated_list(data, url, start = 1, limit =20):
    """
    Generates a paginated list of data.

    Args:
        data (list): The data to be paginated.
        url (str): The base URL of the request.
        start (int): The starting index of the data to be returned (default is 1).
        limit (int): The maximum number of items to be returned per page (default is 20).

    Returns:
        A paginated list of data as a dictionary containing 'start', 'limit', 'count', 'previous', 'next', and 'data' keys.
    """
    start = int(start)
    limit = int(limit)
    count = len(data)
    if count < start:
        return jsonify({'error': 'No data'})
    
    obj = {
        'start': start,
        'limit': limit,
        'count': count
    }

    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

    obj['data'] = data[(start - 1):(start - 1 + limit)]
    return obj
  

if __name__ == '__main__':
   app.run(threaded=True)
