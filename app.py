from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList  # need for creating tables using db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '#Flask$RESTful*'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # localhost:5000/auth

api.add_resource(Item, '/item/<string:item_name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

api.add_resource(Store, '/store/<string:store_name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db  # avoid circular import. that's why importing here
    db.init_app(app)
    app.run(port=5000, debug=True)
