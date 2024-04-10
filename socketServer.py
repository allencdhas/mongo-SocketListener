import os
import sys
import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient, errors
from bson.json_util import dumps

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# MongoDB configuration
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.othvgus.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DB_NAME = 'mydatabase'
COLLECTION_NAME = 'mycollection'

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection on a request as the connect=True parameter of MongoClient seems to be useless here
except errors.PyMongoError as e:
    print("Could not connect to MongoDB: %s" % e)
    sys.exit()

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    try:
        # Send existing data to the client when it connects
        existing_data = [doc for doc in collection.find()]
        emit('initial_data', dumps(existing_data))  # Use dumps to serialize the data
    except Exception as e:
        print("Error sending initial data:", e)

def listen_to_db():
    while True:
        try:
            # Query MongoDB for new data
            new_data = [doc for doc in collection.find()]
            # Emit new data to connected clients
            socketio.emit('new_data', dumps(new_data))  # Use dumps to serialize the data
        except Exception as e:
            print("Error querying database:", e)
        time.sleep(1)

if __name__ == '__main__':
    # Start listening to MongoDB changes in a separate thread
    mongo_listener_thread = threading.Thread(target=listen_to_db)
    mongo_listener_thread.daemon = True
    mongo_listener_thread.start()

    # Start Flask application
    socketio.run(app, debug=True)
