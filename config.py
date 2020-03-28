"""Flask config class."""
import dotenv

def getkey(key):
    return dotenv.get_key(".env", key)

class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = getkey('TESTING')
    DEBUG = getkey('DEBUG')
    SECRET_KEY = getkey('SECRET_KEY')
    SERVER_NAME = getkey('SERVER_NAME')


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    #DATABASE_URI = getkey('PROD_DATABASE_URI')


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    #DATABASE_URI = getkey('DEV_DATABASE_URI')
