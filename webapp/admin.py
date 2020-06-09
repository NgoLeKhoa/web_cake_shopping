from webapp import app
from flask import request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from .library.models import *
from .library.forms import *
from .library.controllers import *

login = LoginManager(app)
admin = Admin(app, name="Database Management", template_mode="bootstrap3")


@login.user_loader
def load_user(id):
    query = Session.query(Administration).filter(Administration.id == id).first()
    return query


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


@app.route("/admin/login", methods=["GET", "POST"])
def index():
    message = ""
    form = FormAdminLogin(request.form)
    if form.validate_on_submit():
        admin_login = (
            Session.query(Administration)
            .filter(
                Administration.Username == form.Username.data
                and Administration.Password == form.Password.data
            )
            .first()
        )
        if admin_login:
            login_user(admin_login)
            return redirect(url_for("admin.index"))
        else:
            message = "Username or Password is wrong !!!!"
    return render_template("admin/login.html", form=form, message=message)


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect(url_for("index"))

class ProductView(MyModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    page_size = 15

class OrderView(MyModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_edit = False
    can_export = True
    page_size = 15
    # column_list = ("ID", "Order_Date","Customer_ID", "Delivery_Information", "Orders_List")

class CustomerView(MyModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_edit = False
    can_export = True
    page_size = 15


class FeedbackView(MyModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_edit = False
    can_export = True
    page_size = 15


admin.add_view(ProductView(Product, Session))
admin.add_view(OrderView(Order, Session))
admin.add_view(CustomerView(Customer, Session))
admin.add_view(FeedbackView(Feedback, Session))
admin.add_view(LogoutView(name="Logout"))

if __name__ == "__main__":
    app.run(debug=True)
