from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item must have a Store")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"Message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"Message": f"An Item with the Name '{name}' already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception:
            return {"Message": "An Error occurred trying to add this item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        return {"Message": "Item Deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            # if item does not exist we create a new item from ItemModel obj
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


