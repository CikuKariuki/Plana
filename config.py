import os

class Config:
    '''
    general configuration parent class
    '''
    QUOTES_API_BASE_URL='http://quotes.stormconsultancy.co.uk/random.json' 
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wanjiku:mySql003@localhost/blogger'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI =os.environ.get("DATABASE_URL")

# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wanjiku:mySql003@localhost/blog_test'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wanjiku:mySql003@localhost/blogger'
    DEBUG = True

config_options = {
    'development':DevConfig,
    'production':ProdConfig
    # 'test': TestConfig
}