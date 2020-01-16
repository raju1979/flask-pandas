from flask import Flask
from flask_restful import Resource, Api

from routes import todo_route

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import argparse
import json

with open('config.json') as config_file:
    config_data = json.load(config_file)

# # Construct the argument parser
# ap = argparse.ArgumentParser()
# ap.add_argument("-s", "--secret", required=True,
#    help="JWT SECRET")

# args = vars(ap.parse_args())
# print(args['secret'])

app = Flask(__name__)

# JWT secret  configuration
secret_settings = config_data['secret']
app.config.update(secret_settings)

app.config['JWT_SECRET_KEY'] = app.config['secret']
jwt = JWTManager(app)



api = Api(app)

api.add_resource(todo_route.TodoSimple, '/titanic/<string:todo_id>')
api.add_resource(todo_route.TitanicGetAllRecords, '/titanic/all')
api.add_resource(todo_route.TatanicDescribe, '/titanic/describe')
api.add_resource(todo_route.UserLogin, '/login')

if __name__ == '__main__':
    app.run(debug=True)