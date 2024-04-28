# Store inventory

Store inventory is a Flask app for store products using a mongodb as database.

## Installation

Go to mongodb page to download [mongodb community server](https://www.mongodb.com/try/download/community) and [mongosh](https://www.mongodb.com/try/download/atlascli).

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the followings modules.

```bash
> pip install flask
> pip install pymongo
> pip install flask_pymongo
```
## Database
Use the shell to run mongodb
```bash
> mongod
```
Use mongosh to create database
```bash
> mongosh
> use frutas
> db.createCollection("products")
```
## License

[MIT](https://choosealicense.com/licenses/mit/)