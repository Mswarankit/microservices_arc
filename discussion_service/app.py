from flask import Flask
from .models import db
from .router import discussion_bp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["POSTGRES_DISCUSSION_CREDS"]
app.config['SQLALCHEMY_COMMENT_DATABASE_URI'] = os.environ["POSTGRES_COMMENT_CREDS"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(discussion_bp)

if __name__ == '__main__':
    app.run(debug=True)
