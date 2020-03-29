import dotenv

def getkey(key):
    return dotenv.get_key(".env", key)

"""Flask config class."""
class Config:
    """Set Flask configuration vars."""

    # General Config
    SECRET_KEY = getkey('SECRET_KEY')
    SERVER_NAME = getkey('SERVER_NAME')
    FLASK_ENV = getkey('FLASK_ENV')
    if FLASK_ENV == 'development':
        WERKZEUG_DEBUG_PIN = 'off'


class ProdConfig(Config):
    #DATABASE_URI = getkey('PROD_DATABASE_URI')
    pass


class DevConfig(Config):
    #DATABASE_URI = getkey('DEV_DATABASE_URI')
    pass
