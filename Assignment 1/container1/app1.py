import json
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return "helloWorld!"

@app.route('/definition', methods=['POST'])
def post():
    record = json.loads(request.data)
    if record["word"] and len(record["word"]):
        filteredWord = record["word"].lower().strip()
        data = {"word": filteredWord}
        response = requests.post(url = "http://container2:3000/meaning", json = data)
        return response.json()
    else:
        return {"word": None, "error": "Invalid JSON input."}

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)