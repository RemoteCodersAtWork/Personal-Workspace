from flask import request, Flask, Blueprint, jsonify
from werkzeug.security import generate_password_hash
from models import db, User
import random
import string

registerBp = Blueprint('registerBp', __name__)

class Register(Resource):
    
    @registerBp.route("/getUser", methods=["GET"])
    def getUser():
        users = User.query.all()
        user_list = []
        for i in range(0, len(users)):
            user_list.append(users[i].serialize())
        return jsonify({ "status" : str(user_list)}), 200

    @registerBp.route('/addUser', methods=["POST"])    
    def addUser():
        json_data = request.get_json(force=True)
        if not json_data:
               return jsonify({'message': 'No input data provided'}), 400

        user = User.query.filter_by(email=json_data['email'].lower()).first()
        if user:
            return jsonify({'message': 'Email address already exists'}), 400
        
        response = requests.get("https://isitarealemail.com/api/email/validate", params = {'email': email})
        status = response.json()['status']
        if status != "valid":
            return jsonify({'message': 'Email address does not exist/cannot be found'}), 400

        user = User(
            firstname = json_data['firstname'],
            lastname = json_data['lastname'],
            number = json_data['number'],
            email = json_data['email'],
            password = generate_password_hash(json_data['password'])
        )
        db.session.add(user)
        db.session.commit()

        result = User.serialize(user)
        
        return jsonify({ "status": 'success', 'data': result }), 201