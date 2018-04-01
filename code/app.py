from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister, UsernameExists
from resources.contact import Contact, ContactList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test' # omit this line if publishing this source code to a 
						# public location, also change this secret key
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/register')
api.add_resource(UsernameExists, '/usernameexists/<username>')
api.add_resource(Contact, '/contact', '/contact/<_id>')
api.add_resource(ContactList, '/contact/list')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(debug=True)