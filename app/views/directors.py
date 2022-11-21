from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import DirectorSchema, Director

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director)
        print(all_directors)
        return directors_schema.dump(all_directors), 200

    def post(self):
        request_json = request.json
        new_director = Director(**request_json)

        with db.session.begin():
            db.session.add(new_director)

        return "New director successfully added.", 201


@directors_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        director = Director.query.get(id)
        return director_schema.dump(director), 200

    def put(self, id):
        updated_director = db.session.query(Director).filter(Director.id == id).update(request.json)
        db.session.commit()

        if not updated_director:
            return "Error. Director not updated.", 400

        return "Director updated successfully.", 204

    def delete(self, id):
        deleted_director = db.session.query(Director).get(id)

        if not deleted_director:
            return "Error. The director's data has not been deleted", 400

        db.session.delete(deleted_director)
        db.session.commit()

        return "The director's data has been successfully deleted.", 204
