# pylint: disable=no-member
import json
from app.exception.httpexception import HttpException
from app.data_access.model.models import Candidate
from flask import Response
from app.index import app

@app.route("/candidate", methods=['GET'])
def get_candidate():
    result = app.db.query(Candidate).all()
    return Response(json.dumps(result), mimetype='application/json')
