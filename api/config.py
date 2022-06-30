import os
from urllib.parse import quote_plus as urlquote

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
        f"postgresql://postgres:{urlquote('P@ssw0rd')}@localhost:5432/postgres"
    )
    SQLALCHEMY_DATABASE_URI = url
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ).replace('postgres', 'postgresql')
    DEBUG = False


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig}
