"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    results = list(map(lambda user: user.serialize_relationships(), users))
   
    return jsonify(results), 200



@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)

    response_body = {
        "user": user.serialize()
    }
    
    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_characters():
    all_characters = Character.query.all()
    results = list(map(lambda character: character.serialize(), all_characters))

    response_body = {
        "msg": "Here is your characters list ",
        "character_id": results
    }

    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = db.session.get(Character, people_id)

    response_body = {
        "user": character.serialize()
    }
    
    return jsonify(response_body), 200


@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))


    response_body = {
        "msg": "Here is your planet list ",
        "planet_id": results
    }

    return jsonify(response_body), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = db.session.get(Planet, planet_id)

    response_body = {
        "user": planet.serialize()
    }
    
    return jsonify(response_body), 200


@app.route('/user/favorite/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = db.session.get(User, user_id)

    

    return {
        "msg": "Here is your favorites list ",
        "favorites": user.serialize_favorite()
    } , 200




@app.route('/user/favorite', methods=['GET'])
def get_users_favorites():
    all_favorite_planets = db.session.execute(select(FavoritePlanet)).scalars().all()
    all_favorite_characters = db.session.execute(select(FavoriteCharacter)).scalars().all()
    
    planetsfav = [planet.serialize() for planet in all_favorite_planets]
    charactersfav = [character.serialize() for character in all_favorite_characters]

    return {
        "msg": "Here is your favorites list ",
        "favorite_planets": planetsfav,
        "favorite_characters": charactersfav,
    } , 200





@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    user = db.session.execute(select(User)).scalars().first()
    planet = db.session.execute(select(Planet).where(Planet.id == planet_id)).scalar_one()


    if planet is None:
        return {
        "msg": "Something happened, the planet does not exist"
    } , 401
    
    favorite_planet = FavoritePlanet (user_id=user.id, planet_id=planet.id)

    db.session.add(favorite_planet)
    db.session.commit()

    return {
        "msg": "You have add a favorite planet"
    } , 200



@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_character(people_id):
    user = db.session.execute(select(User)).scalars().first()
    character = db.session.execute(select(Character).where(Character.id == people_id)).scalar_one()

    if character is None:
        return {
        "msg": "Something happened, the character does not exist"
    } , 401
    
    favorite_character = FavoriteCharacter (user_id=user.id, character_id=character.id)

    db.session.add(favorite_character)
    db.session.commit()

    return {
        "msg": "You have add a favorite character"
    } , 200




@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    
    favorite_planet = db.session.execute(select(FavoritePlanet).where(FavoritePlanet.id == planet_id)).scalars().first()

    print(favorite_planet)

    if favorite_planet is None:
        return {
        "msg": "Something happened, the favorite planet does not exist"
    } , 401
    

    db.session.delete(favorite_planet)
    db.session.commit()

    return {
        "msg": "You have delete a favorite planet"
    } , 200
    

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_character(people_id):
    
    favorite_character = db.session.execute(select(FavoriteCharacter).where(FavoriteCharacter.id == people_id)).scalars().first()


    if favorite_character is None:
        return {
        "msg": "Something happened, the favorite character does not exist"
    } , 401
    

    db.session.delete(favorite_character)
    db.session.commit()

    return {
        "msg": "You have delete a favorite character"
    } , 200







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
