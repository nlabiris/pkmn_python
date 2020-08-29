import json
import sys
import traceback
from app.exceptions.httpexception import HttpException
from app.data_access.core.db import Database
from app.data_access.models.models import new_alchemy_encoder, CandidateNature, Candidate, Nature, Pokemon, Ability, Item, Move
from flask import Flask, Response, abort, jsonify, request

database = Database()
database.create_engine("mysql://root:compaq@localhost/pkmn_breed")
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
    result = app.db.query(Candidate).all()
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
    
    pokemon = app.db.query(Pokemon).filter(Pokemon.id == request.json["pokemon_id"]).first()
    if not pokemon:
        raise HttpException(404, "No Pokemon found with the given ID")
    candidate.pokemon = pokemon

    for ability_id in request.json["ability_ids"]:
        ability = app.db.query(Ability).filter(Ability.id == ability_id).first() 
        if not ability:
            raise HttpException(404, "No Ability found with the given ID")
        candidate.abilities.append(ability)

    for nature_id in request.json["nature_ids"]:
        nature = app.db.query(Nature).filter(Nature.id == nature_id).first()
        if not nature:
            raise HttpException(404, "No Nature found with the given ID")
        candidate.natures.append(nature)

    for item_id in request.json["item_ids"]:
        item = app.db.query(Item).filter(Item.id == item_id).first() 
        if not item:
            raise HttpException(404, "No Item found with the given ID")
        candidate.items.append(item)

    for move_id in request.json["move_ids"]:
        move = app.db.query(Move).filter(Move.id == move_id).first() 
        if not move:
            raise HttpException(404, "No Move found with the given ID")
        candidate.moves.append(move)

    app.db.add(candidate)
    app.db.commit()

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

    candidate = app.db.query(Candidate).filter(Candidate.id == pokemon_id).first()

    pokemon = app.db.query(Pokemon).filter(Pokemon.id == request.json["pokemon_id"]).first()
    if not pokemon:
        raise HttpException(404, "No Pokemon found with the given ID")
    candidate.pokemon = pokemon
    for nature_id in request.json["nature_ids"]:
        nature = app.db.query(Nature).filter(Nature.id == nature_id).first()
        if not nature:
            raise HttpException(404, "No Nature found with the given ID")
        candidate.natures.append(nature)
    app.db.commit() 

    return Response(json.dumps(candidate, cls=new_alchemy_encoder(), check_circular=False), mimetype='application/json')

@app.route("/pokemon/<int:pokemon_id>", methods=['GET'])
def getPokemonById(pokemon_id):
    result = app.db.query(Candidate).filter(Candidate.id == pokemon_id).first()
    if result is None:
        raise HttpException(404, "Pokemon not found")
    return Response(json.dumps(result, cls=new_alchemy_encoder(), check_circular=False), mimetype = 'application/json')

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.db.remove()

if __name__ == "__main__":
    app.run(debug=True)
