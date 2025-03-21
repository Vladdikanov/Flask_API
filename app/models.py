from app import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    product = relationship("Product", back_populates="category")

    def __repr__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category", back_populates="product")
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return self.name


class Sale(db.Model):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    # discount = Column(Numeric(100,2), nullable=True)
    date = Column(Date, nullable=False)
    product = relationship("Product", back_populates="sales")
