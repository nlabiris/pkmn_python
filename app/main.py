import json
import sys
import traceback
from app.exceptions.httpexception import HttpException
from app.data_access.core.db import Database
from app.data_access.models.models import Candidate, Nature, Pokemon, new_alchemy_encoder, CandidateNature
from flask import Flask, Response, abort, jsonify, request

database = Database()
database.create_engine("mysql://root:XX@localhost/pkmn_breed")
database.bind_engine()
database.create_session()
app = Flask(__name__)
app.db = database.session

@app.errorhandler(HttpException)
def custom_http_exception(exception):
    return jsonify({
        "error": exception.errorcode,
        "description": str(exception)
    }), exception.errorcode

@app.errorhandler(Exception)
def internal_server_error(exception):
    return jsonify({
        "error": 500,
        "description": str(exception)
    }), 500

@app.route("/pokemon", methods=['GET'])
def getPokemon():
    result = app.db.query(Candidate).all() # pylint: disable=E1101
    return Response(json.dumps(result), mimetype='application/json')

@app.route("/pokemon", methods=['POST'])
def addPokemon():
    body = request.json
    if not body:
        raise HttpException(400, "Empty body provided")

    if "pokemon_id" not in body:
        raise HttpException(400, "No Pokemon ID provided")

    if "ability_ids" not in body or not body["ability_ids"]:
        raise HttpException(400, "No Ability IDs provided")

    if "nature_ids" not in body or not body["nature_ids"]:
        raise HttpException(400, "No Nature IDs provided")

    if "item_ids" in body:
        if not body["item_ids"]:
            raise HttpException(400, "No Item IDs provided")

    if "move_ids" in body:
        if not body["move_ids"]:
            raise HttpException(400, "No Move IDs provided")

    candidate = Candidate()
    pokemon = app.db.query(Pokemon).filter(Pokemon.id == request.json["pokemon_id"]).first() # pylint: disable=E1101
    if not pokemon:
        raise HttpException(404, "No Pokemon found with the given ID")
    candidate.pokemon = pokemon
    for nature_id in request.json["nature_ids"]:
        nature = app.db.query(Nature).filter(Nature.id == nature_id).first() # pylint: disable=E1101
        if not nature:
            raise HttpException(404, "No Nature found with the given ID")
        candidate.natures.append(nature)
    app.db.add(candidate) # pylint: disable=E1101
    app.db.commit() # pylint: disable=E1101

    return Response(json.dumps(candidate, cls=new_alchemy_encoder(), check_circular=False), mimetype='application/json')

@app.route("/pokemon/<int:pokemon_id>", methods=['PUT'])
def updatePokemon(pokemon_id):
    body = request.json
    if not body:
        raise HttpException(400, "Empty body provided")

    if "pokemon_id" not in body:
        raise HttpException(400, "No Pokemon ID provided")

    if "ability_ids" not in body or not body["ability_ids"]:
        raise HttpException(400, "No Ability IDs provided")

    if "nature_ids" not in body or not body["nature_ids"]:
        raise HttpException(400, "No Nature IDs provided")

    if "item_ids" in body:
        if not body["item_ids"]:
            raise HttpException(400, "No Item IDs provided")

    if "move_ids" in body:
        if not body["move_ids"]:
            raise HttpException(400, "No Move IDs provided")

    candidate = app.db.query(Candidate).filter(Candidate.id == pokemon_id).first() # pylint: disable=E1101

    pokemon = app.db.query(Pokemon).filter(Pokemon.id == request.json["pokemon_id"]).first() # pylint: disable=E1101
    if not pokemon:
        raise HttpException(404, "No Pokemon found with the given ID")
    candidate.pokemon = pokemon
    for nature_id in request.json["nature_ids"]:
        nature = app.db.query(Nature).filter(Nature.id == nature_id).first() # pylint: disable=E1101
        if not nature:
            raise HttpException(404, "No Nature found with the given ID")
        candidate.natures.append(nature)
    app.db.commit()  # pylint: disable=E1101

    return Response(json.dumps(candidate, cls=new_alchemy_encoder(), check_circular=False), mimetype='application/json')

@app.route("/pokemon/<int:pokemon_id>", methods=['GET'])
def getPokemonById(pokemon_id):
    result = app.db.query(Candidate).filter(Candidate.id == pokemon_id).first() # pylint: disable=E1101
    if result is None:
        raise HttpException(404, "Pokemon not found")
    return Response(json.dumps(result, cls=new_alchemy_encoder(), check_circular=False), mimetype = 'application/json')

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.db.remove()

if __name__ == "__main__":
    app.run(debug=True)
