from flask import request, jsonify
from flask_restful import Resource, Api, reqparse

from flask import current_app as app

import json

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import pandas as pd

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
        print(req['username'])
        data = userParser.parse_args()
        access_token = create_access_token(identity=req['username'])
        print(access_token)
        return {"login": "Success", "token": access_token}, 200

class TitanicGetColumnsName(Resource):
    @jwt_required
    def get(self):
        df = read_csv_via_pandas()
        print(df.columns)
        return {"total_columns": list(df.columns.values)}



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
