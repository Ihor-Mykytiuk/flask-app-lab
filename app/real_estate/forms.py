from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import (
    StringField, TextAreaField, IntegerField, SubmitField,
    SelectField, SelectMultipleField, widgets, FileField
)
from wtforms.validators import DataRequired, Length, NumberRange


# Клас для чекбоксів
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class HousingForm(FlaskForm):
    # Основні поля житла
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=100)])
    area = IntegerField('Area (m²)', validators=[DataRequired(), NumberRange(min=1)])
    rooms = IntegerField('Rooms', validators=[DataRequired(), NumberRange(min=1)])

    type = SelectField('Type', coerce=int, validators=[DataRequired()])
    repair = SelectField('Repair Type', coerce=int, validators=[DataRequired()])

    communications = MultiCheckboxField('Communications', coerce=int)
    comforts = MultiCheckboxField('Comforts', coerce=int)

    images = MultipleFileField('Images')

    submit = SubmitField('Add Housing')

class SearchHousingForm(FlaskForm):
    sort_by = SelectField('Sort by', choices=[('created', 'Sort by created'),
                                              ('price', 'Sort by price'),
                                              ('rooms', 'Sort by rooms'),
                                              ('area', 'Sort by area'),])
    min_price = IntegerField('Min Price')
    max_price = IntegerField('Max Price')
    min_area = IntegerField('Min Area')
    max_area = IntegerField('Max Area')
    rooms = IntegerField('Rooms')
    type = SelectField('Type', coerce=int)
    repair = SelectField('Repair Type', coerce=int)
    communications = MultiCheckboxField('Communications', coerce=int)
    comforts = MultiCheckboxField('Comforts', coerce=int)

    submit = SubmitField('Search')
