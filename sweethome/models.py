import enum
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKeyConstraint

from sweethome import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60))
    user_type = db.Column(db.Integer, nullable=False, default=1)  # 1 for User  2 for Vendor
    phone_number = db.Column(db.String(11))
    name = db.Column(db.String(40), nullable=False)
    homes = db.relationship('Home', backref='owner', lazy=True)
    vendors = db.relationship('VendorServices', backref='vendor', lazy=True)
    #services = db.relationship('ServicesPurchased', backref='service', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(140), nullable=False)
    address2 = db.Column(db.String(140))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    zipcode = db.Column(db.String(6))
    year_built = db.Column(db.Integer)
    zillow_url = db.Column(db.String(2048))
    home_owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    services = db.relationship('ServicesPurchased', backref='services', lazy=True)
    documents = db.relationship('Documents', backref='documents', lazy=True)

    def __repr__(self):
        return f"Home('{self.address1}', '{self.city}', '{self.state}', '{self.zipcode}')"


class ServiceTypes(enum.Enum):
    Insurance = 1
    Warranty = 2
    Gardener = 3
    Plumber = 4
    Handyman = 5
    Contractor = 6

    @property
    def __repr__(self):
        return ServiceTypes.list();


class VendorServices(db.Model):
    __tablename__ = 'VendorServices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(140))
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    servicespurchased = db.relationship('ServicesPurchased', backref='servicespurchased', lazy=True)


    def __repr__(self):
        return f"VendorServices('{self.name}', '{self.description}', '{self.vendor_id}')"


class ServicesPurchased(db.Model):
    __tablename__ = 'ServicesPurchased'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    purchase_price = db.Column(db.Float, default=0.0)
    warranty_enddate = db.Column(db.DateTime, default=datetime.utcnow)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('VendorServices.id'), nullable=False)
    #item_type = db.Column(db.Integer)  # 1 for physical Item 2 for Service

    def __repr__(self):
        return f"ServicesPurchased('{self.name}', '{self.purchase_date}', '{self.vendor_id}'')"

class Documents(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(140), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)

