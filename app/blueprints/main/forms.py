from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ...models import User

class FilterSortForm(FlaskForm):
    category = RadioField("Filter by:", choices=[("goods", "Goods"), ("services", "Services")])
    sort = RadioField("Sort by:", choices=[("asc_name", "Alpha A-Z"), ("desc_name", "Alpha Z-A"), ("asc_price", "Price $-$$$$"), ("desc_price", "Price $$$$-$")])
    submit = SubmitField("Apply")