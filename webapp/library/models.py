from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///webapp/database/demo_api_db.db?check_same_thread=False")
Base = declarative_base()


class Product(Base):
    __tablename__ = "Product"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    Code = Column(String(200), nullable=False)
    Name = Column(String(200), nullable=False)
    Category = Column(String(200), nullable=False)
    Image = Column(String(200), nullable=False)
    Unit_Price = Column(Integer, nullable=False)
    Created_Date = Column(String(200), nullable=False)

    def __repr__(self):
        return "('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            self.ID,
            self.Code,
            self.Name,
            self.Category,
            self.Image,
            self.Unit_Price,
            self.Created_Date,
        )


class Customer(Base):
    __tablename__ = "Customer"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    Name = Column(String(200), nullable=False)
    Username = Column(String(200), nullable=False)
    Email = Column(String(200), nullable=False)
    Password = Column(String(200), nullable=False)
    Phone = Column(String(200), nullable=False)
    Address = Column(String(200), nullable=False)

    def __repr__(self):
        return "('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            self.ID,
            self.Name,
            self.Username,
            self.Email,
            self.Password,
            self.Phone,
            self.Address,
        )


class Order(Base):
    __tablename__ = "Order"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    Order_Date = Column(String(200), nullable=False)
    Customer_ID = Column(Integer, ForeignKey("Customer.ID"))
    Delivery_Information = Column(Text, nullable=False)
    Orders_List = Column(Text, nullable=False)
    relate = relationship(Customer, backref="order")

    def __repr__(self):
        return "('{}', '{}', {}', '{}', '{}')".format(
            self.ID,
            self.Order_Date,
            self.Customer_ID,
            self.Delivery_Information,
            self.Orders_List,
        )


class Feedback(Base):
    __tablename__ = "Feedback"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    Name = Column(String(200), nullable=False)
    Email = Column(String(200), nullable=False)
    Subject = Column(String(200), nullable=False)
    Details = Column(Text, nullable=False)

    def __repr__(self):
        return "('{}', '{}', '{}', '{}')".format(
            self.ID, self.Name, self.Email, self.Message,
        )


class Administration(Base, UserMixin):
    __tablename__ = "Administration"
    id = Column(Integer, autoincrement=True, primary_key=True)
    Name = Column(String(200), nullable=False)
    Username = Column(String(200), nullable=False)
    Password = Column(String(200), nullable=False)

    def __repr__(self):
        return "('{}', '{}', '{}', '{}')".format(
            self.id, self.Name, self.Username, self.Password,
        )


# Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
Session = DBsession()
