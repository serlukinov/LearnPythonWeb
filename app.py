import os
from flask import Flask, render_template, url_for
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup

app = Flask(__name__)


@app.route("/")
def index():
    return "Learn Pyton"


if __name__ == "__main__":
    app.run()
