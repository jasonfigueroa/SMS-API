from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.contact import ContactModel

class Contact(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('nickname',
        type=str,
        required=True,
        help="A nickname is required to create a contact"
    )

    parser.add_argument('full_name',
        type=str,
        required=True,
        help="A full name is required to create a contact"
    )

    parser.add_argument('phone_number',
        type=str,
        required=True,
        help="A phone number is required to create a contact"
    )

    @jwt_required()
    def get(self, _id):
        contact = ContactModel.find_by_id(_id)
        if contact and current_identity.id != contact.user_id:
            return {"message": "Not authorized to view this content"}, 401
        if contact:
            return contact.json()
        return {"message": "Contact not found"}, 404

    @jwt_required()
    def post(self):
        data = Contact.parser.parse_args()

        nickname = data['nickname']
        full_name = data['full_name']
        phone_number = data['phone_number']

        user_id = current_identity.id        

        contact = ContactModel(
            user_id,
            nickname,
            full_name,
            phone_number
        )

        try:
            contact.save_to_db()
        except:
            return {"message": "An error occurred while storing the match stats"}, 500

        return contact.json(), 201

class ContactList(Resource):
    @jwt_required()
    def get(self):
        contacts = [contact.json() for contact in ContactModel.query.all() if contact.user_id == current_identity.id]

        return {"contacts": contacts}