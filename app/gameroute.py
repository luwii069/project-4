from flask import Blueprint, jsonify,json, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Game
from . import db
from .game_engine import game  # Assuming your game_engine module is imported correctly

game_blueprint = Blueprint('game', __name__)

from flask import Blueprint, jsonify,json, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Game
from . import db
from .game_engine import game  # Assuming your game_engine module is imported correctly

game_blueprint = Blueprint('game', __name__)

@game_blueprint.route("/game/new-game", methods=["GET"])
@jwt_required()
def new_game():
    current_user = get_jwt_identity()

    # Check if a game already exists for the current user
    game = Game.query.filter_by(member_id=current_user['id']).first()
    if game:
        return jsonify({'message': "Game already exists for this user"}), 400

    # Create a new game instance
    new_deck = []
    new_game = Game(member_id=current_user['id'], deck=json.dumps(new_deck),
                    player_hand=json.dumps([]), computer_hand=json.dumps([]),
                    tablecard=json.dumps([]))

    db.session.add(new_game)
    db.session.commit()

    return jsonify({'message': "New game started"}), 200

#NB the game route route ain't working yet

@game_blueprint.route("/game/make-move", methods=["PUT"])
@jwt_required()
def make_move():
    body = request.get_json()
    rank = body.get("rank")
    suit = body.get("suit")
    
    current_user = get_jwt_identity()
    game = Game.query.filter_by(member_id=current_user['id']).first()
    
    if not game:
        return jsonify({'message': "Game not found"}), 400
    
    deck = json.loads(game.deck)#.loads desirializes json code to python obect
    player_hand = json.loads(game.player_hand)
    computer_hand = json.loads(game.computer_hand)
    tablecard = json.loads(game.tablecard)
    
    play = (rank, suit)
    
    if play in player_hand and (play[0] == tablecard[-1][0] or play[1] == tablecard[-1][1]):
        tablecard.append(play)
        player_hand.remove(play)
        
        if play[0] == "A":
            newsuit = input("Enter the new card suit: ").capitalize().strip()
            tablecard[-1] = (tablecard[-1][0], newsuit)
            print(f"The game was changed to {newsuit}")
        
        if play[0] in ["2", "3", "K", "J", "8", "Q"]:
            game.handle_special_card(play, computer_hand, deck)
        
        game.deck = json.dumps(deck)#serializes python code to json objects 
        game.player_hand = json.dumps(player_hand)
        game.computer_hand = json.dumps(computer_hand)
        game.tablecard = json.dumps(tablecard)
        
        db.session.commit()
        
        # Trigger computer's turn after player's move
        game.computer_turn(player_hand, computer_hand, tablecard, deck)
        
        return jsonify({'message': "Move made successfully"}), 200
    
    return jsonify({'message': "Invalid move"}), 400