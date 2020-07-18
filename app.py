import os
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to Mongo
client = MongoClient()
db = client.graphs


@app.route('/')
def todo():

    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('graphs_cloud.html', items=items)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)