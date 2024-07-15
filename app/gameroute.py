from flask import Blueprint, jsonify, request,json
from flask_jwt_extended import jwt_required, get_jwt_identity
from.models import Game, Member
from. import db
from .utils import initialize_deck
import random
game_blueprint = Blueprint('game', __name__)

@game_blueprint.route("/game/new-game", methods=["GET"])
@jwt_required()
def new_game():
    current_user = get_jwt_identity()

    # Checking  if a game already exists for the current user
    game = Game.query.filter_by(member_id=current_user['id']).first()
    if game:
        return jsonify({'message': "Game already exists for this user"}), 400

    #creating a new game instance for the player if he has no game 
    new_deck = []
    new_game = Game(member_id=current_user['id'], deck=json.dumps(new_deck),
                    player_hand=json.dumps([]), computer_hand=json.dumps([]),
                    tablecard=json.dumps([]))

    db.session.add(new_game)
    db.session.commit()
    
    return jsonify({'message': "New game started"}), 200
    
@game_blueprint.route("/game/deal-cards", methods=["GET"])
@jwt_required()
def deal_cards():
    current_user = get_jwt_identity()
    game = Game.query.filter_by(member_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "Game not found"}), 400
    # Initialize the deck and deal cards
    initialize_deck(game)

    return jsonify({'message': "Cards dealt"}), 200

@game_blueprint.route("/game/make-move", methods=["PUT"])
@jwt_required()
def make_move():
    body = request.get_json()
    rank = body.get("rank")
    suit = body.get("suit")
    current_user = get_jwt_identity()
    game = Game.query.filter_by(member_id=current_user['id']).first()#identify current user
    if not game:
        return jsonify({'message': "Game not found"}), 400

    # Get the current state of the game
    player_hand = json.loads(game.player_hand)
    computer_hand = json.loads(game.computer_hand)
    tablecard = json.loads(game.tablecard)
    deck = json.loads(game.deck)

    # Check if the player has the card in their hand
    play = (rank, suit)
    if play in player_hand:
        # Check if the move is valid (i.e., the card matches the rank or suit of the top card on the table)
        if not tablecard or (play[0] == tablecard[-1][0] or play[1] == tablecard[-1][1]):
            # Remove the card from the player's hand and add it to the table
            player_hand.remove(play)
            tablecard.append(play)

            # Update gamestate
            game.player_hand = json.dumps(player_hand)
            game.tablecard = json.dumps(tablecard)
            db.session.commit()

            # Check if the computer can make a move
            if computer_hand:
                # here its  a valid move for the computer by iterating through its cards and finding the one that matces the table card
                valid_moves = [play for play in computer_hand if (not tablecard or (play[0] == tablecard[-1][0] or play[1] == tablecard[-1][1]))]
                if valid_moves:
                    computer_move = random.choice(valid_moves)
                    computer_hand.remove(computer_move)
                    tablecard.append(computer_move)

                    
                    game.computer_hand = json.dumps(computer_hand)
                    game.tablecard = json.dumps(tablecard)
                    db.session.commit()

            return jsonify({'message': "Move made"}), 200
        else:
            return jsonify({'message': "Invalid move"}), 400
    else:
        return jsonify({'message': "You don't have that card in your hand"}), 400

@game_blueprint.route("/game/winner", methods=["GET"])
@jwt_required()
def winner():
    current_user = get_jwt_identity()
    game = Game.query.filter_by(member_id=current_user['id']).first()
    if not game:
        return jsonify({'message': "Game not found"}), 400
    player_hand = json.loads(game.player_hand)
    computer_hand = json.loads(game.computer_hand)
    # winner logic here
    return jsonify({'message': "Winner determined"}), 200