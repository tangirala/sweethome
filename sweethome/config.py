class Config:
    SECRET_KEY = '1234567890'
#    SQLALCHEMY_DATABASE_URI  = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:car4sale@localhost/sweethome'
    MAIL_SERVER = 'mail.brightstonemarketing.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'smtp@brightstonemarketing.com'
    MAIL_PASSWORD = 'car4sale'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
