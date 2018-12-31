from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_price', type=float, required=True, help='this field cannot be blank')
    parser.add_argument('store_id', type=int, required=True, help='every items needs a store id')

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, item_name):
        if ItemModel.find_by_name(item_name):
            return {'message': 'An item with name {} already exists'.format(item_name)}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(item_name, **data)  # or data['item_price'], data['store_id']
        try:
            new_item.save_to_db()
        except:
            return {"message": "An Error occurred inserting the Item"}, 500  # internal server error
        return new_item.json(), 201  # 201 is when something is successfully created

    def put(self, item_name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)
        if item is None:
            item = ItemModel(item_name, **data)  # or data['item_price'], data['store_id']
        else:
            item.item_price = data['item_price']
        item.save_to_db()
        return item.json()

    def delete(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            item.delete_from_db()
            return {'message': 'Item Deleted Successfully'}
        return {'message': 'No such item exists in the database'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
