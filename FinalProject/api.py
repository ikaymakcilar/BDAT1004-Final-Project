from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

api_bp = Blueprint("api", __name__, url_prefix='/api')


# Create a MongoDB client and collection
client = MongoClient("mongodb+srv://bdat1004:bdat1004@cluster0.wzablab.mongodb.net/?retryWrites=true&w=majority")
db1 = client["bitcoinData"]
collection = db1["bitcoinHistoricalData"]

@api_bp.route('/items', methods=['GET'])
def get_all_items():
    # Retrieve a list of documents (items) from the MongoDB collection
    items = list(collection.find())

    # Convert ObjectId to string for each item in the list
    # This ensures that the '_id' field is serializable to JSON
    items = [{**item, '_id': str(item['_id'])} for item in items]

    # Return the list of items as a JSON response
    return jsonify(items)

@api_bp.route('/items/range', methods=['GET'])
def get_items_range():
    start = request.args.get('start')
    end = request.args.get('end')

    # Modify the start and end dates to match the format stored in MongoDB.
    start_date = f"{start}T00:00:00.000+00:00"
    end_date = f"{end}T23:59:59.999+00:00"

    # Convert start_date and end_date to datetime objects
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f%z")

    # Query MongoDB with the modified date format.
    items = list(collection.find({"date": {"$gte": start_date_obj, "$lte": end_date_obj}}))

    # Convert ObjectId fields to strings before returning JSON
    for item in items:
        item['_id'] = str(item['_id'])

    return jsonify(items)

@api_bp.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = collection.find_one({'_id': ObjectId(id)})

    if item:
        # Convert ObjectId to a string before returning it as JSON
        item['_id'] = str(item['_id'])

        return jsonify(item)
    else:
        return ('', 404)
# Close the MongoDB client when necessary
#@api_bp.teardown_request
#def teardown_db(exception):
#    client.close()
