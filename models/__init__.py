from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@dataclass
class Player(db.Model):
    id: int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name: str = db.Column(db.String(30))
    classId: int = db.Column(db.Integer, db.ForeignKey('player_class.id'))



@dataclass
class PlayerClass(db.Model):
    id: int = db.Column(db.Integer, primary_key = True,autoincrement=True)
    name: str = db.Column(db.String(30))


@dataclass
class ItemType(db.Model):
    id: int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name: str = db.Column(db.String(30))


@dataclass
class Item(db.Model):
    id: int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name: str = db.Column(db.String(30))
    itemType: int = db.Column(db.Integer, db.ForeignKey('item_type.id'))
    quality: int = db.Column(db.Integer)
    owner: int = db.Column(db.Integer, db.ForeignKey('player.id'))

    def __repr__(self):
        return f"{{'id': {self.id}, 'itemType': {self.itemType}, 'quality': {self.quality}, 'owner': {self.owner}}}"

@dataclass
class LocationType(db.Model):
    id: int = db.Column(db.Integer, primary_key = True,autoincrement=True)
    name: str = db.Column(db.String(30))


@dataclass
class Location(db.Model):
    id: int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    locationNum:str = db.Column(db.String(10))
    locationType: int = db.Column(db.Integer, db.ForeignKey('location_type.id'))
    description: str = db.Column(db.Text)


@dataclass
class Message(db.Model):
    id: int = db.Column(db.Integer, primary_key = True ,autoincrement=True)
    playerFrom: int = db.Column(db.Integer, db.ForeignKey('player.id'))
    playerTo:int  = db.Column(db.Integer, db.ForeignKey('player.id'))
    messageText: str = db.Column(db.String(1000))