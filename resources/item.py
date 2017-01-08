# from flask_restful import Resource, reqparse
# from flask_jwt import JWT, jwt_required
# from models.item import ItemModel
# from db import db
#
#
# class ItemModel(db.Model):
#     __tablename__ = 'items'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))
#     price = db.Column(db.Float(precision=2))
#
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
#     store = db.relationship('StoreModel')
#
#     def __init__(self, name, price, store_id):
#         self.name = name
#         self.price = price
#         self.store_id = store_id
#
#     def json(self):
#         return {'name': self.name, 'price': self.price}
#
#     @classmethod
#     def find_by_name(cls, name):
#         return cls.query.filter_by(name=name).first()
#
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
#
# class ItemList(Resource):
#     def get(self):
#         return {'items': [item.json() for item in ItemModel.query.all()]}
#         # above is best if working primarily in
#         # python...otherwise see below
#         # return {'items': list(map(lambda x: x.json(), ItemModel.querty.all()))}





from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}