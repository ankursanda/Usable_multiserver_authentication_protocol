from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .register import RegistrationCenter

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['API_KEY'] = os.getenv('API_KEY')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('registration_server.log'), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Flask application")

    db.init_app(app)
    registration_center = RegistrationCenter(app.config['SECRET_KEY'])

    with app.app_context():
        db.create_all()

    from .routes import register_bp
    register_bp.registration_center = registration_center
    app.register_blueprint(register_bp) #

    @app.route('/ping', methods=['GET'])
    def ping():
        return {"message": "Service is running"}, 200

    return app
