import json
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
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404

@app.route("/pokemon", methods=['GET'])
def getPokemon():
    try:
        result = app.db.query(Pokemon).all() # pylint: disable=E1101
        return Response(json.dumps(result, cls=AlchemyEncoder), mimetype='application/json')
    except Exception as exception:
        abort(404, description=exception)

@app.route("/pokemon/<int:pokemon_id>", methods=['GET'])
def getPokemonById(pokemon_id):
    try:
        result = app.db.query(Pokemon).filter(Pokemon.id == pokemon_id).first() # pylint: disable=E1101
        return Response(json.dumps(result, cls=AlchemyEncoder), mimetype='application/json')
    except Exception as exception:
        abort(404, description=exception)

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    """Closes the database session."""
    app.db.remove()

if __name__ == "__main__":
    app.run(debug=True)
