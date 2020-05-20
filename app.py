import os
from flask import Flask
from scraper import *

app = Flask(__name__)

# home page
@app.route('/<question>', methods=['GET'])
def home():
    answer = solution(question)
    print(answer)
    return answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    app.debug = True
    app.run(debug=True)
    app.debug = True