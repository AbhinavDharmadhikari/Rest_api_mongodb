import os
import json
import pymongo
from flask import Flask, jsonify
from flask import request
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("logfile")

formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

client = MongoClient()

app = Flask(__name__)

mongo_db_name = os.environ.get('MONGO_DB_NAME', default="first_db")
mongo_collection_name = os.environ.get('MONGO_COLLECTION_NAME', default="employeeinformation")

db = client[mongo_db_name]
collection = db[mongo_collection_name]


@app.route("/insert", methods=['POST'])
def insert_document():
    try:
        req_data = request.get_json()
        name = req_data['name']
        contact = req_data['contact']
        collection.insert_one(req_data).inserted_id
        d = {"status": "success"}
        return json.dumps(d)
    except Exception:
        logger.warning("Please fill mandatory filed to inert data i.e name and contact")


@app.route("/u", methods=['POST'])
def update():
    try:
        req_data = request.get_json()
        where = req_data['where']
        set = {"$set": req_data['set']}
        collection.update_one(where, set)
        d = {'status': 200}
        return json.dumps(d)
    except Exception:
        logger.info("please check where and set clause")


@app.route("/d", methods=['POST'])
def delete():
    try:
        req_data = request.get_json()
        delete = req_data['delete']
        collection.delete_one(delete)

        d = {"status": 200}
        return json.dumps(d)
    except Exception:
        logger.info("cannot delete without using delete clause")


@app.route('/v', methods=["GET"])
def findAll():
    try:
        query = collection.find()
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i += 1
        return jsonify(output)
    except Exception:
        logger.error("error in finding all")

    finally:
        logger.error(("How to get this resolved"))


@app.route("/find_one", methods=['POST'])
def find_one():
    for x in collection.find({}, {"name": request.get_json()['name'] , "contact": request.get_json()['contact']}):
        x.pop("_id")
        print(x)

        return jsonify(x)

@app.route("/sort",methods = ['POST'])
def sorting():
    x = collection.find({},{"name":request.get_json()['name']})
    print(x)
    # x.pop("_id")
    # print(x)

if __name__ == '__main__':
    app.run(debug=True, port= 6001)



