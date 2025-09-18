from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"   # 👈 اسم الجدول ثابت
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(30), nullable=False, default='default.png')
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(10), nullable=False)

    shops = db.relationship("Shop", backref="user", cascade="all, delete-orphan")  
    news = db.relationship("News", backref="user", cascade="all, delete-orphan")  
    orders = db.relationship("Order", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Shop(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, unique=True, nullable=False)
    prix = db.Column(db.String(30), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False, default='default.jpg')
    category = db.Column(db.String(20), nullable=False, default='clothing')
    available_colors = db.Column(db.String(200))  
    available_sizes = db.Column(db.String(100))   
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    orders = db.relationship("Order", backref="shop", cascade="all, delete-orphan")

    def get_colors_list(self):
        return self.available_colors.split(',') if self.available_colors else []

    def get_sizes_list(self):
        return self.available_sizes.split(',') if self.available_sizes else []

    def __repr__(self):
        return f"<Shop {self.title}>"


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.String(30), nullable=False, unique=True, default='offer1.jpg')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name="fk_news_user_id"),
        nullable=False
    )

    def __repr__(self):
        return f"<News {self.thumbnail}>"


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50))
    category = db.Column(db.String(20), nullable=True)
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name="fk_order_user_id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Order {self.id}>"
