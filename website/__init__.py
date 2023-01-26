from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'database.db'

def page_not_found(e):
  return render_template('404.html')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '!directors directors are no fun!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    app.register_error_handler(404, page_not_found)

    from .models import Director
    with app.app_context():
        db.create_all()

    return app