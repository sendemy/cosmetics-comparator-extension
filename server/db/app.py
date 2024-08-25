from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields

from flask import Flask, jsonify, request

app = Flask(__name__)
ma = Marshmallow(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    price_without_sale = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=False)
    delivery_time = db.Column(db.Date, nullable=False)


class ItemSchema(Schema):
    id = fields.String()
    name = fields.String()
    url = fields.String()
    description = fields.String(allow_none=True)
    price = fields.Integer()
    price_without_sale = fields.Float(allow_none=True)
    rating = fields.Float()
    delivery_time = fields.Date()


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@app.route('/get_items')
def get_items():
    items = Item.query.all()

    return items_schema.dump(items)


@app.route('/create_item', methods=['POST'])
def create_item():
    request_data = request.get_json()

    try:
        validated_data = item_schema.load(request_data)
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400

    new_item = Item(name=validated_data['name'],
                    url=validated_data['url'], price=validated_data['price'], price_without_sale=validated_data['price_without_sale'], rating=validated_data['rating'], delivery_time=validated_data['delivery_time'])
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'}), 201


@app.route('/create_items', methods=['POST'])
def create_items():
    request_data = request.get_json()

    try:
        validated_data = items_schema.load(request_data)
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.messages}), 400

    for new_item in validated_data:
        new_item = Item(name=validated_data['name'],
                        url=validated_data['url'], description=validated_data['description'], price=validated_data['price'], price_without_sale=validated_data['price_without_sale'], rating=validated_data['rating'], delivery_time=validated_data['delivery_time'])
        db.session.add(new_item)
        db.session.commit()

    return jsonify({'message': 'Items added successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
