from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="A username is required to register."
	)

	parser.add_argument('password',
		type=str,
		required=True,
		help="A password is required to register."
	)

	def post(self):
		data = UserRegister.parser.parse_args()
		
		username = data['username']
		password = data['password']

		if UserModel.find_by_username(username):
			return {"message": "User with that username already exists."}, 400
		
		user = UserModel(username, generate_password_hash(password))
		user.save_to_db()
		return {"message": "User created successfully."}, 201

class UsernameExists(Resource):
	def get(self, username):
		if UserModel.find_by_username(username):
			return {"message": "User with that username already exists."}
		return {"message": "That username is currently available."}
