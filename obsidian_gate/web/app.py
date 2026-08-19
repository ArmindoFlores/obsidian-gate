from pathlib import Path

import redis
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import URL

from obsidian_gate import config
from obsidian_gate.models.db import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        f"{config.DATABASE_ENGINE}+{config.DATABASE_DRIVER}",
        username=config.DATABASE_USERNAME,
        password=config.DATABASE_PASSWORD,
        host=config.DATABASE_HOST,
        database=config.DATABASE_NAME,
    )
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    if config.SESSION_REDIS_URL is not None:
        app.config["SESSION_TYPE"] = "redis"
        app.config["SESSION_REDIS"] = redis.from_url(config.SESSION_REDIS_URL)
    else:
        app.config["SESSION_TYPE"] = "filesystem"
 
    db.init_app(app)
    Migrate(app, db, directory=(Path(__file__) / ".." / ".." / "migrations").resolve())
 
    from obsidian_gate.web.routes import notes_bp
 
    app.register_blueprint(notes_bp)
 
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
 
