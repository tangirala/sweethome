from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired


class HomeForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    address2 = StringField('Address2', validators=[])
    city = StringField('City', validators=[])
    state = StringField('State', validators=[])
    zipcode = StringField('Zipcode', validators=[])
    year_built = IntegerField('Year Buit',validators=[])
    zillow_url = StringField('Zillow URL', validators=[])
    date_posted = DateField('Creation Date', validators=None)
    submit = SubmitField('Create Home')

class DocumnentUploadForm(FlaskForm):
    file = FileField('file', validators=[DataRequired()])
    filename = StringField('filename', validators=[DataRequired()])
    submit = SubmitField('Upload')
