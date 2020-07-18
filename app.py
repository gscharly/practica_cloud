import os
from flask import Flask, render_template, Response, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to Mongo
client = MongoClient()
db = client.graphs


def create_graph(node_cursor, edge_cursor):
    nodes = [item for item in node_cursor]
    edges = [item for item in edge_cursor]
    graph_dict = {
        "directed": False,
        "multigraph": False,
        "graph": dict(),
        "nodes": nodes,
        "links": edges
    }
    return graph_dict


@app.route('/')
def todo():
    return render_template('graphs_cloud.html')


@app.route('/completeGraph')
def complete_graph():
    _complete_nodes = db.complete_graph_nodes.find({}, {'_id': False})
    _complete_edges = db.complete_graph_edges.find({}, {'_id': False})
    graph = create_graph(_complete_nodes, _complete_edges)
    return jsonify(graph)


@app.route('/reducedGraph')
def reduced_graph():
    _reduced_nodes = db.reduced_graph_nodes.find({}, {'_id': False})
    _reduced_edges = db.reduced_graph_edges.find({}, {'_id': False})
    graph = create_graph(_reduced_nodes, _reduced_edges)
    return jsonify(graph)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)