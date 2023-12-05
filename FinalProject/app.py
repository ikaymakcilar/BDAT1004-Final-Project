from bson import ObjectId
from flask import Flask, jsonify, render_template
from pymongo import MongoClient
import json
from api import api_bp

client = MongoClient("mongodb+srv://bdat1004:bdat1004@cluster0.wzablab.mongodb.net/?retryWrites=true&w=majority")
db = client['bitcoinData']
collection = db['bitcoinHistoricalData']

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data')
def data():
    # Fetch all documents from the collection
    data = list(collection.find())
    data.reverse()
    # Pass the data to the template
    return render_template('data.html', data=data)

@app.route('/dashboard')
def dashboard():
    # Fetch all documents from the collection
    data_from_mongodb = list(collection.find())
    data_from_mongodb.reverse()

    # Format data for JavaScript
    chartData = []
    for entry in data_from_mongodb:
        # Assuming 'date' is a field in your MongoDB document
        date = entry['date']
        # Assuming 'price' is a field in your MongoDB document
        price = entry['price']
        
        formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')# Format the data and add it to chartData
        #formatted_date = date.strftime('%Y-%m-%d')  # Format date as 'Y-m-d'
        chartData.append([formatted_date, price])  # Convert date to string and keep price as-is

    # Convert chartData to a JSON string
    chartData_json = json.dumps(chartData)

    # Pass the data to the template
    return render_template('dashboard.html', chartData_json=chartData_json)

@app.route('/api-documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
