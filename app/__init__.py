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
  
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "a_random_secret_key_123456789")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
  
    login_manager.login_view = "main.login"
    login_manager.login_message_category = "info"

    # استيراد النماذج بعد تهيئة db
    from app.models import User

    # إعداد user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # تسجيل Blueprints
    from app.route import bp
    app.register_blueprint(bp)

    @app.context_processor
    def inject_user_model():
        return dict(User=User)

    return app