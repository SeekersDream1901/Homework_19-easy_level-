from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import GenreSchema, Genre

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre)
        return genres_schema.dump(all_genres), 200

    def post(self):
        request_json = request.json
        new_genre = Genre(**request_json)

        with db.session.begin():
            db.session.add(new_genre)

        return "New genre successfully added.", 201


@genres_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id):
        genre = Genre.query.get(id)
        return genre_schema.dump(genre), 200

    def put(self, id):
        updated_genre = db.session.query(Genre).filter(Genre.id == id).update(request.json)
        db.session.commit()

        if not updated_genre:
            return "Error. Genre not updated.", 400

        return "Genre updated successfully", 204

    def delete(self, id):
        deleted_genre = db.session.query(Genre).get(id)

        if not deleted_genre:
            return "Error. Genre not deleted.", 400

        db.session.delete(deleted_genre)
        db.session.commit()

        return "Genre deleted successfully", 204
