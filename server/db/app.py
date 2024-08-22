# import json
# from datetime import datetime

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# from marshmallow import Schema, ValidationError, fields

app = Flask(__name__)
ma = Marshmallow(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.URL, nullable=False)
    price = db.Colmn(db.Integer, nullable=False)
    price_without_sale = db.Colmn(db.Integer, nullable=False)


items_schema = Item(many=True)


@app.route('/get_items')
def get_items():
    items = Item.query.all()

    return items_schema.dump(items)
