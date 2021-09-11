# pylint: disable=no-member
import json
from app.exception.httpexception import HttpException
from app.data_access.model.models import new_alchemy_encoder, CandidateEvSpread, CandidateIvSpread, CandidateNature, CandidateMove, CandidateItem, CandidateAbility, Candidate, Nature, Pokemon, Ability, Item, Move
from flask import Response, request
from app.index import app

@app.route("/candidate", methods=['POST'])
def add_candidate():
    body = request.json
    if not body:
        raise HttpException(400, "Empty body provided")

    if "pokemon_id" not in body:
        raise HttpException(400, "No Pokemon ID provided")
    else:
        pokemon = app.db.query(Pokemon).filter(Pokemon.id == request.json["pokemon_id"]).first()

    if "ability_ids" not in body or not body["ability_ids"]:
        raise HttpException(400, "No Ability IDs provided")
    else:
        abilities = app.db.query(Ability).filter(Ability.id.in_(request.json["ability_ids"])).all()

    if "ev_spreads" in body:
        if not body["ev_spreads"]:
            raise HttpException(400, "No EV spreads provided")

    if "item_ids" in body:
        if not body["item_ids"]:
            raise HttpException(400, "No Item IDs provided")
        else:
            items = app.db.query(Item).filter(Item.id.in_(request.json["item_ids"])).all()

    if "iv_spreads" in body:
        if not body["iv_spreads"]:
            raise HttpException(400, "No IV spreads provided")

    if "move_ids" in body:
        if not body["move_ids"]:
            raise HttpException(400, "No Move IDs provided")
        else:
            moves = app.db.query(Move).filter(Move.id.in_(request.json["move_ids"])).all()

    if "nature_ids" not in body or not body["nature_ids"]:
        raise HttpException(400, "No Nature IDs provided")
    else:
        natures = app.db.query(Nature).filter(Nature.id.in_(request.json["nature_ids"])).all()

    candidate = Candidate()

    if not pokemon:
        raise HttpException(404, "No Pokemon found with the given ID")
    else:
        candidate.pokemon = pokemon

    if not abilities:
        raise HttpException(404, "No Abilities found with the given IDs")
    else:
        candidate.abilities.extend(abilities)

    for ev_spread in request.json["ev_spreads"]:
        ev = CandidateEvSpread()
        ev.candidate_id = candidate.id
        ev.hp = ev_spread["hp"]
        ev.atk = ev_spread["atk"]
        ev._def = ev_spread["def"]
        ev.spatk = ev_spread["spatk"]
        ev.spdef = ev_spread["spdef"]
        ev.spe = ev_spread["spe"]
        ev.sum = ev.hp + ev.atk + ev._def + ev.spatk + ev.spdef + ev.spe
        candidate.candidate_ev_spreads.append(ev)

    if not items:
        raise HttpException(404, "No Items found with the given IDs")
    else:
        candidate.items.extend(items)

    for iv_spread in request.json["iv_spreads"]:
        iv = CandidateIvSpread()
        iv.candidate_id = candidate.id
        iv.hp = iv_spread["hp"]
        iv.atk = iv_spread["atk"]
        iv._def = iv_spread["def"]
        iv.spatk = iv_spread["spatk"]
        iv.spdef = iv_spread["spdef"]
        iv.spe = iv_spread["spe"]
        candidate.candidate_iv_spreads.append(iv)

    if not moves:
        raise HttpException(404, "No Moves found with the given IDs")
    else:
        candidate.moves.extend(moves)

    if not natures:
        raise HttpException(404, "No Natures found with the given IDs")
    else:
        candidate.natures.extend(natures)

    app.db.add(candidate)
    app.db.commit()

    return Response(json.dumps(candidate, cls=new_alchemy_encoder(), check_circular=False), mimetype='application/json')
