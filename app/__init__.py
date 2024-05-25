# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from poe_api_wrapper import PoeApi


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # set the maximum file size
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1000 * 1000

    # Register Blueprints or other application components
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Initialize PoeApi
    app.config["POE_P_B"] = os.getenv("POE_P_B", "")
    app.config["POE_P_LAT"] = os.getenv("POE_P_LAT", "")
    # for dev
    proxy_context = [
        {"https": "http://127.0.0.1:7890", "http": "http://127.0.0.1:7890"},
    ]
    tokens = {"b": app.config["POE_P_B"], "lat": app.config["POE_P_LAT"]}
    app.poe_client = PoeApi(cookie=tokens, proxy=proxy_context)
    # for production
    # app.poe_client=PoeApi(cookie=tokens)

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
