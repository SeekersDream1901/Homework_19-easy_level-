from flask import request
from flask_restx import Namespace, Resource

from app.models import UserSchema, User
from app.database import db


users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = db.session.query(User)
        print(all_users)
        return users_schema.dump(all_users)

    def post(self):
        request_json = request.json

        new_user = User(**request_json)

        with db.session.begin():
            db.session.add(new_user)

        return "A new user has been registered", 201


@users_ns.route('/<int:user_id>')
class UsersView(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return user_schema.dump(user), 200

    def put(self, user_id):
        updated_user = db.session.query(User).filter(User.id == user_id).update(request.json)
        db.session.commit()

        if not updated_user:
            return "Mistake. The user's data has not been updated.", 400

        return "The user's data has been updated.", 204

    def delete(self, user_id):
        deleted_user = db.session.query(User).get(user_id)

        if not deleted_user:
            return "Error. The user has not been deleted.", 400

        db.session.delete(deleted_user)
        db.session.commit()

        return "User deleted.", 204
