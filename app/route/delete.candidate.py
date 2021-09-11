# pylint: disable=no-member
from app.exception.httpexception import HttpException
from app.data_access.model.models import Candidate
from flask import jsonify
from app.index import app

@app.route("/candidate/<int:candidate_id>", methods=['DELETE'])
def delete_candidate(candidate_id):
    candidate = app.db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate is None:
        raise HttpException(404, "Candidate not found")
    app.db.delete(candidate)
    app.db.commit()
    return jsonify({
        "success": True,
        "description": f"Candidate with ID {candidate_id} was deleted successfully"
    })
