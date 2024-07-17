from flask import Flask

from proxy.routes import api


def create_app(settings_override=None):
    app = Flask(__name__)

    app.config.from_object("config.settings")
    app.register_blueprint(api)

    if settings_override:
        app.config.update(settings_override)

    return app

