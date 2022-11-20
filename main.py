from flask import Flask
from flask_restx import Api

from easy_level.app.config import Config
from easy_level.app.database import db
from easy_level.app.views.directors import directors_ns
from easy_level.app.views.genres import genres_ns
from easy_level.app.views.movies import movies_ns


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    app.run()
