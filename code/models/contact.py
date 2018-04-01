from db import db

class ContactModel(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80))
    full_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('UserModel')
    
    def __init__(self, user_id, nickname, full_name, phone_number):
        self.user_id = user_id
        self.nickname = nickname
        self.full_name = full_name
        self.phone_number = phone_number

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'full_name': self.full_name,
            'phone_number': self.phone_number
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()