from pymongo import MongoClient


def create_graph(node_list, edge_list):
    graph_dict = {
        "directed": False,
        "multigraph": False,
        "graph": dict(),
        "nodes": node_list,
        "links": edge_list
    }
    return graph_dict


client = MongoClient()
db = client.graphs

graphs_names = ['complete', 'reduced']
graphs_dict = dict()

for name in graphs_names:
    if name == 'complete':
        _complete_nodes = db.complete_graph_nodes.find({}, {'_id': False})
        _complete_edges = db.complete_graph_edges.find({}, {'_id': False})
    else:
        _complete_nodes = db.reduced_graph_nodes.find({}, {'_id': False})
        _complete_edges = db.reduced_graph_edges.find({}, {'_id': False})

    complete_nodes = [item for item in _complete_nodes]
    complete_edges = [item for item in _complete_edges]

    graph = create_graph(complete_nodes, complete_edges)
    graphs_dict[name] = graph


print(graphs_dict)
