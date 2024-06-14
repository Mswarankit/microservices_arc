from flask import Flask
from flask_jwt_extended import JWTManager
from .models import db
from .router import user_bp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["POSTGRES_CREDS"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
