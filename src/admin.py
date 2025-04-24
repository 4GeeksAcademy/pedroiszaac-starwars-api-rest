import os
from flask_admin import Admin
from models import db, User, Character, CharacterFavorite, Planet, PlanetFavorite, Vehicle, VehicleFavorite
from flask_admin.contrib.sqla import ModelView

class UserView(ModelView): 
    column_list = ("id", "username", "email", "password", "is_active", "planets_favorites", "characters_favorites", "vehicles_favorites")

class CharacterView(ModelView):
    column_list = ("id", "name", "gender", "skin_color", "hair_color", "height", "eye_color", "mass", "birth_year", "is_active", "users_favorites")

class CharacterFavoriteView(ModelView):
    column_list = ("user_id", "character_id", "user", "character")

class PlanetView(ModelView):
    column_list = ("id", "name", "terrain", "climate", "diameter", "gravity", "orbital_period", "rotation_period", "population", "is_active", "users_favorites")

class PlanetFavoriteView(ModelView):
    column_list = ("user_id", "planet_id", "user", "planet")

class VehicleView(ModelView):
    column_list = ("id", "name", "model", "manufacturer", "length", "crew", "cargo_capacity", "consumables", "vehicle_class", "is_active", "users_favorites_associations")

class VehicleFavoriteView(ModelView):
    column_list = ("user_id", "vehicle_id", "user", "vehicle")

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserView(User, db.session))
    admin.add_view(CharacterView(Character, db.session))
    admin.add_view(CharacterFavoriteView(CharacterFavorite, db.session))
    admin.add_view(PlanetView(Planet, db.session))
    admin.add_view(PlanetFavoriteView(PlanetFavorite, db.session))
    admin.add_view(VehicleView(Vehicle, db.session))
    admin.add_view(VehicleFavoriteView(VehicleFavorite, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))