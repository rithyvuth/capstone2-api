import json
from flask import Flask, jsonify, request, render_template
import my_db
import khmernltk
import text_normalization
import os

app = Flask(__name__)

# text = open('text.txt', 'r', encoding='UTF-8').read()

def from_txt(text_file):
    # text = open(text_file, 'r', encoding='UTF-8').read()
    text = text_file.split('។')
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
        if not os.path.exists('upload'):
            os.mkdir('upload')
        if not os.path.exists('upload/raw'):
            os.mkdir('upload/raw')
        if not os.path.exists('upload/normalized'):
            os.mkdir('upload/normalized')            
        open('upload/raw/' + file.filename, 'w', encoding='UTF-8').write(file_content)
        
        texts = from_txt(file_content)
        open('upload/normalized/' + file.filename, 'w', encoding='UTF-8').write('\n'.join(texts))
        for text in texts:
            my_db.insert(text, file.filename)

        return render_template('add_text.html', message='ការបញ្ចូលបានជោគជ័យ')

    
    return render_template('add_text.html', message='ការបញ្ចូលបរាជ័យ')

@app.route('/text_normalize', methods=['GET']) 
def text_normalize():
    return render_template('text_normalization.html')  

@app.route('/text_normalize', methods=['POST'])
def text_normalize_post():
    text = request.form['text']
    text = text_normalization.text_normalize(text)
    return jsonify({'text': text})


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
def saved_text(id):
    id = request.form['id']
    wav_name = request.form['name']
    my_db.update_status(id, 'saved', wav_name)
    return jsonify({'status': 'ok'})

@app.route('/get_all_texts', methods=['GET'])
def get_all_texts():
    data = my_db.get_all_texts()
    return jsonify({'data': data})


@app.route('/test_get_text', methods=['GET'])
def test_get_text():
    
    return jsonify({'text': my_db.test_get_text()[1], 'id': my_db.test_get_text()[0]})

if __name__ == '__main__':
   app.run()