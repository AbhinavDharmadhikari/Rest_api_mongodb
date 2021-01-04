import os
import json
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
        logger.debug(req_data)
        name = req_data.get('name', None)
        contact = req_data.get('contact', None)
        if name is None:
            raise KeyError('name')
        if contact is None:
            raise KeyError('contact')
        # name = req_data['name']
        # contact = req_data['contact']
        resp = collection.insert_one(req_data).inserted_id
        logger.debug(resp)
        d = {"status": "success"}
        return json.dumps(d)
    except KeyError as e:
        logger.error(f"mandatory field {e} is not found")
        d = f"mandatory field {e} is not found"
        return json.dumps({"message": d})

    except Exception as e:
        logger.error(f"Server faced an unknown problem:{e}")
        d = f"Server faced an unknown problem:{e}"
        return json.dumps({"message": d})


@app.route("/u", methods=['POST'])
def update():
    try:
        req_data = request.get_json()
        where = req_data['where']
        set = req_data['set']
        collection.update_one(where, set)
        d = {'status': 200}
        return json.dumps(d)
    except KeyError as e:
        logger.error(f"please check {e} clause")
        d = f"please check {e} clause"
        return json.dumps({"message": d})

    except Exception as e:
        logger.error(f"Server faced an unknown problem:{e}")
        d = f"Server faced an unknown problem:{e}"
        return json.dumps({"message": d})


@app.route("/d", methods=['POST'])
def delete():
    try:
        req_data = request.get_json()
        delete = req_data['delete']
        collection.delete_one(delete)

        d = {"status": 200}
        return json.dumps(d)
    except KeyError as e:
        logger.error("cannot delete without using delete clause")
        d = "cannot delete without using delete clause"
        return json.dumps({"message": d})

    except Exception as e:
        logger.error(f"Server faced an unknown problem:{e}")
        d = f"Server faced an unknown problem:{e}"
        return json.dumps({"message": d})


@app.route('/view', methods=["GET"])
def find_all():
    try:
        query = collection.find()
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i += 1
        return jsonify(output)
    except Exception as e:
        logger.error(f"error in finding all: {e}")

@app.route('/find_one',methods=['POST'])
def find_one():
    try:
        id_1 = (collection.find({"name": request.get_json()['name']}))[0]
        logger.debug(id_1)
        id_1.pop('_id')
        print(id_1)
        return json.dumps(id_1)
    except Exception as e:
        logger.error(f"error in finding all: {e}")



if __name__ == "__main__":
    app.run(debug = True,  port=5001)
