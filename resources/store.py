from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, store_name):
        store = StoreModel.find_by_name(store_name)
        if store:
            return store.json()
        return {'message': 'no store with that name exists'}, 404

    def post(self, store_name):
        if StoreModel.find_by_name(store_name):
            return {'message': 'store {} already exists'.format(store_name)}, 400
        new_store = StoreModel(store_name)
        try:
            new_store.save_to_db()
        except:
            return {'message': "couldn't create a store, we're sorry about that ! try after sometime "}, 500
        return new_store.json(), 201  # 201 successful creation

    def delete(self, store_name):  # delete or do nothing if the store doesn't exist
        store = StoreModel.find_by_name(store_name)
        if store:
            store.delete_from_db()
            return {'message': "store deleted successfully"}, 200


class StoreList(Resource):
    def get(self):
        return {'store': [store.json() for store in StoreModel.query.all()]}
