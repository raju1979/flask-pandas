from flask import request, jsonify
from flask_restful import Resource, Api, reqparse
from flask import current_app as app
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import pandas as pd
import hashlib, binascii, os
import pymongo

from bson import json_util, ObjectId
import json

parser = reqparse.RequestParser()

userParser = reqparse.RequestParser()
userParser.add_argument('username', help = 'This field cannot be blank', required = True)
userParser.add_argument('password', help = 'This field cannot be blank', required = True)

todos = {}

file_name = "https://raw.githubusercontent.com/rajeevratan84/datascienceforbusiness/master/titanic.csv"

class TodoSimple(Resource):
    def get(self, todo_id):
        if todo_id in todos:
            return {todo_id: todos[todo_id]}
        else:
            return {todo_id: "no"}  , 404          

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

class TitanicGetAllRecords(Resource):
    @jwt_required
    def post(self):
        print("in post")
        new_x = request.get_json()
        print(new_x)
        json_output = get_pandas_csv_data()
        return {'output': json.loads(json_output)}, 200

class TatanicDescribe(Resource):
    def get(self):
        json_output = get_pandas_describe_data()
        return {'output': json.loads(json_output)}, 200

class UserLogin(Resource):
    def post(self):
        req = request.get_json()
        username = req['username']
        usrpass = req['password']
        user_collection = app.mydb['users']

        # Check username in db
        if user_collection.count_documents({"name": username}) == 0:
            return {"message":"User doesnt exists / Invalid Credentials"}, 400

        user = user_collection.find_one({"name": username})
        hashed_pass = hash_password(usrpass)
        pass_match = verify_password(user['pass'], usrpass)
        if(pass_match == False):
            return {"message":"User doesnt exists / Invalid Credentials"}, 400

        # data = userParser.parse_args()
        access_token = create_access_token(identity=req['username'])
        print(access_token)
        return {"login": "Success", "token": access_token}, 200

class TitanicGetColumnsName(Resource):
    @jwt_required
    def get(self):
        df = read_csv_via_pandas()
        print(df.columns)
        return {"total_columns": list(df.columns.values)}

class UserRegistration(Resource):
    def post(self):
        req = request.get_json()
        username = req['username']
        usrpass = req['password']
        hashed_pass = hash_password(usrpass)
        user_collection = app.mydb['users']
        print(user_collection.count_documents({"name": username}))
        if user_collection.count_documents({"name": username}) != 0:
            return {"message":"User already exists"}, 400
        user = user_collection.insert_one({"name": username, "pass": hashed_pass}).inserted_id
        created_id = json.loads(json_util.dumps(user))
        print(created_id)
        return {"user": created_id}, 200

def get_pandas_csv_data():    
    df = pd.read_csv(file_name,  converters={'json_column_name': eval})
    out = df.to_json(orient='records')
    return out

def get_pandas_describe_data():
    df = pd.read_csv(file_name,  converters={'json_column_name': eval})
    out = df.describe()
    json_out = out.to_json()
    return json_out


def read_csv_via_pandas():
    df = pd.read_csv(file_name,  converters={'json_column_name': eval})
    return df

# Password hashing function
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
