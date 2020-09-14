from operator import attrgetter

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.fields.html5 import DateField
#from flask_login import current_user
#from sweethome.models import VendorServices



class ServicesPurchasedForm(FlaskForm):

    name = StringField('Name')
    purchase_date = DateField('Purchased On')
    purchase_price = DecimalField('Purchase Price')
    warranty_enddate = DateField('Warranty End Date')
    home_id = SelectField('For which Home', coerce=int)
    service_id = SelectField('Service Purchased', coerce=int)
    submit = SubmitField('Add Service Purchased')
