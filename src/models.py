from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class User(db.Model):

    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    planets_favorites: Mapped[list["PlanetFavorite"]] = relationship("PlanetFavorite", back_populates="user", cascade="all, delete-orphan")
    characters_favorites: Mapped[list["CharacterFavorite"]] = relationship("CharacterFavorite", back_populates="user", cascade="all, delete-orphan")
    vehicles_favorites: Mapped[list["VehicleFavorite"]] = relationship("VehicleFavorite", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active
        }
    
    def serialize_favorites(self):
        return {
            "characters": [favorite_character.serialize() for favorite_character in self.characters_favorites] if len(self.characters_favorites) > 0 else [],
            "planets": [favorite_planet.serialize() for favorite_planet in self.planets_favorites] if len(self.planets_favorites) > 0 else [],
            "vehicles": [favorite_vehicle.serialize() for favorite_vehicle in self.vehicles_favorites] if len(self.vehicles_favorites) > 0 else []
        }


class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Character(db.Model):
    __tablename__="characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[enum.Enum] = mapped_column(Enum(GenderEnum), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hair_color: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    height: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    eye_color_color: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    mass: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    users_favorites: Mapped[list["CharacterFavorite"]] = relationship("CharacterFavorite", back_populates="character", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Character {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender.value,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color_color": self.eye_color_color,
            "mass": self.mass,
            "birth_year": self.birth_year,
            "is_active": self.is_active
        }
        
class CharacterFavorite(db.Model):
    __tablename__="characters_favorites"
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("characters.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="characters_favorites")
    character: Mapped["Character"] = relationship(back_populates="users_favorites")

    def __repr__(self):
        return f"User {self.user.username} likes {self.character.name}"

    def serialize(self):
        return self.character.serialize()


class Planet(db.Model):
    __tablename__="planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    terrain: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    diameter: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    gravity: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    orbital_period: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    rotation_period: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    population: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    users_favorites: Mapped[list["PlanetFavorite"]] = relationship("PlanetFavorite", back_populates="planet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Planet {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "is_active": self.is_active
        }

class PlanetFavorite(db.Model):
    __tablename__="planets_favorites"
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), primary_key=True)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey("planets.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="planets_favorites")
    planet: Mapped["Planet"] = relationship(back_populates="users_favorites")

    def __repr__(self):
        return f"User {self.user.username} likes {self.planet.name}"
    
    def serialize(self):
        return self.planet.serialize()


class Vehicle(db.Model):
    __tablename__="vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    consumables: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(170), unique=True, nullable=False)
    crew: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    length: Mapped[float] = mapped_column(Float, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    users_favorites_associations: Mapped[list["VehicleFavorite"]] = relationship("VehicleFavorite", back_populates="vehicle", cascade="all, delete-orphan")

    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "manufacturer": self.manufacturer,
            "crew": self.crew,
            "length": self.length,
            "is_active": self.is_active
        }

class VehicleFavorite(db.Model):
    __tablename__="vehicles_favorites"
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey("vehicles.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="vehicles_favorites")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="users_favorites_associations")

    def __repr__(self):
        return f"User {self.user.username} likes {self.vehicle.name}"
    
    def serialize(self):
        return self.vehicle.serialize()
    
