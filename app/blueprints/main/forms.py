from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField

class FilterSortForm(FlaskForm):
    category = RadioField("Filter by:", choices=[("accessories", "Accessories"), ("clubs", "Clubs")])
    sort = RadioField("Sort by:", choices=[("asc_name", "Alpha A-Z"), ("desc_name", "Alpha Z-A"), ("asc_price", "Price $-$$$$"), ("desc_price", "Price $$$$-$")])
    submit = SubmitField("Apply")