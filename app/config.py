import os

basedir = os.path.abspath(os.path.dirname(__file__))  # создаем файл __file__='app.db'

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, '..', 'app.db')  # задаем путь для хранения БД

SECRET_KEY = "dgdfgddfg3g3ug43gj3g03049lkcjkr43r43"

# IMAGE_URL = os.path.join(basedir, 'app/static/images')

SQLALCHEMY_TRACK_MODIFICATIONS = False