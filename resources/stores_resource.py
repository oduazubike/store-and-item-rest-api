from flask_restful import Resource
from models.store_model import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"Message": "Store not found"}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"Message": f"Store with the name '{name}' already exist"}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"Message": "An error occurred while trying to insert this to the database"}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"Message": "Item Deleted"}
        return {"Message": "The store you tried to delete does not exist"}


class StoresList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}

