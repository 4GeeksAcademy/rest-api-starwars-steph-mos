from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planet = relationship("FavoritePlanet", back_populates="user")
    favorite_character = relationship("FavoriteCharacter", back_populates="user")

    def __str__(self): 
        return self.name


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            # "favorite_planet": self.favorite_planet,
            # "favorite_character": self.favorite_character,

            # do not serialize the password, its a security breach
        }
    
    def serialize_relationships (self):        
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "favorite_planet": [planetfav.serialize() for planetfav in self.favorite_planet ],
            "favorite_character": [characterfav.serialize() for characterfav in self.favorite_character]
        }
    
    def serialize_favorite (self):
        return {
            "favorite_planet": [planetfav.serialize() for planetfav in self.favorite_planet ],
            "favorite_character": [characterfav.serialize() for characterfav in self.favorite_character]
        }

    
class Character(db.Model):
    __tablename__='character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    hair_color: Mapped[str] = mapped_column(String, nullable=True)
    eye_color: Mapped[str] = mapped_column(String, nullable=True)
    height: Mapped[str] = mapped_column(Integer, nullable=True)
    weight: Mapped[str] = mapped_column(Integer,nullable=True)

    favorite_character = relationship("FavoriteCharacter", back_populates="character")

    def __str__(self): 
        return self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "height": self.height,
            "weight": self.weight,

        }
    

class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="favorite_character")

    character_id = mapped_column(ForeignKey("character.id"))
    character = relationship("Character", back_populates="favorite_character")

    
    def __str__(self): 
        return str(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "character": self.character.serialize()
        }
    
    
    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[str] = mapped_column(String(100), nullable=True)
    diameter: Mapped[int] = mapped_column(Integer)

    favorite_planet = relationship("FavoritePlanet", back_populates="planet")
    
    def __str__(self): 
        return self.name


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter,
        }
    
    
    
class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="favorite_planet")

    planet_id = mapped_column(ForeignKey("planet.id"))
    planet = relationship("Planet", back_populates="favorite_planet")


    
    def __str__(self): 
        return str(self.id)
    

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "planet":self.planet.serialize()
        }
        
    

 
    

