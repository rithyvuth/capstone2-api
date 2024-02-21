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
    return jsonify({'data': data})


@app.route('/get_text_by_user/<user_id>', methods=['GET'])
def get_text_by_user(user_id):
    data = my_db.get_text_by_user_id(user_id)
    # return jsonify({'data': data})
    id = data[0]
    text = data[1]
    return jsonify({'id': id, 'text': text})


@app.route('/get_free_texts', methods=['GET'])
def get_free_text():
    data = my_db.get_220_free_texts_id()
    return jsonify({'data': data})



if __name__ == '__main__':
   app.run()