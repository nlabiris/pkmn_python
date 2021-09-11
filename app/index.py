from app.exception.httpexception import HttpException
from app.data_access.core.db import Database
from flask import Flask, jsonify

database = Database()
database.create_engine("mysql://root:compaq@localhost/pkmn_breed")
database.bind_engine()
database.create_session()
app = Flask(__name__)
app.db = database.session

import app.route

@app.errorhandler(HttpException)
def custom_http_exception(exception):
    return jsonify({
        "success": False,
        "description": str(exception),
        "error": exception.errorcode
    }), exception.errorcode

@app.errorhandler(Exception)
def internal_server_error(exception):
    return jsonify({
        "success": False,
        "description": str(exception),
        "error": 500
    }), 500

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.db.remove()

if __name__ == "__main__":
    app.run(debug=True)
