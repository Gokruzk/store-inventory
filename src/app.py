from flask import Flask, request, jsonify, Response, render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util, ObjectId

app = Flask(__name__)
database = 'pymongodb'
app.config['MONGO_URI'] = 'mongodb+srv://tidomar:Mongo321@testdb.vqbg6xa.mongodb.net/frutas'
mongo = PyMongo(app)


@app.route('/products', methods=['POST'])
def add_product():
    # reciving data from html form
    try:
        product = request.form['product']
        description = request.form['description']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']
        type_ = request.form['type']
        query = ''
        print(product)
        if product and description and price and image and stock and type_:
            # insert into mongo collection
            query = mongo.db.producto.insert_one(
                {
                    "product": product,
                    "description": description,
                    "price": price,
                    "image": image,
                    "stock": stock,
                    "type": type_
                }
            )
        else:
            render_template('messages.html', msg='Fill all the blanks')
    except:
        render_template('messages.html', msg='Fill all the blanks')
    return render_template('messages.html', msg='Inserted succesfully')


@app.route('/products', methods=['GET'])
def view_products():
    response = ''
    try:
        products = mongo.db.producto.find()
        response = json_util.dumps(products)
    except:
        render_template('messages.html',
                        msg='An error has occurred while getting products.')
    return render_template('view_products.html', data=Response(response, mimetype='application/json').get_json())
    # return Response(response, mimetype='application/json')


@app.route('/product', methods=['POST'])
def get_product():
    input_ = request.form['search']
    option = request.form['category']
    # product = mongo.db.producto.find({'product': input_})
    # response = json_util.dumps(product)
    # print(response)
    response = ""
    try:
        product = mongo.db.producto.find({f'{option}': input_})
        response = json_util.dumps(product)
    except:
        render_template('messages.html',
                        msg='An error has occurred while getting the product.')
    return render_template('view_product.html', data=Response(response, mimetype='application/json').get_json())


@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
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


@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
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


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/add_product')
def add_one():
    return render_template('add_product.html')


@app.route('/get_product')
def get_one():
    return render_template('get_product.html')


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
