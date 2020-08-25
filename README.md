sqlacodegen mysql://root:compaq@localhost/pkmn_breed > models.py

$env:FLASK_ENV = "development"
$env:FLASK_APP = "app.main:app"
flask run