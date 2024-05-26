# app/__init__.py
from flask import Flask
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from .tools import limiter


def create_app():
    app = Flask(__name__)

    # set the maximum file size
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1000 * 1000

    # limiter setting
    # get the client's IP address from the X-Forwarded-For header
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
    limiter.init_app(app)

    # Register Blueprints or other application components
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Bind environment variables
    app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

    app.config["DOMAIN"] = "imagetowebsite.dev"
    # Specify the directory to save uploaded images
    UPLOAD_FOLDER = "app/static/uploads"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    TMP_FOLDER = "app/static/tmp"
    if not os.path.exists(TMP_FOLDER):
        os.makedirs(TMP_FOLDER)
    app.config["TMP_FOLDER"] = TMP_FOLDER

    return app
