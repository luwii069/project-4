from. import db
from flask import json


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.BigInteger, primary_key=True)
    alias = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # one-to-many track which games belong to which members(player can have multiple games)
    games = db.relationship('Game', backref='member', lazy=True)

    def details(self):
        return {'id': self.id, 'alias': self.alias, 'email': self.email}

class Card(db.Model): # static data for all possible cards
    __tablename__ = 'card'

    id = db.Column(db.BigInteger, primary_key=True)
    suit = db.Column(db.String(10), nullable=False)
    rank = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.BigInteger, db.ForeignKey('member.id', ondelete='CASCADE'), nullable=False)

#many-to-many relationship(game-card)
#manage the deck of cards used in the game
#(tseme allows for easier shuffling)
    deck = db.relationship('Card', secondary='game_card', backref='games')

#One-to-many(game-game card)  manage player's hand, computer's hand, and table cards
    player_hand = db.relationship('GameCard', backref='player_game', lazy=True, cascade='all, delete-orphan')
    computer_hand = db.relationship('GameCard', backref='computer_game', lazy=True, cascade='all, delete-orphan')
    tablecard = db.relationship('GameCard', backref='table_game', lazy=True, cascade='all, delete-orphan')
#nb each card displays each instance for player comps and table 
class GameCard(db.Model):
    __tablename__ = 'game_card'

    game_id = db.Column(db.BigInteger, db.ForeignKey('game.id'), primary_key=True)
    card_id = db.Column(db.BigInteger, db.ForeignKey('card.id'), primary_key=True)

    #many-to-one relationship with Game, establishing a connection between GameCard and Game
    game = db.relationship('Game', backref='game_cards')
    card = db.relationship('Card', backref='game_cards')
    #establish associations between specific games and specific cards.