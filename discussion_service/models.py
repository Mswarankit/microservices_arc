from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    view_count = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='discussion', lazy='dynamic')
    likes = db.relationship('Like', backref='discussion', lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    likes = db.relationship('Like', backref='comment', lazy='dynamic')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
