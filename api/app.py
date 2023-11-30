import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

load_dotenv()
app = Flask(__name__)

# Configuraciones
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
# MongoDB Configuration for local development
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/db?authSource=admin'

# JWT Manager
jwt = JWTManager(app)

# CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Rutas
from main import routes
app.register_blueprint(routes.main)

if __name__ == '__main__':
    PORT = os.getenv('PORT')
    DEBUG = os.getenv('DEBUG')
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
