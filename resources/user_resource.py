import hmac

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from models.user_model import UserModel


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and hmac.compare_digest(user.password, data["password"]):

            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token
            }, 200

        return {"Message": "Invalid credentials"}, 401  # unauthorised


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):  # that is, if not None
            return {"Message": "A User with the Username already exists"}, 400  # Bad request

        user = UserModel(**data)
        user.save_to_db()

        return {"Message": "User Created"}, 201

