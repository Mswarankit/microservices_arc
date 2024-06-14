from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Discussion, Comment, Like

discussion_bp = Blueprint('discussion_bp', __name__)

@discussion_bp.route('/discussions', methods=['POST'])
@jwt_required()
def create_discussion():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_discussion = Discussion(title=data['title'], text=data['text'], image_url=data.get('image_url'), tags=data.get('tags'), user_id=current_user_id)
    db.session.add(new_discussion)
    db.session.commit()
    return jsonify({'message': 'Discussion created successfully', 'discussion_id': new_discussion.id}), 201

@discussion_bp.route('/discussions/<int:id>', methods=['PUT'])
@jwt_required()
def update_discussion(id):
    data = request.get_json()
    discussion = Discussion.query.get(id)
    if discussion:
        discussion.title = data['title']
        discussion.text = data['text']
        discussion.image_url = data.get('image_url')
        discussion.tags = data.get('tags')
        db.session.commit()
        return jsonify({'message': 'Discussion updated successfully'}), 200
    return jsonify({'message': 'Discussion not found'}), 404

@discussion_bp.route('/discussions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_discussion(id):
    discussion = Discussion.query.get(id)
    if discussion:
        db.session.delete(discussion)
        db.session.commit()
        return jsonify({'message': 'Discussion deleted successfully'}), 200
    return jsonify({'message': 'Discussion not found'}), 404

@discussion_bp.route('/discussions/<int:id>', methods=['GET'])
def get_discussion(id):
    discussion = Discussion.query.get(id)
    if discussion:
        discussion.view_count += 1
        db.session.commit()
        return jsonify({'id': discussion.id, 'title': discussion.title, 'text': discussion.text, 'image_url': discussion.image_url, 'tags': discussion.tags, 'user_id': discussion.user_id, 'created_on': discussion.created_on, 'view_count': discussion.view_count}), 200
    return jsonify({'message': 'Discussion not found'}), 404

@discussion_bp.route('/discussions', methods=['GET'])
def list_discussions():
    discussions = Discussion.query.all()
    return jsonify([{'id': discussion.id, 'title': discussion.title, 'text': discussion.text, 'image_url': discussion.image_url, 'tags': discussion.tags, 'user_id': discussion.user_id, 'created_on': discussion.created_on, 'view_count': discussion.view_count} for discussion in discussions]), 200

@discussion_bp.route('/discussions/search', methods=['GET'])
def search_discussions():
    text = request.args.get('text')
    discussions = Discussion.query.filter(Discussion.text.ilike(f'%{text}%')).all()
    return jsonify([{'id': discussion.id, 'title': discussion.title, 'text': discussion.text, 'image_url': discussion.image_url, 'tags': discussion.tags, 'user_id': discussion.user_id, 'created_on': discussion.created_on, 'view_count': discussion.view_count} for discussion in discussions]), 200

@discussion_bp.route('/discussions/tags', methods=['GET'])
def list_discussions_by_tags():
    tags = request.args.get('tags')
    discussions = Discussion.query.filter(Discussion.tags.ilike(f'%{tags}%')).all()
    return jsonify([{'id': discussion.id, 'title': discussion.title, 'text': discussion.text, 'image_url': discussion.image_url, 'tags': discussion.tags, 'user_id': discussion.user_id, 'created_on': discussion.created_on, 'view_count': discussion.view_count} for discussion in discussions]), 200

@discussion_bp.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_comment = Comment(text=data['text'], user_id=current_user_id, discussion_id=data['discussion_id'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully', 'comment_id': new_comment.id}), 201

@discussion_bp.route('/comments/<int:id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if comment:
        comment.text = data['text']
        db.session.commit()
        return jsonify({'message': 'Comment updated successfully'}), 200
    return jsonify({'message': 'Comment not found'}), 404

@discussion_bp.route('/comments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    comment = Comment.query.get(id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    return jsonify({'message': 'Comment not found'}), 404

@discussion_bp.route('/comments/<int:id>/like', methods=['POST'])
@jwt_required()
def like_comment(id):
    current_user_id = get_jwt_identity()
    like = Like(user_id=current_user_id, comment_id=id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Comment liked successfully'}), 201

@discussion_bp.route('/discussions/<int:id>/comments', methods=['GET'])
def get_comments_for_discussion(id):
    comments = Comment.query.filter_by(discussion_id=id).all()
    return jsonify([{'id': comment.id, 'text': comment.text, 'user_id': comment.user_id, 'created_on': comment.created_on} for comment in comments]), 200
