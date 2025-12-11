from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

# Correct config key
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


# Create tables
with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def home():
    return "Deployment Success"
           
# Create user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'user created'}), 201
    except Exception as e:
        return jsonify({'message': 'error in user creation', 'error': str(e)}), 500


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.json() for user in users]), 200
    except Exception as e:
        return jsonify({'message': 'error getting users', 'error': str(e)}), 500


# Get user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if user:
            return jsonify({'user': user.json()}), 200
        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error getting user', 'error': str(e)}), 500


# Update user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        user = User.query.get(id)

        if user:
            user.username = data['username']
            user.email = data['email']
            db.session.commit()

            return jsonify({'message': 'user updated'}), 200

        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error updating user', 'error': str(e)}), 500


# Delete user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'user deleted'}), 200

        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error deleting user', 'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 4000)))
