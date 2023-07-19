# app/main.py

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

flask_app = Flask(__name__)
cors = CORS(flask_app)
bcrypt = Bcrypt(flask_app)
jwt = JWTManager(flask_app)


def create_app():
    # Load configuration from .env file
    load_dotenv()
    flask_app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # flask_app.config.from_envvar('.env')

    # Register API routes
    from app.api.movies import movies
    from app.api.users import users
    flask_app.register_blueprint(movies)
    flask_app.register_blueprint(users)

    return flask_app
