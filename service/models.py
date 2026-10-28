from enum import Enum
from service import db


class Category(str, Enum):
    UNKNOWN = "Unknown"
    CLOTHS = "Cloths"
    FOOD = "Food"
    HOUSEWARES = "Housewares"


class Product(db.Model):
    """A product stored in the database."""
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="")
    price = db.Column(db.Float, nullable=False, default=0.0)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.String(40), nullable=False, default=Category.UNKNOWN.value)

    def __init__(self, name, description="", price=0.0, available=True, category=Category.UNKNOWN.value, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = float(price)
        self.available = bool(available)
        self.category = category.value if isinstance(category, Category) else str(category)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {"id": self.id, "name": self.name, "description": self.description,
                "price": self.price, "available": self.available, "category": self.category}

    def deserialize(self, data):
        for key in {"name", "description", "price", "available", "category"}.intersection(data or {}):
            value = data[key]
            if key == "price":
                value = float(value)
            elif key == "available":
                value = value.lower() in ("true", "1", "yes", "on") if isinstance(value, str) else bool(value)
            elif key == "category" and isinstance(value, Category):
                value = value.value
            setattr(self, key, value)
        return self

    @classmethod
    def find(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(name)).all()

    @classmethod
    def find_by_category(cls, category):
        category = category.value if isinstance(category, Category) else str(category)
        return cls.query.filter_by(category=category).all()

    @classmethod
    def find_by_availability(cls, available):
        if isinstance(available, str):
            available = available.lower() in ("true", "1", "yes", "on")
        return cls.query.filter_by(available=bool(available)).all()
