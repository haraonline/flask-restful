from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120))
    item_price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, item_name, item_price, store_id):
        self.item_name = item_name
        self.item_price = item_price
        self.store_id = store_id

    def json(self):
        return {'item_name': self.item_name, 'price': self.item_price}

    @classmethod
    def find_by_name(cls, item_name):
        return cls.query.filter_by(item_name=item_name).first()

    # both insert and update. upsert
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):  # item is a dictionary here
        db.session.delete(self)
        db.session.commit()
