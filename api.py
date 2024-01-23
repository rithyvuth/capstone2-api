import json
from flask import Flask, jsonify, request, render_template
import my_db

app = Flask(__name__)

text = open('text.txt', 'r', encoding='UTF-8').read()

def from_txt(text_file):
    text = open(text_file, 'r', encoding='UTF-8').read()
    text = text.replace('\n', ' ')
    text = text.replace(' ', '')
    tests = text.split('។')
    return tests


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_text', methods=['GET', 'POST'])
def add_text():
    if request.method == 'POST':
        text = request.form['text']
        my_db.insert(text)
        return jsonify({'status': 'ok'})
    return render_template('add_text.html')
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


if __name__ == '__main__':
   app.run(host="0.0.0.0")