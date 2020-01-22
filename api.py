from flask import Flask
from flask_restful import Resource, Api

from routes import todo_route

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from flask_pymongo import PyMongo
from pymongo import MongoClient
import pymongo
import argparse
import json
from flask_cors import CORS

with open('config.json') as config_file:
    config_data = json.load(config_file)

# # Construct the argument parser
# ap = argparse.ArgumentParser()
# ap.add_argument("-s", "--secret", required=True,
#    help="JWT SECRET")

# args = vars(ap.parse_args())
# print(args['secret'])

app = Flask(__name__)
CORS(app)
# JWT secret  configuration
secret_settings = config_data['secret']
app.config.update(secret_settings)

app.config['JWT_SECRET_KEY'] = app.config['secret']
jwt = JWTManager(app)

mongo_url = config_data['MONGO_URI']
app.config.update(mongo_url)

app.config["MONGO_URI"] = app.config['MONGO_URI']
# mongo = PyMongo(app)
# print(app.config)
global mydb
myclient = MongoClient(app.config['MONGO_URI'])
app.mydb = myclient["flask-pandas"]


api = Api(app)

api.add_resource(todo_route.TodoSimple, '/titanic/<string:todo_id>')
api.add_resource(todo_route.TitanicGetAllRecords, '/titanic/all')
api.add_resource(todo_route.TatanicDescribe, '/titanic/describe')
api.add_resource(todo_route.UserLogin, '/login')
api.add_resource(todo_route.TitanicGetColumnsName, '/titanic/columns')
api.add_resource(todo_route.UserRegistration, '/registration')

if __name__ == '__main__':
    app.run(debug=True)