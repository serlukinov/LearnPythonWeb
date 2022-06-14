from flask import Flask, render_template
from app.model import db, Track

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py') #указываем откуда брать параметры конфигурации
    db.init_app(app) #инициализируем базу данных


    @app.route("/")
    def index():
        title = "Learn Python Web"
        return render_template('index.html', page_title=title)

    return app



