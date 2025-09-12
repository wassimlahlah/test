from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,SelectField,PasswordField,RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
    Optional,
    
    
)
from .models import User
from flask_login import current_user
class RegistrationForm(FlaskForm):
    fname= StringField(
        "First Name", validators=[DataRequired(),Length(min=2,max=25)]
    )
    lname= StringField(
        "Last Name",validators=[DataRequired(),Length(min=2,max=25)]
    )
    username= StringField(
        "Username",validators=[DataRequired(),Length(min=2,max=25)]
    )
    email= StringField(
        "Email",validators=[DataRequired(),Email()]
    )
    password= PasswordField(
        "Password",validators=[DataRequired(),
              Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
               message='كلمة السر يجب أن تحتوي حرف كبير، حرف صغير، رقم، وطول 8+')
    ])
        
    confirm_password=PasswordField(
        "Confirm Password",validators=[DataRequired(),EqualTo("password")]
    )
    number = StringField("Phone (optional)", validators=[Optional(), Length(min=5, max=20)])

    submit=SubmitField("sign up")

    def validate_username(self, username):
       
       if User.query.filter_by(username=username.data).first():
        raise ValidationError("Username already exists. Please choose a different one.")

    def validate_email(self, email):
      
       if User.query.filter_by(email=email.data).first():
        raise ValidationError("Email already registered. Please log in.")



class LoginForm(FlaskForm):
    email= StringField(
        "Email",validators=[DataRequired(),Email()]
    )
    password= PasswordField(
        "Password",validators=[DataRequired()])        
    
    remember= BooleanField('Remember me')

    submit=SubmitField("log in")

class ProfileForm(FlaskForm):

    
    username= StringField(
        "Username",validators=[DataRequired(),Length(min=2,max=25)]
    )
    email= StringField(
        "Email",validators=[DataRequired(),Email()]
    ) 
    number = StringField("Phone ", validators=[Optional(), Length(min=5, max=20)])
    image = FileField("Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists! Please chosse a different one"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please chosse a different one"
                )

class NewShop(FlaskForm):
   
   title=StringField("title",validators=[DataRequired(),Length(min=2,max=23)])
   content=StringField("content",validators=[DataRequired(),Length(min=2,max=53)])
   prix = StringField("prize ", validators=[Optional(), Length(min=5, max=20)])
   thumbnail=FileField("thumbnail",validators=[FileAllowed(["jpg", "jpeg", "png","avif","webp"], "Images only!")])
   category = SelectField('Category', choices=[
        ('clothing', 'Clothing'),
        ('shoes', 'Shoes')
    ], validators=[DataRequired()])
   submit=SubmitField('create')

class NewNews(FlaskForm):
   
   thumbnail=FileField("thumbnail",validators=[FileAllowed(["jpg", "jpeg", "png","avif","webp"], "Images only!")])
   submit=SubmitField('create')
class PurchaseForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    number = StringField("Phone", validators=[Optional(), Length(min=5, max=20)])

    country = SelectField(
        "Country",
        choices=[("Alger", "Alger"), ("Oran", "Oran"), ("Bejaia", "Bejaia"), ("Annaba", "Annaba")]
    )


    # Size و Color كـ StringField باش يقراو من hidden inputs
    size = StringField("Size", validators=[DataRequired()])
    color = StringField("Color", validators=[DataRequired()])

    submit = SubmitField("Send")

class UpdateForm(NewShop):
   thumbnail=FileField("thumbnail",validators=[FileAllowed(["jpg", "jpeg", "png","avif","webp"], "Images only!")])
   submit=SubmitField('update')

class deleteform(FlaskForm):
   submit=SubmitField('Delete')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
    