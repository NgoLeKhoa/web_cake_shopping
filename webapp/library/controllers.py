import json
import os
from datetime import datetime
from .models import *
from flask import redirect, url_for, Markup

def get_products_list():
    PRODUCTS_LIST = []
    q_Products_List = Session.query(Product).all()
    for product in q_Products_List:
        product_dict = {
            "ID": product.ID,
            "Code": product.Code,
            "Name": product.Name,
            "Category": product.Category,
            "Image": product.Image,
            "Unit_Price": product.Unit_Price,
            "Created_Date": product.Created_Date,
        }
        PRODUCTS_LIST.append(product_dict)
    return PRODUCTS_LIST

def get_customers_list():
    CUSTOMERS = []
    q_Customers_List = Session.query(Customer).all()
    for customer in q_Customers_List:
        customer_dict = {
            "ID": customer.ID,
            "Name": customer.Name,
            "Username": customer.Username,
            "Email": customer.Email,
            "Password": customer.Password,
            "Phone": customer.Phone,
            "Address": customer.Address,
        }
        CUSTOMERS.append(customer_dict)
    return CUSTOMERS


def get_selected_product(products_list, ID):
    lst = list(filter(lambda product: product["ID"] == ID, products_list))
    if len(lst) == 1:
        selected_product = lst[0]
    else:
        selected_product = None
    return selected_product

def get_category_product_list():
    Products = Session.query(Product).all()
    Product_list = []
    Category_list = {}
    for row in Products:
        Product_list.append((row.Category, ((row.Code)[0] + (row.Code)[1])))
    for Category in sorted(Product_list):
        if Category in Category_list:
            Category_list[Category] += 1
        else:
            Category_list[Category] = 1
    return Category_list


def login_customer(customers_list, email, password):
    lst = list(
        filter(
            lambda customer: customer["Email"] == email
            and customer["Password"] == password,
            customers_list,
        )
    )
    if len(lst) == 1:
        selected_customer = lst[0]
    else:
        selected_customer = None
    return selected_customer

def add_new_customer(customer):
    result = False
    SQLAlchemy_String = Customer(
        Name=customer["Name"],
        Username=customer["Username"],
        Email=customer["Email"],
        Password=customer["Password"],
        Phone=customer["Phone"],
        Address=customer["Address"],
    )
    if SQLAlchemy_String:
        Session.add(SQLAlchemy_String)
        result = True
    Session.commit()
    return result


def add_new_order(order):
    result = False
    SQLAlchemy_String = Order(
        Order_Date=order["Order_Date"],
        Customer_ID=order["Customer_ID"],
        Delivery_Information=json.dumps(
            order["Delivery_Information"], ensure_ascii=False
        ),
        Orders_List=json.dumps(order["Orders_List"], ensure_ascii=False),
    )
    if SQLAlchemy_String:
        Session.add(SQLAlchemy_String)
        print("Order is inserted successfully!")
        result = True
    Session.commit()
    return result

def add_new_feedback(feedback):
    result = False
    SQLAlchemy_String = Feedback(
        Name=feedback["Name"],
        Email=feedback["Email"],
        Subject=feedback["Subject"],
        Details=feedback["Details"],
    )
    if SQLAlchemy_String:
        Session.add(SQLAlchemy_String)
        print("Feedback is inserted successfully!")
        result = True
    Session.commit()
    return result

def create_login_or_logout_HTML_string(customer_login):
    login_or_logout_HTML_string = "<a href='/login'>Login</a>"
    if customer_login != "":
        login_or_logout_HTML_string = "<a href='/logout'>Logout</a>"
    else:
        login_or_logout_HTML_string = "<a href='/login'>Login</a>"
    return Markup(login_or_logout_HTML_string)

def find_product_by_name(find_string, products_list):
    result = list(filter(lambda product: find_string.upper() in product['Name'].upper(), products_list))
    return result
