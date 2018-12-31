import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='this field cannot be empty')
    parser.add_argument('password', type=str, required=True, help='this field cannot be empty')

    def post(self):
        data = UserRegister.parser.parse_args()  # data from json payload
        # check if user already exists
        if UserModel.find_by_username(data['username']):
            return {"message": "User with this name already exists"}, 400

        user = UserModel(**data)  # unpack the data dictionary
        user.save_to_db()
        return {"message": "user created successfully"}, 201
