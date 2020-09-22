from json import dumps
from http import HTTPStatus

from flask import Blueprint, jsonify, session, request
from flask.views import MethodView

from models import db, Item, ItemType, Player, PlayerClass, Location, LocationType, Message

bp = Blueprint('api', __name__)

@bp.route('/item/all')
def show_all_items():
    items = Item.query.all()
    return jsonify(items)

@bp.route('/item', methods = ['POST'])
def create_item():
    request_json = request.json
    print(request_json)


    item_type = request_json.get('itemType')
    quality = request_json.get('quality')
    owner = request_json.get('owner')
    name = request_json.get('name')

    try:
        item = Item(itemType = item_type, quality = quality, owner = owner, name=name)
    except:
        return '', HTTPStatus.CONFLICT

    print(item)
    db.session.add(item)
    db.session.commit()
    return jsonify(item), HTTPStatus.CREATED

class ItemView(MethodView):
    def get(self, item_id):
        item = Item.query.filter_by(id = item_id).first_or_404()
        return jsonify(item), HTTPStatus.OK

    def patch(self, item_id):
        request_json = request.json
        item_type = request_json.get('itemType')
        quality = request_json.get('quality')
        owner = request_json.get('owner')
        item = Item.query.filter_by(id = item_id).first_or_404()

        try:
            if not item_type is None: item.itemType = item_type
            if not quality is None: item.quality = quality
            if not owner is None: item.owner = owner
        except:
            return '', HTTPStatus.CONFLICT

        db.session.add(item)
        db.session.commit()
        return jsonify(item), HTTPStatus.OK


    def delete(self, item_id):
        item = Item.query.filter_by(id = item_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return '',HTTPStatus.NO_CONTENT
bp.add_url_rule('/item/<int:item_id>', view_func=ItemView.as_view('item'))


@bp.route('/item-type/all')
def show_all_item_types():
    item_types = ItemType.query.all()
    return jsonify(item_types)

@bp.route('/item-type/', methods = ['POST'])
def create_item_type():
    request_json = request.json
    name = request_json.get('name')
    try:
        item_type = ItemType(name = name)
    except:
        return '', HTTPStatus.CONFLICT
    db.session.add(item_type)
    db.session.commit()
    return jsonify(item_type), HTTPStatus.CREATED

class ItemTypeView(MethodView):
    def get(self, type_id):
        item_type = ItemType.query.filter_by(id=type_id).first_or_404()
        return jsonify(item_type)

    def patch(self, type_id):
        request_json = request.json
        name = request_json.get('name')
        item_type = ItemType.query.filter_by(id=type_id).first_or_404()

        try:
            if not name is None: item_type.name = name
            db.session.add(item_type)
            db.session.commit()
        except:
            return '', HTTPStatus.BAD_REQUEST
        return jsonify(item_type), HTTPStatus.OK

    def delete(self, type_id):
        item_type = ItemType.query.filter_by(id=type_id).first_or_404()
        try:
            db.session.delete(item_type)
            db.session.commit()
        except:
            return '', HTTPStatus.BAD_REQUEST
        return '', HTTPStatus.NO_CONTENT
bp.add_url_rule('/item-type/<int:type_id>', view_func=ItemTypeView.as_view('itemType'))

@bp.route('/player-class/all')
def show_all_player_classes():
    player_classes = PlayerClass.query.all()
    return jsonify(player_classes)

@bp.route('/player-class/', methods = ['POST'])
def create_player_class():
    request_json = request.json
    name = request_json.get('name')
    try:
        player_class = PlayerClass(name = name)
    except:
        return '', HTTPStatus.CONFLICT
    db.session.add(player_class)
    db.session.commit()
    return jsonify(player_class), HTTPStatus.CREATED

class PlayerClassView(MethodView):
    def get(self, class_id):
        player_class = PlayerClass.query.filter_by(id = class_id).first_or_404()
        return jsonify(player_class), HTTPStatus.OK

    def patch(self, class_id):
        player_class = PlayerClass.query.filter_by(id=class_id).first_or_404()

        request_json = request.json
        name = request_json.get('name')

        try:
            if not name is None: player_class.name = name
        except:
            return '', HTTPStatus.BAD_REQUEST
        db.session.add(player_class)
        db.session.commit()
        return  jsonify(player_class), HTTPStatus.OK

    def delete(self, class_id):
        player_class = PlayerClass.query.filter_by(id=class_id).first_or_404()
        try:
            db.session.delete(player_class)
        except:
            db.session.rollback()
            return '', HTTPStatus.BAD_REQUEST
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
bp.add_url_rule('/player-class/<int:class_id>', view_func=PlayerClassView.as_view('playerClass'))

@bp.route('/player/all')
def show_all_players():
    players = Player.query.all()
    return jsonify(players)

@bp.route('/player/', methods = ['POST'])
def create_player():
    request_json = request.json
    name = request_json.get('name')
    class_id = request_json.get('classId')
    try:
        player = Player(name = name, classId = class_id)
    except:
        return '', HTTPStatus.CONFLICT
    db.session.add(player)
    db.session.commit()
    return jsonify(player), HTTPStatus.CREATED

class PlayerView(MethodView):
    def get(self, player_id):
        player = Player.query.filter_by(id = player_id).first_or_404()
        return jsonify(player), HTTPStatus.OK

    def patch(self, player_id):
        player = Player.query.filter_by(id=player_id).first_or_404()

        request_json = request.json
        name = request_json.get('name')
        class_id = request_json.get('classId')
        try:
            if not name is None: player.name = name
            if not class_id is None: player.classId = class_id
        except:
            return '', HTTPStatus.BAD_REQUEST
        db.session.add(player)
        db.session.commit()
        return jsonify(player), HTTPStatus.OK

    def delete(self, player_id):
        player = Player.query.filter_by(id=player_id).first_or_404()
        try:
            db.session.delete(player)
            db.session.commit()
        except:
            db.session.rollback()
            return '', HTTPStatus.BAD_REQUEST
        return '', HTTPStatus.NO_CONTENT

bp.add_url_rule('/player/<int:player_id>', view_func=PlayerView.as_view('player'))

@bp.route('/location/all')
def show_all_locations():
    locations = Location.query.all()
    return jsonify(locations)

@bp.route('/location', methods = ['POST'])
@bp.route('/location/', methods = ['POST'])
def create_location():
    request_json = request.json
    location_num = request_json.get('locationNum')
    location_type = request_json.get('locationType')
    description = request_json.get('description')
    try:
        location = Location(locationNum = location_num, locationType = location_type, description = description)
    except:
        return '', HTTPStatus.CONFLICT
    db.session.add(location)
    db.session.commit()
    return jsonify(location), HTTPStatus.CREATED

class LocationView(MethodView):
    def get(self, location_id):
        location = Location.query.filter_by(id = location_id).first_or_404()
        return jsonify(location), HTTPStatus.OK

    def patch(self, location_id):
        location = Location.query.filter_by(id=location_id).first_or_404()

        request_json = request.json
        location_num = request_json.get('locationNum')
        location_type = request_json.get('locationType')
        description = request_json.get('description')
        try:
            if not location_num is None: location.locationNum = location_num
            if not location_type is None: location.locationType = location_type
            if not description is None: location.description = description
        except:
            return '', HTTPStatus.BAD_REQUEST
        db.session.add(location)
        db.session.commit()
        return jsonify(location), HTTPStatus.CREATED

    def delete(self, location_id):
        location = Location.query.filter_by(id = location_id).first_or_404()
        try:
            db.session.delete(location)
            db.session.commit()
        except:
            db.session.rollback()
            return '', HTTPStatus.BAD_REQUEST
        return '', HTTPStatus.NO_CONTENT
bp.add_url_rule('/location/<int:location_id>', view_func=LocationView.as_view('location'))

@bp.route('/location-type/all')
def show_all_location_types():
    location_types = LocationType.query.all()
    return jsonify(location_types)

@bp.route('/location-type', methods = ['POST'])
@bp.route('/location-type/', methods = ['POST'])
def create_location_type():
    request_json = request.json
    name = request_json.get('name')
    try:
        location_type = LocationType(name=name)
    except:
        return '', HTTPStatus.CONFLICT
    db.session.add(location_type)
    db.session.commit()
    return jsonify(location_type), HTTPStatus.CREATED

class LocationTypeView(MethodView):
    def get(self, type_id):
        location_type = LocationType.query.filter_by(id = type_id).first_or_404()
        return jsonify(location_type), HTTPStatus.OK

    def patch(self, type_id):
        request_json = request.json
        name = request_json.get('name')
        location_type = LocationType.query.filter_by(id=type_id).first_or_404()

        try:
            if not name is None: location_type.name = name
            db.session.add(location_type)
            db.session.commit()
        except:
            return '', HTTPStatus.BAD_REQUEST
        return jsonify(location_type), HTTPStatus.OK

    def delete(self, type_id):
        location_type = LocationType.query.filter_by(id = type_id).first_or_404()
        try:
            db.session.delete(location_type)
            db.session.commit()
        except:
            db.session.rollback()
            return '', HTTPStatus.BAD_REQUEST
        return '', HTTPStatus.NO_CONTENT
bp.add_url_rule('/location-type/<int:type_id>', view_func=LocationTypeView.as_view('locationType'))

@bp.route('/message/all')
def show_all_messages():
    messages = Message.query.all()
    return jsonify(messages)

@bp.route('/message', methods = ['POST'])
@bp.route('/message/', methods = ['POST'])
def create_message():
    request_json = request.json
    player_from = request_json.get('playerFrom')
    player_to = request_json.get('playerTo')
    message_text = request_json.get('messageText')

    try:
        message = Message(playerTo = player_to, playerFrom = player_from, messageText = message_text)
    except:
        return '', HTTPStatus.CONFLICT

    db.session.add(message)
    db.session.commit()
    return jsonify(message), HTTPStatus.CREATED

class MessageView(MethodView):
    def get(self, message_id):
        message = Message.query.filter_by(id = message_id).first_or_404()
        return jsonify(message), HTTPStatus.OK

    def patch(self, message_id):
        message = Message.query.filter_by(id = message_id).first_or_404()

        request_json = request.json
        player_from = request_json.get('playerFrom')
        player_to = request_json.get('playerTo')
        message_text = request_json.get('messageText')

        try:
            if not player_from is None: message.playerFrom = player_from
            if not player_to is None: message.playerTo = player_to
            if not message_text is None: message.messageText = message_text
        except:
            return '', HTTPStatus.BAD_REQUEST

        db.session.add(message)
        db.session.commit()
        return jsonify(message), HTTPStatus.OK

    def delete(self, message_id):
        message = Message.query.filter_by(id = message_id).first_or_404()
        try:
            db.session.delete(message)
            db.session.commit()
        except:
            db.session.rollback()
            return '', HTTPStatus.BAD_REQUEST
        return '', HTTPStatus.NO_CONTENT
bp.add_url_rule('/message/<int:message_id>', view_func=MessageView.as_view('message'))