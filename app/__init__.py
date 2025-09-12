from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
  
    app.config["SECRET_KEY"] =os.getenv("SECRET_KEY","a_random_secret_key_123456789")
    app.config["SQLALCHEMY_DATABASE_URI"] =os.getenv("DATABASE_URL","sqlite:///app.db")
    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
  
    # اجعل هذا يطابق blueprint.endpoint لمسار تسجيل الدخول
    login_manager.login_view = "app.login"   # أو "auth.login" إذا كان اسم الـ BP "auth"
    # login_manager.login_message_category = "info"  # اختياري للتنبيهات

    # تسجيل البلوبربنتات
    from app.route import bp  # يفترض أن route.py يعرّف: bp = Blueprint("app", __name__)
    app.register_blueprint(bp)

    from app.models import User

    @app.context_processor
    def inject_user_model():
     return dict(User=User)


    return app

