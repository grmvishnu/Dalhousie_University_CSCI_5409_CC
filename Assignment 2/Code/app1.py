import json
from re import U
from flask import Flask, jsonify, request, session
import boto3
import requests
import flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    # credentials = {}
    # credentials["banner"] = "B00871949"
    # credentials["ip"] = "3.92.210.162"
    credentials = {
        "banner": "B00871849",
        "ip": "54.210.25.167"
    }
    # finalcred = json.dumps(credentials)
    response = requests.post(url = "http://3.88.132.229/begin", json= credentials)
    print(response.text)
    return response.text


@app.route('/storedata', methods=['POST'])
def post():
    try:
        input = request.json
        stringdata = input.get("data")

        boto3session = boto3.Session (
            aws_access_key_id = 'ASIAUMQG3ZW5DQ2JUR4K',
            aws_secret_access_key = 'M/EfUnQWapiR57CBjkwy2hHmfR15/erO1+nLc7qt',
            aws_session_token = 'FwoGZXIvYXdzEA4aDIcyePSlafLoxCoD9iLAAYLh2gCjMdFDTQdZyS0Z75e58Uklwc4RgD9iS0QCWfjc1R4hyRhyGTeMXyYgUBOOiSetEEYNeXL4HS/HC5c1vuhUqeemcY+293SQQiVybg2ywugTssxxOrz3ssToJ2yd5JIwk6MElmNMzZrE6HTeteWmTcYuDnj0UQKO6r/PCBUV9zoPNWU3qwHxao7Khi6yEaMQ8Sk2DZZy2btPNOXttbKyCPCyIHN6TiS0hyTHy5CMOgojujUCr6QnfgcF/DHGjSi55YmRBjItBI4IXpol7sntMw30FZjhFRoR9AF2de9YECHGj+WJcJlUOjpYgJFLgOz1TD8q'          
        )

        s3_resource = boto3session.resource('s3')
        filename = 'data.txt'
        bucket_name = 'grmvdata'

        obj = s3_resource.Object(bucket_name, filename)
        output = obj.put(Body=stringdata)

        url = 'https://grmvdata.s3.amazonaws.com/data.txt'

        result = output.get('ResponseMetadata')

        if result.get('HTTPStatusCode') == 200:
            return jsonify({"s3uri" : url})
            
    except Exception as e:
        print("Exception:")
        print(str(e))
        return 400


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 80, debug = True)

