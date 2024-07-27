from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):
    count = users.count_documents({"Username": username})
    return count > 0

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)



api.add_resource(Register, '/register')


if __name__=="__main__":
    app.run(host='0.0.0.0')