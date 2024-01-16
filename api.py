import json
from flask import Flask, jsonify, request

app = Flask(__name__)

text = open('text.txt', 'r', encoding='UTF-8').read()

def from_txt(text_file):
    text = open(text_file, 'r', encoding='UTF-8').read()
    text = text.replace('\n', ' ')
    text = text.replace(' ', '')
    tests = text.split('។')
    return tests


@app.route('/get_text', methods=['GET'])
def get_text():
 return jsonify({'text': from_txt('khmerText.txt')})


if __name__ == '__main__':
   app.run(host="0.0.0.0")