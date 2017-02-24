from flask.ext.wtf import Form
from wtforms import StringField, validators
from wtforms.validators import DataRequired


class BuildFinderForm(Form):
    packageFileName = StringField('packageFileName', [validators.Length(min=4, max=25)])
