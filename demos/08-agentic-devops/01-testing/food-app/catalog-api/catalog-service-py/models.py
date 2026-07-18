from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal

db = SQLAlchemy()

class CatalogItem(db.Model):
    __tablename__ = 'catalog_item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(18, 4), nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    picture_url = db.Column(db.String(255))
    description = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'inStock': self.in_stock,
            'pictureUrl': self.picture_url,
            'description': self.description
        }
    
    def from_dict(self, data):
        self.name = data.get('name', self.name)
        self.price = Decimal(str(data.get('price', self.price)))
        self.in_stock = data.get('inStock', self.in_stock)
        self.picture_url = data.get('pictureUrl', self.picture_url)
        self.description = data.get('description', self.description)
        return self
