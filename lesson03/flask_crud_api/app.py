# app.py

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

# Create database tables
with app.app_context():
    db.create_all()

# Create resources
class HomeResource(Resource):
    def get(self):
        return {"message": "Welcome to the Flask CRUD API"}, 200
    
class UserResource(Resource):
    def get(self, user_id):
        user = db.session.get(User, user_id)
        if user:
            return user.to_dict(), 200
        return {"message": "User not found"}, 404

    def post(self, user_id):
        data = request.get_json()
        if not data.get("name") or not data.get("email"):
            return {"message": "Name and email required"}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"message": "Email already exists"}, 400

        user = User(id=user_id, name=data["name"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

    def put(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)

        db.session.commit()
        return user.to_dict(), 200
    
    def delete(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
    
# Register endpoint
api.add_resource(HomeResource, "/")
api.add_resource(UserResource, "/users/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)