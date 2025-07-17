from sqlalchemy import Column, Integer, String, Float, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from . import db

# Ассоциативная таблица для связи многие-ко-многим между продуктами и категориями
product_category = Table(
    'product_category',
    db.Model.metadata,
    Column('product_id', Integer, ForeignKey('products.id', ondelete='CASCADE')),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'))
)

class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    image_url = Column(String)
    on_main = Column(Boolean)

    categories = relationship(
        "Category",
        secondary=product_category,
        back_populates="products"
    )

    def __repr__(self):
        return f"<Product id={self.id} name={self.name}>"

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship(
        "Product",
        secondary=product_category,
        back_populates="categories"
    )

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"
