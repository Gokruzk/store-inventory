from flask import Flask, request, jsonify, Response, render_template
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)
# test connection
try:
    app.config['MONGO_URI'] = 'mongodb+srv://tidomar:Mongo321@testdb.vqbg6xa.mongodb.net/frutas'
    print('Connected')
except Exception as e:
    print(e)

mongo = PyMongo(app)


@app.route('/products', methods=['POST'])
def add_product():
    # reciving data from html form
    product = request.form['product']
    description = request.form['description']
    price = request.form['price']
    stock = request.form['stock']
    type_ = request.form['type']
    try:
        if product and description and price and stock and type_:
            # insert into mongo collection
            mongo.db.producto.insert_one(
                {
                    "product": product,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "type": type_
                }
            )
        else:
            # show error message
            render_template('messages.html', msg='Fill all the blanks')
    except Exception as e:
        # show error message
        render_template('messages.html', msg='Fill all the blanks')
    # show success message
    return render_template('messages.html', msg='Product added successfully')


@app.route('/products', methods=['GET'])
def view_products():
    response = ''
    try:
        # get products
        products = mongo.db.producto.find()
        response = json_util.dumps(products)
    except Exception as e:
        # show error message
        # print(e)
        render_template('messages.html',
                        msg='An error has occurred while getting products.')
    # sends products information to html
    return render_template('view_products.html', data=Response(response, mimetype='application/json').get_json())
    # return Response(response, mimetype='application/json')


@app.route('/product', methods=['POST'])
def get_product():
    # reciving data from html form
    input_ = request.form['search']
    option = request.form['category']
    response = ""
    try:
        # get product
        product = mongo.db.producto.find({f'{option}': input_})
        response = json_util.dumps(product)
    except:
        # show error message
        render_template('messages.html',
                        msg='An error has occurred while getting the product.')
    # sends products information to html
    return render_template('view_product.html', data=Response(response, mimetype='application/json').get_json())


@app.route('/delete/<string:id_>')
def delete_product(id_):
    try:
        # delete product
        mongo.db.producto.delete_one({'_id': ObjectId(id_)})
    except:
        # show error message
        render_template('messages.html',
                        msg='An error has occurred while deleting the product.')
    # show success message
    return render_template('messages.html', msg='Product deleted successfully')


@app.route('/uproducts/<string:id_>', methods=['POST'])
def update_product(id_):
    try:
        # reciving data from html form
        product = request.form['product']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        type_ = request.form['type']
        if product and description and price and stock and type_:
            # update product
            mongo.db.producto.update_one(
                {"_id": ObjectId(id_)},
                {"$set": {
                    "product": product,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "type": type_
                }
                }
            )
        else:
            # show error message
            render_template('messages.html', msg='Fill all the blanks')
    except:
        # show error message
        render_template('messages.html', msg='Fill all the blanks')
    # show success message
    return render_template('messages.html', msg='Product updated successfully')


# routes
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/add_product')
def add_one():
    return render_template('add_product.html')


@app.route('/get_product')
def get_one():
    return render_template('get_product.html')


@app.route('/delete')
def delete_one():
    response = ''
    try:
        # get products
        products = mongo.db.producto.find()
        response = json_util.dumps(products)
    except:
        # show error message
        render_template('messages.html',
                        msg='An error has occurred while getting products.')
    # sends products information to html
    return render_template('delete_product.html', data=Response(response, mimetype='application/json').get_json())


@app.route('/update')
def update_products():
    response = ''
    try:
        # get products
        products = mongo.db.producto.find()
        response = json_util.dumps(products)
    except:
        # show error message
        render_template('messages.html',
                        msg='An error has occurred while getting products.')
    # sends products information to html
    return render_template('update_products.html', data=Response(response, mimetype='application/json').get_json())


@app.route('/update_form/<string:id_>')
def update_form(id_):
    response = ''
    try:
        # get product information
        products = mongo.db.producto.find_one({'_id': ObjectId(id_)})
        response = json_util.dumps(products)
    except:
        render_template('messages.html',
                        msg='An error has occurred while getting product.')
    return render_template('update_form.html', data=Response(response, mimetype='application/json').get_json())


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
