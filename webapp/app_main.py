from webapp import app
from flask import render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from flask_ckeditor import CKEditor
from .library.controllers import *
from .library.models import *
from .library.forms import *
from sqlalchemy.orm import sessionmaker

Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
Session = DBsession()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""
app.config["MAIL_DEFAULT_SENDER"] = ""
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)
ckeditor = CKEditor(app)


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def page_index():
    customer_login = ""
    if session.get("session_Customer"):
        customer_login = session["session_Customer"]
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)
    return render_template(
        "index.html", login_or_logout_HTML_string=login_or_logout_HTML_string
    )


@app.route("/shop", methods=["GET", "POST"])
def page_shop():
    # Khởi tạo biến:
    total_quantity = 0
    customer_login = ""
    selected_products_list = []
    total_price = 0

    # Kiểm tra khách hàng đănh nhập:
    customer_login = ""
    if session.get("session_Customer"):
        customer_login = session["session_Customer"]
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)

    # Lấy danh sách sản phẩm:
    PRODUCTS_LIST = get_products_list()

    # Lấy danh sách phân loại sản phẩm:
    category_products_list = get_category_product_list()
    for values in category_products_list.values():
        total_quantity += values

    # Kiểm tra danh sách sản phẩm chọn:
    if session.get("session_Cart"):
        selected_products_list = session["session_Cart"]["Cart"]

    # Xử lý thêm sản phẩm vào giỏ hàng:
    if request.form.get("shop_tps_ID") is not None:
        _id = int(request.form.get("shop_tps_ID"))
        _quantity = int(request.form.get("shop_tps_Quantity"))
        selected_product = get_selected_product(PRODUCTS_LIST, _id)
        _price = _quantity * selected_product["Unit_Price"]
        old_selected_product = get_selected_product(selected_products_list, _id)
        if old_selected_product is not None:
            old_quantity = old_selected_product["Quantity"]
            _quantity += old_quantity
            _price = _quantity * old_selected_product["Unit_Price"]
            selected_products_list.remove(old_selected_product)

        selected_product["Quantity"] = _quantity
        selected_product["Price"] = _price
        selected_products_list.append(selected_product)
        session["session_Cart"] = {"Cart": selected_products_list}

    # Xử lý thay đổi hoặc xóa sản phẩm trong giỏ hàng:
    if request.form.get("shop_tps_ID_1") is not None:
        _id_1 = int(request.form.get("shop_tps_ID_1"))
        _quantity_1 = int(request.form.get("shop_tps_Quantity_1"))
        selected_product = get_selected_product(selected_products_list, _id_1)

        # Loại bỏ sản phẩm đang thực hiện ra khỏi danh sách chọn:
        if selected_product is not None:
            selected_products_list.remove(selected_product)

            # Cập nhật lại số lượng sản phẩm:
            if _quantity_1 > 0:
                selected_product["Quantity"] = _quantity_1
                selected_product["Price"] = _quantity_1 * selected_product["Unit_Price"]
                selected_products_list.append(selected_product)

        session["session_Cart"] = {"Cart": selected_products_list}

    for selected_product in selected_products_list:
        total_price += selected_product["Price"]

    # login_or_logout_string = create_login_or_logout_string(customer_login)
    return render_template(
        "shop.html",
        PRODUCTS_LIST=PRODUCTS_LIST,
        category_products_list=category_products_list,
        total_quantity=total_quantity,
        selected_products_list=selected_products_list,
        total_price=total_price,
        login_or_logout_HTML_string=login_or_logout_HTML_string,
    )


@app.route("/login", methods=["GET", "POST"])
def page_login():
    customer_login = ""
    if session.get("session_Customer"):
        return redirect(url_for("page_shop"))

    if session.get("session_Customer"):
        customer_login = session["session_Customer"]
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)

    Customer_List = get_customers_list()
    _Email = ""
    _Password = ""
    Alarm_string = ""
    form = FormLogin(request.form)
    if form.validate_on_submit():
        _Email = form.Email.data
        _Password = form.Password.data
        customer_login = login_customer(Customer_List, _Email, _Password)
        if customer_login is not None:
            session["session_Customer"] = customer_login
            return redirect(url_for("page_index"))
        else:
            Alarm_string = "Email or Password is wrong!"
    return render_template(
        "login.html",
        form=form,
        Alarm_string=Alarm_string,
        login_or_logout_HTML_string=login_or_logout_HTML_string,
    )


@app.route("/logout", methods=["GET", "POST"])
def page_logout():
    session["session_Customer"] = None
    return redirect(url_for("page_login"))


@app.route("/signup", methods=["GET", "POST"])
def page_signup():
    customer_login = ""
    if session.get("session_Customer"):
        customer_login = session["session_Customer"]
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)

    form = FormSignup(request.form)
    if form.validate_on_submit():
        customer = {
            "Name": form.Name.data,
            "Username": form.Username.data,
            "Email": form.Email.data,
            "Password": form.Password.data,
            "Phone": form.Phone.data,
            "Address": form.Address.data,
        }
        if add_new_customer(customer):
            print("success")
            return redirect(url_for("page_shop"))
        else:
            print("failed")
    return render_template(
        "signup.html",
        form=form,
        login_or_logout_HTML_string=login_or_logout_HTML_string,
    )


@app.route("/cart", methods=["GET", "POST"])
def page_cart():
    total_price = 0
    selected_products_list = []

    # Kiểm tra trạng thái của giỏ hàng:
    if session.get("session_Cart"):
        selected_products_list = session["session_Cart"]["Cart"]

    # Kiem tra khach hang danh nhap:
    if session.get("session_Customer"):
        customer_login = session["session_Customer"]

        # Cập nhật giỏ hàng
        if request.form.get("cart_tps_ID"):
            _id = int(request.form.get("cart_tps_ID"))
            _quantity = int(request.form.get("cart_tps_Quantity"))
            selected_product = get_selected_product(selected_products_list, _id)

            # Loại bỏ sản phẩm đang thực hiện ra khỏi danh sách chọn:
            if selected_product is not None:
                selected_products_list.remove(selected_product)

                # Cập nhật lại số lượng sản phẩm:
                if _quantity > 0 and selected_product is not None:
                    selected_product["Quantity"] = _quantity
                    selected_product["Price"] = (
                        _quantity * selected_product["Unit_Price"]
                    )
                    selected_products_list.append(selected_product)

            session["session_Cart"] = {"Cart": selected_products_list}
    else:
        # Neu chua dang nhap thi chuyen huong sang trang login
        return redirect(url_for("page_login"))

    # In ra tổng tiền cần thanh toán
    for selected_product in selected_products_list:
        total_price += selected_product["Price"]

    # Chuỗi đăng nhập - đăng xuất:
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)

    # Chuyển tiếp trang
    if request.form.get("cart_tps_preceed_to_checkout_btn") == "success":
        return redirect(url_for("page_checkout"))

    return render_template(
        "cart.html",
        selected_products_list=selected_products_list,
        total_price=total_price,
        login_or_logout_HTML_string=login_or_logout_HTML_string,
    )


@app.route("/checkout", methods=["GET", "POST"])
def page_checkout():
    # Khởi tạo biến:
    msg = ""
    message = ""
    orders_list = []
    selected_products_list = []
    total_price = 0
    customer_login = ""

    if session.get("session_Cart"):
        selected_products_list = session["session_Cart"]["Cart"]

    for selected_product in selected_products_list:
        total_price += selected_product["Price"]

    if session.get("session_Customer"):
        customer_login = session["session_Customer"]
        if request.form.get("checkout_tps_Name"):
            delivery_information = {
                "Name": request.form.get("checkout_tps_Name"),
                "Phone": request.form.get("checkout_tps_Phone"),
                "Address": request.form.get("checkout_tps_Delivery_Address"),
                "Message": request.form.get("checkout_tps_Message"),
            }
            if request.method == "POST":
                for selected_product in selected_products_list:
                    selected_product_dict = {
                        "ID": selected_product["ID"],
                        "Name": selected_product["Name"],
                        "Code": selected_product["Code"],
                        "Quantity": selected_product["Quantity"],
                        "Price": selected_product["Price"],
                    }
                    orders_list.append(selected_product_dict)
                order = {
                    "Order_Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "Customer_ID": int(request.form.get("checkout_tps_Customer_ID")),
                    "Delivery_Information": delivery_information,
                    "Orders_List": orders_list,
                }
                if add_new_order(order):
                    msg = Message("Thank you for ordering")
                    msg.body = (
                        "Our ordering system has recorded your orders at "
                        + order["Order_Date"]
                        + ". The total price of your order is "
                        + str(total_price)
                        + ".00 dollars. Please prepare small denomination cash for convenience. \n"
                        + "We are going to deliver within 2 hours. Have a nice day."
                    )
                    msg.recipients = [customer_login["Email"]]
                    mail.html = msg
                    mail.send(msg)
                    session.pop("session_Cart", None)
                    message = "Your order list is placed successfully"

    # Chuỗi đăng nhập - đăng xuất:
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)

    return render_template(
        "checkout.html",
        customer_login=customer_login,
        selected_products_list=selected_products_list,
        total_price=total_price,
        message=message,
        login_or_logout_HTML_string=login_or_logout_HTML_string,
    )


@app.route("/contact", methods=["GET", "POST"])
def page_contact():
    customer_login = ""
    if session.get("session_Customer"):
        customer_login = session["session_Customer"]
    login_or_logout_HTML_string = create_login_or_logout_HTML_string(customer_login)

    message = ""
    form = FormContact(request.form)
    if form.validate_on_submit():
        feedback = {
            "Name": form.Name.data,
            "Email": form.Email.data,
            "Subject": form.Subject.data,
            "Details": form.Details.data,
        }
        if add_new_feedback(feedback):
            msg = Message("Thank you for your feedback")
            msg.body = "We are happy to hear from you. We will try to serve better. Thank you and have a nice day."
            msg.recipients = [feedback["Email"]]
            mail.html = msg
            mail.send(msg)
            message = "Your message is sent successfully"
        else:
            message = "Oop!! Your message is sent unsuccessfully"
    return render_template(
        "contact.html",
        form=form,
        message=message,
        login_or_logout_HTML_string=login_or_logout_HTML_string,
    )


if __name__ == "__main__":
    app.run(debug=True)
