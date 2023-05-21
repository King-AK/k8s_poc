import os


class BaseConfig():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class PostgresConfig(BaseConfig):
    database = os.environ.get("MAT_DATABASE_NAME", "mat")
    user = os.environ.get("MAT_DATABASE_USER", "mat_admin")
    passwd = os.environ.get("MAT_DATABASE_PASSWD", "passwd")
    host = os.environ.get("MAT_DATABASE_HOST", "localhost")
    port = os.environ.get("MAT_DATABASE_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}"
