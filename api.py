import json
from flask import Flask, jsonify, request, render_template, redirect
import my_db
import khmernltk
import text_normalization
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# text = open('text.txt', 'r', encoding='UTF-8').read()

def from_txt(text_file):
    # text = open(text_file, 'r', encoding='UTF-8').read()
    text = text_file.replace('។', ' ')
    text = khmernltk.word_tokenize(text)
    # connect text in every 20 words
    text = [''.join(text[i:i+20]) for i in range(0, len(text), 20)]

    text = [text_normalization.text_normalize(t) for t in text if t != None or t != '']
    return text


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_text', methods=['GET'])
def add_text():
    return render_template('add_text.html')

@app.route('/add_text', methods=['POST'])
def add_text_post():
    # return jsonify({'text': 'true'})
    file = request.files['text_file']
    if file and file.filename.endswith('.txt'):
        # Read the content of the text file
        file_content = file.read().decode('utf-8')
        baseRoot = os.getenv('BASE_ROOT', '/var/www/api/')
        if not os.path.exists(os.path.join(baseRoot, 'upload')):
            os.mkdir(os.path.join(baseRoot, 'upload'))
        if not os.path.exists(os.path.join(baseRoot, 'upload/raw')):
            os.mkdir(os.path.join(baseRoot, 'upload/raw'))
        if not os.path.exists(os.path.join(baseRoot, 'upload/normalized')):
            os.mkdir(os.path.join(baseRoot, 'upload/normalized'))           
        open(os.path.join(baseRoot, 'upload/raw/') + file.filename, 'w', encoding='UTF-8').write(file_content)
        
        texts = from_txt(file_content)
        open(os.path.join(baseRoot, 'upload/normalized/') + file.filename, 'w', encoding='UTF-8').write('\n'.join(texts))
        for text in texts:
            my_db.insert(text, file.filename)

        return render_template('add_text.html', message='ការបញ្ចូលបានជោគជ័យ', status='primary')

    
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
    data = my_db.get_text()
    text = data[1]
    id = data[0]
    return jsonify({'text': text, 'id': id})

@app.route('/set_free', methods=['GET'])
def set_free():
    my_db.status_to_free()
    return jsonify({'status': 'ok'})

@app.route('/saved_text', methods=['POST'])
def saved_text():
    id = request.form['id']
    wav_name = request.form['name']
    my_db.update_status(id, 'saved', wav_name)
    return jsonify({'status': 'ok'})

@app.route('/get_all_texts', methods=['GET'])
def get_all_texts():
    data = my_db.get_all_texts()
    return jsonify({'data': data})

@app.route('/get_users', methods=['GET'])
def get_user():
    user = my_db.get_users()
    return jsonify({'user': user})

@app.route('/get_texts_by_user/<user_id>', methods=['GET'])
def get_texts_by_user(user_id):
    data = my_db.get_texts_by_user_id(user_id)
    url = request.base_url
    start = request.args.get('start', 1)
    limit = request.args.get('limit', 20)
    return jsonify(get_paginated_list(data, url, start, limit))


@app.route('/get_text_by_user/<user_id>', methods=['GET'])
def get_text_by_user(user_id):
    data = my_db.get_text_by_user_id(user_id)
    # return jsonify({'data': data})
    id = data[0]
    text = data[1]
    return jsonify({'id': id, 'text': text})



def get_paginated_list(data, url, start = 1, limit =20):
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
   app.run()