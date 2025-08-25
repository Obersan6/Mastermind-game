# project-root/config.py 
# loads env & applies Flask/DB config

import os
from dotenv import load_dotenv

def apply_config(app):
    load_dotenv()  # load .env into os.environ

    app_env = os.environ.get("APP_ENV", "dev")

    # SECRET_KEY: allow default in dev, require in prod
    secret = os.environ.get("SECRET_KEY")
    if app_env == "prod" and not secret:
        raise RuntimeError("SECRET_KEY is required in production")
    app.config["SECRET_KEY"] = secret or "change-me"

    # Database URL: allow default in dev, require in prod
    db_url = os.environ.get("DATABASE_URL")
    if app_env == "prod" and not db_url:
        raise RuntimeError("DATABASE_URL is required in production")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "postgresql+psycopg://postgres:postgres@localhost:5433/mastermind_db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


