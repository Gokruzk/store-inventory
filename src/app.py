from flask import Flask, request, jsonify, Response, render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util, ObjectId

app = Flask(__name__)
database = 'pymongodb'
app.config['MONGO_URI'] = f'mongodb://localhost:27017/{database}'
mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():
    # reciving data from html form
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username and email and password:
            #hash password
            hashed_password = generate_password_hash(password)
            #insert into mongo collection
            id = mongo.db.users.insert_one(
                {
                    "username": username,
                    "email": email,
                    "password": hashed_password
                }
            )
            response = {
                "id": str(id),
                "username": username,
                "email": email,
                "password": hashed_password
            }
            return response
    except:
        print('An error has occurred while creating the user.')
    else:
        return not_found()
    return {' message': ' received'}


@app.route('/users', methods=['GET'])
def get_users():
    response = ''
    try:
        users = mongo.db.users.find()
        response = json_util.dumps(users)
    except:
        print('An error has occurred while getting users.')
    return render_template('view_users.html', data=Response(response, mimetype='application/json').get_json())
    # return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    response = ''
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        response = json_util.dumps(user)
    except:
        print('An error has occurred while getting the user.')
    return Response(response, mimetype='application/json')


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    response = ''
    try:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = jsonify({
            "message": "User deleted",
            "status": 200
        })
        response.status_code = 200
    except:
        print('An error has occurred while removing the user.')
        not_found()
    return response


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    # reciving data
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if username and email and password:
            hashed_password = generate_password_hash(password)
            mongo.db.users.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "username": username,
                    "email": email,
                    "password": hashed_password
                }
                }
            )
            response = jsonify({
                "message": "User updated",
                "status": 200
            })
            response.status_code = 200
            return response
    except:
        print('An error has occurred while creating the user.')
    else:
        return not_found()
    return {' message': ' received'}


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/help')
def help_page():
    return render_template('help.html')


@app.route('/create')
def create_use():
    return render_template('create.html')


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        "message": "Bad request: " + request.url,
        "status": 404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
