import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get():
    return "helloWorld!"

@app.route('/meaning', methods=['POST'])
def post():
    jsonObject = json.loads(request.data)
    word = jsonObject["word"]
    dictionaryFile = open("/usr/src/app/resources/dictionary.txt")
    Lines = dictionaryFile.readlines()
    if len(word):
        for line in Lines:
            if line.startswith(word+'='):
                output = {"word": word, "definition": line.split('=')[1].strip("\n")}
                return output
    else:
        output = {"word": None, "error": "Invalid JSON input."}
        return output
    output = {"word": word, "error": "Word not found in dictionary."}
    return output

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 3000, debug = True)