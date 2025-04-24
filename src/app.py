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
from models import db, User, Character, CharacterFavorite, Planet, PlanetFavorite, Vehicle, VehicleFavorite
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

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if len(users) < 1:
        return jsonify({"msg": "not found"}), 404
    
    serialized_users = [user.serialize() for user in users]

    return jsonify(serialized_users), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "not found"}), 404
    serialized_favorites = user.serialize_favorites()
    return jsonify(serialized_favorites), 200


@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    if len(characters) < 1:
        return jsonify({"msg": "not found"}), 404
    
    serialized_characters = [character.serialize() for character in characters]

    return jsonify(serialized_characters), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"msg": "not found"}), 404

    return jsonify(character.serialize()), 200


@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_character_to_favorites(user_id, character_id):
    favorite_exists = CharacterFavorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite_exists:
        return jsonify({"msg": "already exists"}), 400
    
    new_favorite = CharacterFavorite(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "added character favorite"}), 200


@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def delete_character_from_favorites(user_id, character_id):
    favorite_exists = CharacterFavorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite_exists:
        return jsonify({"msg": "favorite not found"}), 404
    
    db.session.delete(favorite_exists)
    db.session.commit()
    return jsonify({"msg": "deleted character favorite"}), 200



@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    if len(planets) < 1:
        return jsonify({"msg": "not found"}), 404
    
    serialized_planets = [planet.serialize() for planet in planets]

    return jsonify(serialized_planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "not found"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorites(user_id, planet_id):
    favorite_exists = PlanetFavorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_exists:
        return jsonify({"msg": "already exists"}), 400
    
    new_favorite = PlanetFavorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "added planet favorite"}), 200


@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_from_favorites(user_id, planet_id):
    favorite_exists = PlanetFavorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite_exists:
        return jsonify({"msg": "favorite not found"}), 404
    
    db.session.delete(favorite_exists)
    db.session.commit()
    return jsonify({"msg": "deleted planet favorite"}), 200


@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    if len(vehicles) < 1:
        return jsonify({"msg": "not found"}), 404
    
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]

    return jsonify(serialized_vehicles), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg": "not found"}), 404

    return jsonify(vehicle.serialize()), 200


@app.route('/favorite/user/<int:user_id>/vehicle/<int:vehicle_id>', methods=['POST'])
def add_vehicle_to_favorites(user_id, vehicle_id):
    favorite_exists = VehicleFavorite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if favorite_exists:
        return jsonify({"msg": "already exists"}), 400
    
    new_favorite = VehicleFavorite(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "added vehicle favorite"}), 200


@app.route('/favorite/user/<int:user_id>/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_from_favorites(user_id, vehicle_id):
    favorite_exists = VehicleFavorite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if not favorite_exists:
        return jsonify({"msg": "favorite not found"}), 404
    
    db.session.delete(favorite_exists)
    db.session.commit()
    return jsonify({"msg": "deleted vehicle favorite"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
