import os

_current_dir = os.path.dirname(os.path.abspath(__file__))


# more configuration options here http://flask.pocoo.org/docs/1.0/config/
class Config:
    """
    Base Configuration
    """

    SECRET_KEY = "testkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"  # where logs are outputted to
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'test')
    JWT_ALGORITHM = "HS256"
    SESSION_TYPE = 'filesystem'


class DevelopmentConfig(Config):
    url = (
        "postgres://eyrsyqluzmciea:366bef3f59412fd0f68567bb94a80db812c6e60098e2d1be9061ef42af128904@ec2-63-34-180-86."
        "eu-west-1.compute.amazonaws.com:5432/da2dp7hqo03dto"
    )
    SQLALCHEMY_DATABASE_URI = url
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )  # you may do the same as the development config but this currently gets the database URL from an env variable
    DEBUG = False


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig}
