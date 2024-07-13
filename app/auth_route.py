from flask import Blueprint,jsonify,request

from flask_jwt_extended import create_access_token,JWTManager

from . import db,bcrypt

from datetime import timedelta,datetime,timezone

from .models import Member,Game

#from .game_engine import create_board,init_knight,init_rook

import json


auth_blueprint=Blueprint('auth',__name__)#name of blue print
#signing up route
@auth_blueprint.route("/signup",methods=["POST"])
def signup():
    body=request.get_json()
    alias=body.get('alias')
    email=body.get('email')
    password=body.get('password')

    ## Validation
    if not email or not password or not alias:
        return jsonify({'message':"Required field missing"}),400
    
    if len(email)<4:
        return jsonify({'message':"Email too short"}),400
    
    if len(alias)<4:
        return jsonify({'message':"Name too short"}),400
    
    if len(password)<4:
        return jsonify({'message':"Password too short"}),400
    
    existing_member=Member.query.filter_by(email=email).first()

    if existing_member:
        return jsonify({'message':f"Email already in use {email}"}),400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
    
    member=Member(alias=alias,email=email,password=hashed_password)
    db.session.add(member)
    db.session.commit()
    return jsonify({"message":"Sign up success"}),201
    
@auth_blueprint.route("/login",methods=["POST"])
def login():
    body=request.get_json()
    email=body.get('email')
    password=body.get('password')

        ## Validation
    if not email or not password:
        return jsonify({'message':"Required field missing"}),400
    user=Member.query.filter_by(email=email).first()

 
    if not user:
        return jsonify({'message':"User not found"}),400
    
    
    pass_ok=bcrypt.check_password_hash(user.password.encode('utf-8'),password)
    
    if not pass_ok:
        return jsonify({"message":"Invalid password"}),401

    expires=datetime.utcnow()+timedelta(hours=24)
    ## ACCESS TOKEN
    access_token=create_access_token(identity={"id":user.id,"alias":user.alias,"role":"cats and dogs"},expires_delta=(expires-datetime.utcnow()))
   
    #if not user.game:
        #member_id=user.id
        #board=create_board()
        #knight_x=init_knight['x']
        #knight_y=init_knight['y']
        #rook_x=init_rook['x']
        #rook_y=init_rook['y']
        #board[knight_y][knight_x]="BN"
        #board[rook_y][rook_x]="WR"
        #print(board)
        #board=json.dumps(board)
        #print(board)
        #game=Game(member_id=member_id,board=board,rook_x=rook_x,rook_y=rook_y,knight_x=knight_x,knight_y=knight_y)
        #db.session.add(game)
        #db.session.commit()
        #idk how to give a game to a player that has not gotten any game i mean a new player must be given a new game that sasa 

    return jsonify({'user':user.details(),'token':access_token})
    
      #This Flask blueprint (auth_blueprint) defines two routes (/signup and /login)
      #  for handling user registration and authentication using JWT. It integrates
      #  with your database (db), uses password hashing (bcrypt), and generates JWT 
      # tokens (create_access_token) for authenticated users. Additionally, 
      # it initializes a game for users upon successful login if they don't
      #  already have an existing game. Each route handles request validation 
      # and responds with appropriate JSON messages or data.