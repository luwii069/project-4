from . import db
from flask import json


class Member(db.Model):
    __tablename__='member'

    id=db.Column(db.BigInteger,primary_key=True)
    alias=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    game=db.relationship('Game',backref='member',uselist=False,cascade='all, delete-orphan')

    def details(self):
        return {'id':self.id,'alias':self.alias, 'email':self.email}
    
class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.BigInteger, db.ForeignKey('member.id', ondelete='CASCADE'), nullable=False, unique=True)
    deck = db.Column(db.String, nullable=False)
    player_hand = db.Column(db.String, nullable=False)
    computer_hand = db.Column(db.String, nullable=False)
    tablecard = db.Column(db.String, nullable=False)

 
    class Game:
     def __init__(self, member_id):
        self.member_id = member_id
        self.deck = []
        self.player_hand = []
        self.computer_hand = []
        self.tablecard = []

     def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        new_ranks = ['4', '5', '6', '7', '9', '10']
        new_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        return self.deck

     def deal_cards(self, num_cards):
        if len(self.deck) < num_cards:
            return None  # Handle case where not enough cards are available

        # Distribute cards to player_hand
        self.player_hand.extend(self.deck[:num_cards])
        del self.deck[:num_cards]

        # Distribute cards to computer_hand
        self.computer_hand.extend(self.deck[:num_cards])
        del self.deck[:num_cards]

        # Additional logic for tablecard distribution if needed

        return self.player_hand, self.computer_hand
    

        #initializes a new game instance with the provided attributes and 
        #ensures they're stored in a method compatible to databases using 
        #json serialization