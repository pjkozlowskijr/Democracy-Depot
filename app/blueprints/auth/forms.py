from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ...models import User

# cats = Category.query.all()
# cat_choices = []
# for cat in cats:
#     id = cat.id
#     name = cat.name
#     cat_choices.append((id, name))

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format.")])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Register")

    def validate_email(form, field):
        email_already_used = User.query.filter_by(email=field.data).first()
        if email_already_used:
            raise ValidationError("Email is already in use.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    desc = StringField("Description", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    img = StringField("Image URL", validators=[DataRequired()])
    category_id = RadioField("Category:", validators=[DataRequired()], choices=[(2, "Goods"), (3, "Services")])
    submit = SubmitField("Add Product")

class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField("Add Category")

class EditProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format.")])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Update")

    def validate_email(form, field):
        email_already_used = User.query.filter_by(email=field.data).first()
        if email_already_used:
            raise ValidationError("Email is already in use.")

class RemCategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField("Remove Category")

class RemProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    submit = SubmitField("Remove Product")