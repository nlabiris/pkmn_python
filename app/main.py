import json
from app.exceptions.httpexception import HttpException
from app.data_access.core.db import Database
from app.data_access.models.models import Pokemon, AlchemyEncoder
from flask import Flask, Response, abort, jsonify, request

database = Database()
database.create_engine("sqlite:///pkmn_breed.db")
database.bind_engine()
database.create_session()

app = Flask(__name__)
app.db = database.session

@app.errorhandler(404)
def resource_not_found(exception):
    return jsonify({
        "error": 404,
        "description": str(exception)
    }), 404

@app.errorhandler(500)
def internal_server_error(exception):
    return jsonify({
        "error": 500,
        "description": str(exception)
    }), 500

@app.route("/pokemon", methods=['GET'])
def getPokemon():
    try:
        result = app.db.query(Pokemon).all() # pylint: disable=E1101
        return Response(json.dumps(result, cls=AlchemyEncoder), mimetype='application/json')
    except Exception as e:
        abort(500, description=e)

@app.route("/pokemon/<int:pokemon_id>", methods=['GET'])
def getPokemonById(pokemon_id):
    try:
        result = app.db.query(Pokemon).filter(Pokemon.id == pokemon_id).first() # pylint: disable=E1101
        if result is None:
            raise HttpException(404, "Pokemon not found")
        return Response(json.dumps(result, cls=AlchemyEncoder), mimetype='application/json')
    except HttpException as e:
        abort(404, description=e)
    except Exception as e:
        abort(500, description=e)

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    """Closes the database session."""
    app.db.remove()

if __name__ == "__main__":
    app.run(debug=True)
