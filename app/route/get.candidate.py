# pylint: disable=no-member
import json
from app.exception.httpexception import HttpException
from app.data_access.model.models import new_alchemy_encoder, Candidate
from flask import Response
from app.index import app

@app.route("/candidate/<int:candidate_id>", methods=['GET'])
def get_candidate_by_id(candidate_id):
    candidate = app.db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate is None:
        raise HttpException(404, "Candidate not found")
    return Response(json.dumps(candidate, cls=new_alchemy_encoder(), check_circular=False), mimetype = 'application/json')
