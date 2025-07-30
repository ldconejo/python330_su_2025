import os

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
with app.app_context():
    db.create_all()

class HomeResource(Resource):
    def get(self):
        return {'message': 'Welcome to the Flask CRUD API!'}
    
class UserResource(Resource):
    def get(self, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return {'message': 'Invalid user ID'}, 400
        user = db.session.get(User, user_id)
        if user:
            return user.to_dict(), 200
        return {'message': 'User not found'}, 404
    
    def post(self, user_id):
        data = request.get_json()
        if not data.get("name") or not data.get("email"):
            return {'message': 'Name and email are required'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
        
        user = User(id=user_id, name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201  
    
    def patch(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404
        data = request.get_json()
        user.name = data.get('name', user.name )
        user.email = data.get('email', user.email)

        db.session.commit()
        return user.to_dict(), 200
    
    def delete(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    
class SayHello(Resource):
    def get(self, name):
        return {'message': f'Hello, {name}!'}
    
api.add_resource(HomeResource, '/')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(SayHello, '/users/<name>')
    
if __name__ == '__main__':
    app.run(debug=True)
