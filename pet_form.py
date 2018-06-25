from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, IntegerField, validators, RadioField, TextAreaField


class PetForm(FlaskForm):
    name = StringField(
        'name', [validators.Length(min=1),
                 validators.DataRequired()])
    species = RadioField(
        'species',
        choices=[('cat', 'CAT'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])

    photo_url = StringField(
        'photo_url',
        [validators.URL(require_tld=False),
         validators.optional()])

    age = IntegerField(
        'age', [validators.NumberRange(min=0, max=30),
                validators.optional()])
    notes = TextAreaField(
        'Notes', [validators.Optional(strip_whitespace=True)])
    available = BooleanField('Available', default=True)


class PetEditForm(FlaskForm):
    # name = StringField(
    #     'name', [validators.Length(min=1),
    #              validators.DataRequired()])
    # species = StringField(
    #     'species',
    #     [validators.Length(min=6, max=35),
    #      validators.DataRequired()])
    photo_url = StringField('photo_url', [validators.optional()])
    age = IntegerField(
        'age',
        [validators.NumberRange(min=1, max=100),
         validators.DataRequired()])
    available = BooleanField('Available')