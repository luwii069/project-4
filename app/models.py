from . import db


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
    __tablename__='game'
    id=db.Column(db.BigInteger,primary_key=True)
    member_id=db.Column(db.BigInteger,db.ForeignKey('member.id',ondelete='CASCADE'),nullable=False,unique=True)
    board=db.Column(db.Text,nullable=False)
    knight_x=db.Column(db.Integer,nullable=False)
    knight_y=db.Column(db.Integer,nullable=False)
    rook_x=db.Column(db.Integer,nullable=False)
    rook_y=db.Column(db.Integer,nullable=False)
    