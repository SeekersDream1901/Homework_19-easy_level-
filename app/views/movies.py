from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import MovieSchema, Movie


movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        all_movies = db.session.query(Movie)

        director_id = request.args.get("director_id")
        if director_id is not None:
            all_movies = all_movies.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")
        if genre_id is not None:
            all_movies = all_movies.filter(Movie.genre_id == genre_id)

        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

        return "New movie has been added", 201


@movies_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        return movie_schema.dump(movie), 200

    def put(self, id):
        updated_movie = db.session.query(Movie).filter(Movie.id == id).update(request.json)
        db.session.commit()

        if not updated_movie:
            return "Error. Movie data not updated", 400

        return "Movie data updated successfully.", 204

    def delete(self, id):
        deleted_row = db.session.query(Movie).get(id)

        if not deleted_row:
            return "Error. The movie data has not been deleted.", 400

        db.session.delete(deleted_row)
        db.session.commit()

        return "Movie data deleted.", 204
