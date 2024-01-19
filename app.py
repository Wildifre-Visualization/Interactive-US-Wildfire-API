from flask import Flask
from pymongo import MongoClient
import json
from flask import jsonify
from flask import render_template

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wildfires']
collection1 = db['1992-1999']
collection2 = db['2000-2007']
collection3 = db['2008-2015']


# def load_data():
#     file_path = './Resources/wildfires_1992_1999.geojson'
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#         # Check if data is already loaded in the database to avoid duplicate entries
#         if collection1.count_documents({}) == 0:
#             if isinstance(data, list):  # Check if data is a list of records
#                 collection1.insert_many(data)  # Use insert_many for list
#             else:
#                 # Use insert_one for a single record
#                 collection1.insert_one(data)
#         else:
#             print("Data already loaded in the database.")
#     return
file_paths = [
    './Resources/wildfires_1992_1999.geojson',
    './Resources/wildfires_2000_2007.geojson',
    './Resources/wildfires_2008_2015.geojson'
]

collections = [collection1, collection2, collection3]

def load_data(file_paths, collections):
    for file_path, collection in zip(file_paths, collections):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Check if data is already loaded in the database to avoid duplicate entries
            if collection.count_documents({}) == 0:
                if isinstance(data, list):  # Check if data is a list of records
                    collection.insert_many(data)  # Use insert_many for list
                else:
                    # Use insert_one for a single record
                    collection.insert_one(data)
                print(f"Data loaded into collection {collection.name}.")
            else:
                print(f"Data already loaded in the collection {collection.name}.")
file_paths = [
    './Resources/wildfires_1992_1999.geojson',
    './Resources/wildfires_2000_2007.geojson',
    './Resources/wildfires_2008_2015.geojson'
]

collections = [collection1, collection2, collection3]

load_data(file_paths, collections)

def get_wildfires_data(collection, limit):
    # Retrieve data from MongoDB
    data_cursor = collection.find().limit(limit)

    # Convert cursor to list
    data_list = list(data_cursor)

    # Convert ObjectId to string, because MongoDB uses ObjectId type and JSON does not support it
    for document in data_list:
        document['_id'] = str(document['_id'])

    return jsonify(data_list)

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1/wildfires/1992-1999'>/api/v1/wildfires/1992-1999</a> - List wildfires JSON data, loaded in a MongoDB server. First 5 results.<br/>"
        f"<a href='/api/v1/wildfires/2000-2007'>/api/v1/wildfires/2000-2007</a> - List wildfires JSON data, loaded in a MongoDB server. First 5 results.<br/>"
        f"<a href='/api/v1/wildfires/2008-2015'>/api/v1/wildfires/2008-2015</a> - List wildfires JSON data, loaded in a MongoDB server. First 5 results.<br/>"
        f"<a href='/api/v1/mapbox'>/api/v1/mapbox</a><br>"
    )
    
# @app.route('/api/v1/wildfires(1992-1999)')
@app.route('/api/v1/wildfires/1992-1999')
def wildfires_1992_1999():
    return get_wildfires_data(collection1, 5)

@app.route('/api/v1/wildfires/2000-2007')
def wildfires_2000_2007():
    return get_wildfires_data(collection2, 5)

@app.route('/api/v1/wildfires/2008-2015')
def wildfires_2008_2015():
    return get_wildfires_data(collection3, 5) 

@app.route('/api/v1/mapbox')
def show_html():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()