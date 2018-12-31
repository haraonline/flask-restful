from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(120))
    items = db.relationship('ItemModel', lazy='dynamic')  # back reference. learn about lazy = dynamic

    def __init__(self, store_name):
        self.store_name = store_name

    def json(self):
        return {'store_name': self.store_name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, store_name):
        return cls.query.filter_by(store_name=store_name).first()

    # both insert and update. upsert
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):  # item is a dictionary here
        db.session.delete(self)
        db.session.commit()
