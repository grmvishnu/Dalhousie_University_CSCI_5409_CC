from flask import Flask
from flask import request
from flask import Response
from flask_mysqldb import MySQL
import json
import boto3
import base64
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "ProductionDB"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session(
        aws_access_key_id = 'ASIAUMQG3ZW5O3I5KJLQ',
        aws_secret_access_key = 'OrobQfMumqP4GfRjULh47IwzPIASC8Xov0xQQEXH',
        aws_session_token = 'FwoGZXIvYXdzEIP//////////wEaDCsu0/UoUrMC1hMuviLAAXFdjAcwpF+ZPITT+NGJ5zMxIZCaLjwznhDncuV6GrDwG+03KkWMC9pNlRPMrA03Q4caFuFzTk3E8Lz78Ccqs7QQ3HKRxhFAWuG9lxoexx5FWftfqPixeMVw8DTdz1DP4FUF8nSQcBC7ZZ31m/t4JRbqdotZAmmnUbIGJSSGLP1xb1rhMEfc+rj2AwyV+HozGwkU8nBUSOdg/1qwOKkIdAAODz6smD5JRvAtF+tckhZ+9FDlw6er5GnKdsMfIfTf9yiD/ZOSBjIt8SDhWzSvmOJE7Gccx5kLn0tIfkzgj8lfNGDUc7WDr/xJTI1Q5a8Oov/2PrS6'
    )
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

app = Flask(__name__)

jsonObject = get_secret()
app.config['MYSQL_HOST'] = 'database-2.cluster-cgxi1b48h8xw.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = jsonObject['DBUserName']
app.config['MYSQL_PASSWORD'] = jsonObject['DBPassword']
app.config['MYSQL_DB'] = 'tutorial'
mySQL = MySQL(app)

@app.route('/storestudents', methods=['POST'])
def storeStudents():
    inputFromPost = json.loads(request.data)
    if ("students" in inputFromPost) and len(inputFromPost['students']) > 0:
        connectToMysql = mySQL.connection.cursor()
        for student in inputFromPost['students']:
            query = ("Insert into students (first_name, last_name, banner) values (%s, %s, %s)")
            row = (student['first_name'], student['last_name'], student['banner'])
            connectToMysql.execute(query, row)
        connectToMysql.connection.commit()
        connectToMysql.close()
        return Response(status=200)
    else:
        return Response("No data found", status=400)

@app.route('/liststudents', methods=['GET'])
def getStudents():
    connectToMysql = mySQL.connection.cursor()
    table_header = "First_Name" + "&ensp;" + "Last_Name" + "&ensp;" + "Banner" + "<br>"
    connectToMysql.execute("Select * from students;")
    records = connectToMysql.fetchall()
    student_details = ""
    for student in records:
        student_details += student[0] + "&ensp;" + student[1] + "&ensp;" + student[2] + "<br>"
#        student_details += student[0] + student[1] + student[2]
    return table_header+student_details