import datetime

from config import default_carbs_ratio

from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, SelectField, SubmitField,
                     TimeField)
from wtforms.validators import InputRequired


class InputForm(FlaskForm):
    date = DateField(label="Date", default=datetime.date.today)
    time = TimeField(label="Time", default=datetime.datetime.now)
    carbs = IntegerField(
        label="Carbs (g)",
        validators=[InputRequired(message="This value cannot be zero")],
        default=0,
    )
    bg = IntegerField(
        label="BG (mg/dL)",
        validators=[InputRequired(message="This value cannot be zero")],
        default=70,
    )
    special = SelectField(
        label="Special collection event", choices=["", "midnight", "bedtime"]
    )
    carbs_ratio = IntegerField(
        label="Carbs Ratio to Units",
        validators=[InputRequired(message="This value cannot be zero")],
        default=default_carbs_ratio
    )
    submit = SubmitField("Submit")
