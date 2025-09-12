from flask import Blueprint, render_template, url_for, flash, redirect, request,abort
from flask_login import login_required, login_user, current_user, logout_user
from app.formes import RegistrationForm, LoginForm ,ProfileForm,NewShop,NewNews,PurchaseForm,UpdateForm,DeleteForm
from app.models import User,Shop,News,Order
from app import bcrypt, db
import os
from flask import current_app
from PIL import Image
from werkzeug.utils import secure_filename
bp = Blueprint("app", __name__) 


def delete_picture(picture_name,path):
    picture_path=os.path.join(current_app.root_path,path,picture_name)
    try:
        os.remove(picture_path)
    except:
        pass   


def save_picture(form_picture, path, output_size=None):

    picture_name = secure_filename(form_picture.filename)
    
    picture_path = os.path.join(current_app.root_path, path, picture_name)

    
    i = Image.open(form_picture)
    if output_size:
        i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name

@bp.route("/")
@bp.route("/home")
def home():
    return render_template("home.html", title="home")

@bp.route("/shop")
def shop():
    page = request.args.get("page", 1, type=int)
    shops = Shop.query.order_by(Shop.id.desc()).paginate(page=page, per_page=3)
    return render_template("shop.html", title="shop", shops=shops)

@bp.route('/news')
def news():
    news = News.query.order_by(News.id.desc()).all()
    return render_template('news.html', news=news)

@bp.route("/dashbored")
def dashbored():
    if current_user.id != 1:  # غير المالك
        abort(403)  
    tab = request.args.get("tab")   
    return render_template("dashbored.html", title="dashbored", active_tab=tab)

@bp.route("/dashbored/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        # حفظ الصورة إن رُفعت (اختياري)
        if form.image.data:
            picture_file = save_picture(form.image.data, "static/user_pics", output_size=(150, 150))
            current_user.image = picture_file

        # تحديث باقي الحقول دائماً (انتبه إلى .data)
        
        current_user.username = form.username.data
        current_user.email = form.email.data

        # انتبه هنا: استخدم .data
        current_user.number = form.number.data

        db.session.commit()
        flash("Profile updated!", "success")

        # داخل blueprint: استعمل '.' للإشارة إلى نفس البلوبِرنت
        return redirect(url_for("app.profile"))

    # GET: ملء الحقول بقيم المستخدم المسجل (فقط إذا مسجَّل)
    elif request.method == "GET" and current_user.is_authenticated:
        
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.number.data = current_user.number

    # رابط الصورة لعرضها في القالب
    image = url_for("static", filename=f"user_pics/{current_user.image}")

    return render_template("profile.html", title="profile", form=form, image=image,active_tab="profile")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if User.query.first():
        abort(404)

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            number=form.number.data,
            password=hashed_password, 
                 )
        db.session.add(user)
        db.session.commit()
        flash(f"compte créé avec succès pour {form.username.data}", "success")
        return redirect(url_for("app.login"))

    return render_template("register.html", title="register", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("app.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"you have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("app.home"))
        else:
            flash("login unsuccessful", "danger")

    return render_template("login.html", title="login", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("app.home"))




@bp.route("/dashbored/new_shop", methods=["GET", "POST"])
@login_required
def new_shop():
    form = NewShop()
    
    # قائمة الألوان (ثابتة)
    color_options = ["Red","Blue","Green","Black","White"]

    # اختيار الأحجام بناءً على الفئة
    if request.method == "POST":
        category = form.category.data
    else:
        category = "clothing"  # افتراضي

    if category == "shoes":
        size_options = ["36","37","38","39","40","41","42","43"]
    else:
        size_options = ["S","M","L","XL","2XL"]

    if form.validate_on_submit():
        # حفظ الصورة
        if form.thumbnail.data:
            picture_file = save_picture(form.thumbnail.data, "static/thumbnail")
        else:
            picture_file = "default.jpg"

        # جلب الألوان والأحجام المختارة
        selected_colors = request.form.getlist("available_colors")
        selected_sizes = request.form.getlist("available_sizes")

        # التحقق من تكرار العنوان
        existing_shop = Shop.query.filter_by(content=form.content.data).first()
        if existing_shop:
            flash("This content already exists. Please choose another one.", "danger")
            return redirect(url_for("app.new_shop"))

        # إنشاء المتجر
        shop = Shop(
            title=form.title.data,
            content=form.content.data,
            prix=form.prix.data,
            thumbnail=picture_file,
            category=category,
            available_colors=",".join(selected_colors),
            available_sizes=",".join(selected_sizes),
            user_id=current_user.id
        )

        db.session.add(shop)
        db.session.commit()
        flash(f"Shop '{form.title.data}' created successfully!", "success")
        return redirect(url_for("app.dashbored"))

    return render_template("new_shop.html", form=form, color=color_options, size=size_options)


@bp.route("/dashbored/new_news", methods=["POST", "GET"])
@login_required
def new_news():
    form = NewNews()
    if form.validate_on_submit():
        # حفظ الصورة
        if form.thumbnail.data:
            picture_file = save_picture(form.thumbnail.data, "static/thumbnail")
        else:
            picture_file = "offer1.jpg"

        # التأكد إذا الصورة موجودة من قبل في News
        ex_news = News.query.filter_by(thumbnail=picture_file).first()
        if ex_news:
            flash("This thumbnail already exists. Please choose another one.", "danger")
            return redirect(url_for("app.new_news"))

        # إنشاء الخبر الجديد
        news = News(
            thumbnail=picture_file,
            user_id=current_user.id
        )
        db.session.add(news)
        db.session.commit()

        flash(f"news créé avec succès pour {picture_file}", "success")
        return redirect(url_for("app.dashbored"))

    return render_template("new_news.html", title="new_news", form=form, active_tab="new_news")

@bp.route("/info/<int:shop_id>", methods=["GET", "POST"])
@login_required
def info(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    form = PurchaseForm()

    # نجهزو الألوان والأحجام للواجهة
    colors = shop.available_colors.split(",") if shop.available_colors else []
    sizes = shop.available_sizes.split(",") if shop.available_sizes else []

    if form.validate_on_submit():
        order = Order(
            shop_id=shop.id,
            username=form.username.data,
            phone=form.number.data,
            country=form.country.data,
            size=form.size.data,
            color=form.color.data,
            user_id=current_user.id
        )
        db.session.add(order)
        db.session.commit()
        flash("✅ الطلب تم بنجاح", "success")
        return redirect(url_for("app.shop", shop_id=shop.id))

    return render_template("info.html", form=form, shop=shop, colors=colors, sizes=sizes)

@bp.route("/order")
@login_required
def order():
    form = DeleteForm()
    orders = Order.query.filter_by(user_id=current_user.id).all()
    order = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("order.html",title="order",orders=orders, order=order,form=form)


@bp.route("/dashbored/your_shops", methods=["GET", "POST"])
@login_required
def your_shops():
    page = request.args.get("page", 1, type=int)
    shops = Shop.query.filter_by(user_id=current_user.id).order_by(Shop.id.desc()).paginate(page=page, per_page=3)
    form = DeleteForm()
    return render_template("your_shops.html", your_shops=shops, form=form)


@bp.route("/<int:shop_id>/update", methods=["GET", "POST"])
@login_required
def update(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    form = UpdateForm()

    if form.validate_on_submit():
        shop.title = form.title.data
        shop.content = form.content.data
        shop.prix=form.prix.data

        if form.thumbnail.data:
            delete_picture(shop.thumbnail, 'static/thumbnail')
            new_pic = save_picture(form.thumbnail.data, 'static/thumbnail')
            shop.thumbnail = new_pic

        db.session.commit()
        flash('Update success', 'success')
        return redirect(url_for('app.your_shops'))

    elif request.method == "GET":
        form.title.data = shop.title
        form.content.data = shop.content
        form.prix.data=shop.prix

    return render_template("update.html", title="Update", form=form, shop=shop)


@bp.route("/<int:shop_id>/delete", methods=["POST"])
@login_required
def delete(shop_id):
    shop = Shop.query.get_or_404(shop_id)

    # تحقق من الملكية
    if shop.user_id != current_user.id:
        flash("❌ لا يمكنك حذف متجر لا تملكه.", "danger")
        return redirect(url_for("app.your_shops"))

    db.session.delete(shop)
    db.session.commit()
    flash("✅ تم حذف المتجر بنجاح!", "success")
    return redirect(url_for("app.your_shops"))

@bp.route('/dashbored/your_news',methods=["POST","GET"])
@login_required
def your_news():
    your_news = News.query.filter_by(user_id=current_user.id).all()
    form = DeleteForm()
    return render_template('your_news.html', your_news=your_news, form=form, active_tab="your_news")

@bp.route('/news/<int:news_id>/delete', methods=['POST'])
@login_required
def delete_news(news_id):
    form = DeleteForm()
    if not form.validate_on_submit():
        flash('طلب غير صالح أو CSRF غير صحيح', 'danger')
        return redirect(url_for('app.your_news'))

    # جلب الخبر من DB
    news = News.query.get_or_404(news_id)

    # تحقق من أن المستخدم صاحب الخبر
    if news.user_id != current_user.id:
        flash('ليس لديك صلاحية حذف هذا الخبر', 'danger')
        return redirect(url_for('app.your_news'))

    db.session.delete(news)
    db.session.commit()
    flash('تم الحذف', 'success')
    return redirect(url_for('app.your_news'))


@bp.route('/order/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    form = DeleteForm()
    if not form.validate_on_submit():
        flash('طلب غير صالح أو CSRF غير صحيح', 'danger')
        return redirect(url_for('app.order'))

    # جلب الخبر من DB
    order = Order.query.get_or_404(order_id)

    # تحقق من أن المستخدم صاحب الخبر
    if order.user_id != current_user.id:
        flash('ليس لديك صلاحية حذف هذا الطلب', 'danger')
        return redirect(url_for('app.order'))

    db.session.delete(order)
    db.session.commit()
    flash('تم الحذف', 'success')
    return redirect(url_for('app.order'))
