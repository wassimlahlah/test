from . import db,login_manager
from flask_login import UserMixin
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image=db.Column(db.String(30),nullable=False,default='default.png')
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    shops = db.relationship("Shop", backref="user")
     
    def __repr__(self):
        return f"<User {self.username}>"

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text,unique=True, nullable=False)
    prix = db.Column(db.String(30), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False, default='default.jpg')
    category = db.Column(db.String(20), nullable=False, default='clothing')
    available_colors = db.Column(db.String(200))  # تخزين الألوان كسلسلة مفصولة بفواصل
    available_sizes = db.Column(db.String(100))   # تخزين الأحجام كسلسلة مفصولة بفواصل
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # علاقة بالمستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def get_colors_list(self):
        """ارجاع قائمة الألوان"""
        if self.available_colors:
            return self.available_colors.split(',')
        return []

    def get_sizes_list(self):
        """ارجاع قائمة الأحجام"""
        if self.available_sizes:
            return self.available_sizes.split(',')
        return []

    def __repr__(self):
        return f"<Shop {self.title}>"   
    
class News(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    thumbnail=db.Column(db.String(30),nullable=False,unique=True ,default='offer1.jpg')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_News_user_id"),  # إضافة اسم للمفتاح
        nullable=False
    )
    def __repr__(self):
        return f"<News{self.thumbnail}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50))
    category = db.Column(db.String(20), nullable=True)  # استخدم nullable=True أولاً
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship("Shop", backref="orders")
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_order_id"),  # إضافة اسم للمفتاح
        nullable=False
    )
    def __repr__(self):
        return f"<Order{self.id}>"
    
