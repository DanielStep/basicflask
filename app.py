from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from typing import List, Dict, Union

app = Flask(__name__)
api = Api(app)

stores: List = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

items: List = []


class Item(Resource):
    def get(self, name: str):
        result = self.getItem(name)
        return {'item': result}, 200 if result is not None else 404

    def post(self, name: str):
        if self.getItem(name) is not None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = request.get_json()
        result: Dict = {'name': name, 'price': data['price']}
        items.append(result)
        return result, 201

    def getItem(self, name: str):
        return next(
            filter(lambda item: item['name'] == name, items),
            None
        )


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



app.run(port=5000, debug=True)
