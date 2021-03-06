import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.items_resource import Item, ItemsList
from resources.user_resource import UserRegister, UserLogin
from resources.stores_resource import Store, StoresList

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
api = Api(app)


jwt = JWTManager(app)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserLogin, '/login')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoresList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)

# 'sqlite:///database.db'
