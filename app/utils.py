
#function that inserts the 52 cards into the Card 
# table and associates 
# them with the Game object through the GameCard junction table
from .models import Game, Card, GameCard,db

def initialize_deck(game):
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    for suit in suits: #Iterates through each combination of suit and rank to create a Card instance.
        for rank in ranks:
            card = Card(suit=suit, rank=rank)
            db.session.add(card)
            db.session.commit()

            game_card = GameCard(game_id=game.id, card_id=card.id)# new GameCard instance linking the game.id and card.id
            db.session.add(game_card)
            db.session.commit()
            #ensures each game has its unique set of cards while maintaining data organization and efficiency

    
    for i in range(4):
        card = game.deck.pop()
        game.player_hand.append(card)
        db.session.commit()

        card = game.deck.pop()
        game.computer_hand.append(card)
        db.session.commit()

    #table card
    game.tablecard = game.deck.pop()
    db.session.commit()
    #nb how to set the 2nd deck