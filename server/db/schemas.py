import datetime

from app import db
from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.String()
    name = fields.String()
    url = fields.URL
    price = fields.Integer()
    price_without_sale = fields.Integer()
