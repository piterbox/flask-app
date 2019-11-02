class Configuration(object):
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root@localhost/test1'
    SECRET_KEY='secret'
    ## flask security ##
    SECURITY_PASSWORD_SALT='salt'
    SECURITY_PASSWORD_HASH='bcrypt'