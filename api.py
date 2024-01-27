import json
from flask import Flask, jsonify, request, render_template
import my_db
import khmernltk
import text_normalization

app = Flask(__name__)

# text = open('text.txt', 'r', encoding='UTF-8').read()

def from_txt(text_file):
    # text = open(text_file, 'r', encoding='UTF-8').read()
    text = text_file
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = text.replace('៕', '។')
    text = text.replace('។។', '។')
    text = text.replace(' ', '')
    tests = text.split('។')
    return tests


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

        # Process the file content (you can add your logic here)
        # For now, just print the content
        return jsonify({'text': from_txt(file_content)})

        # Save the file to a folder (you may want to check for secure filename)
    
    return render_template('add_text.html', message='បានបញ្ចូលប្រភេទអត្ថបទជាថ្មីបានជោគជ័យ')
    # text = request.form['text']
    # return jsonify({'text': text})

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

@app.route('/saved_text/<id>', methods=['POST'])
def saved_text(id):
    my_db.update_status(id, 'saved')
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