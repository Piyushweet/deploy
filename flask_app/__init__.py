from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config:
        app.config.update(test_config)

    # register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
