from flask import Flask
import webapp

app = Flask(__name__)
app.config["SECRET_KEY"] = "a_hard_to_guess_secret_key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import webapp.admin
import webapp.app_main