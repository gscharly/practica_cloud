import networkx as nx
import pandas as pd
import networkx.algorithms.community as nxComm
from networkx.readwrite import json_graph
import json
import pymongo


def load_graph(edges_path, nodes_path):
    g = nx.Graph()
    edges0 = pd.read_csv(edges_path)
    list_edges = edges0.values.tolist()
    for row in list_edges:
        g.add_edge(row[0], row[1])

    # Añadir atributos
    nodes0 = pd.read_csv(nodes_path)
    list_nodes = nodes0[['new_id', 'name', 'country', 'country_id', 'chef']].values.tolist()
    for row in list_nodes:
        g.add_node(row[0], name=row[1], country=row[2], country_id=row[3], chef=row[4])
    return g


def get_communities(g):
    """
    Perform community detection algorithms over g
    :param g:
    :return:
    """
    comm_greedy = list(nxComm.greedy_modularity_communities(g))
    comm_label = list(nxComm.label_propagation_communities(g))
    comm_dict = {
        'greedy': comm_greedy,
        'label': comm_label
    }
    return comm_dict


def get_centrality_metrics(g):
    """
    Calculate centrality metrics over g
    :param g:
    :return:
    """
    degree = nx.degree_centrality(g)
    closeness = nx.closeness_centrality(g)
    betweenness = nx.betweenness_centrality(g)
    centrality_dict = {
        'degree': degree,
        'closeness': closeness,
        'betweenness': betweenness
    }
    return centrality_dict


def add_node_metrics_to_g(g, comm_dict, centrality_dict):
    """
    Adds communities and centrality measures to graph nodes.
    :param g:
    :param comm:
    :param centrality_dict:
    :return:
    """
    for community, comm_nodes in comm_dict.items():
        print(community)
        idComm = 1
        for c in comm_nodes:
            for node in c:
                g.nodes[node][community] = idComm
                for metric_name, metric in centrality_dict.items():
                    g.nodes[node][metric_name] = metric[node]
            idComm += 1
    return g


def add_edge_metrics_to_g(g, edge_betwenness):
    """
    Add edge metrics to graph. For now, only betweenness is added.
    :param g:
    :param edge_betwenness:
    :return:
    """
    for edge in edge_betwenness:
        g[edge[0]][edge[1]]['eb'] = edge_betwenness[edge]
    return g


def write_graph_json(g, json_file):
    json_data = json_graph.node_link_data(g)
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent='\t')


if __name__ == '__main__':
    base_path = 'data'
    json_path = 'json'
    ids = ['complete', 'reduced']

    for graph_id in ids:
        edges_path = '{}/{}.edges'.format(base_path, graph_id)
        nodes_path = '{}/{}_nodes.csv'.format(base_path, graph_id)
        g = load_graph(edges_path, nodes_path)

        # Calculate node metrics
        comm_dict = get_communities(g)
        centrality_dict = get_centrality_metrics(g)

        g = add_node_metrics_to_g(g, comm_dict, centrality_dict)

        # Calculate edge metrics
        edge_betwenness = nx.edge_betweenness(g)
        g = add_edge_metrics_to_g(g, edge_betwenness)

        # Connect to Mongo
        conex = pymongo.MongoClient()
        db = conex.graphs
        json_data = json_graph.node_link_data(g)

        # Write to Mongo
        nodes = json_data['nodes']
        for node in nodes:
            if graph_id == 'complete':
                db.complete_graph_nodes.insert_one(node)
            else:
                db.reduced_graph_nodes.insert_one(node)

        edges = json_data['links']
        for edge in edges:
            if graph_id == 'complete':
                db.complete_graph_edges.insert_one(edge)
            else:
                db.reduced_graph_edges.insert_one(edge)
