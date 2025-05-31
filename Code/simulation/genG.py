# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 23:15:23 2024

@author: jyzhang
"""

import numpy as np
import os
import random
import networkx as nx
import pickle
import re


def generate_spatial_lattice_periodic(m, n, k):
    if k not in [2, 4, 6, 8, 10]:
        raise ValueError("Connectivity k must be one of [2, 4, 6, 8, 10]")

    G = nx.Graph()

    for x in range(m):
        for y in range(n):
            G.add_node((x, y))

    for x in range(m):
        for y in range(n):
            G.add_edge((x, y), ((x + 1) % m, y))

    if k >= 4:
        for x in range(m):
            for y in range(n):
                G.add_edge((x, y), (x, (y + 1) % n))

    if k == 6:
        for x in range(m):
            for y in range(n):
                G.add_edge((x, y), ((x + 1) % m, (y + 1) % n))
                    
    if k >= 8:
        for x in range(m):
            for y in range(n):
                G.add_edge((x, y), ((x + 1) % m, (y + 1) % n))
                G.add_edge((x, y), ((x + 1) % m, (y - 1 + n) % n))        

    if k == 10:
        for x in range(m):
            for y in range(n):
                G.add_edge((x, y), ((x + 2) % m, (y + 1) % n))

    # Convert to scalar indexing
    H = nx.Graph()
    for x in range(m):
        for y in range(n):
            i_node = x * n + y
            H.add_node(i_node)

    for (x1, y1), (x2, y2) in G.edges():
        i_node1 = x1 * n + y1
        i_node2 = x2 * n + y2
        H.add_edge(i_node1, i_node2)

    return H


def gen_G(N, z, networkType):
    # regular ring graph
    if networkType == 'rg':
        p = 0
        G = nx.watts_strogatz_graph(N, z, p)
    
    # small-world network
    elif re.fullmatch(r'sw\d+(\.\d+)?', networkType):
        p = float(networkType.split("sw")[1])
        G = nx.watts_strogatz_graph(N, z, p)    
    
    # newman_watts_strogatz small-world network
    elif re.fullmatch(r'nws\d+(\.\d+)?', networkType):
        p = float(networkType.split("nws")[1])
        G = nx.newman_watts_strogatz_graph(N, z, p)    
    
    elif networkType == 'rd':
        # Probability of creating an edge to achieve average degree z
        p = z / (N-1)
        # Generate a random graph
        G = nx.erdos_renyi_graph(N, p)
        
        # Connect isolated nodes
        def connect_isolated_nodes(G):
            isolated_nodes = list(nx.isolates(G))
            while isolated_nodes:
                node = isolated_nodes.pop()
                # Choose a random node to connect to
                other_node = random.choice(list(G.nodes))
                while other_node == node or G.has_edge(node, other_node):
                    other_node = random.choice(list(G.nodes))
                G.add_edge(node, other_node)
                # Update the list of isolated nodes
                isolated_nodes = list(nx.isolates(G))

        # Connect any isolated nodes in the graph
        connect_isolated_nodes(G)
        
        
    elif networkType == 'rr':
        G = nx.random_regular_graph(z, N)
        
        mapping = dict(zip(G.nodes(), sorted(G.nodes())))
        G = nx.relabel_nodes(G, mapping)
        
        
    elif networkType == 'sf':
        m = int(z/2)
        G = nx.barabasi_albert_graph(N, m)
    
    elif networkType == 'lt':
        if 0: pass
        elif N == 100: m, n = 10, 10 
        elif N == 200: m, n = 20, 10 
        elif N == 400: m, n = 20, 20 
        elif N == 500: m, n = 25, 20 
        elif N == 512: m, n = 32, 16
        elif N == 1000: m, n = 40, 25 
        elif N == 10000: m, n = 100, 100 
        else:
            raise Exception()
        # G = nx.grid_2d_graph(m, n, periodic=False)
        G = generate_spatial_lattice_periodic(m, n, z)
        
        # Relabel nodes with integer indices
        mapping = {node: i for i, node in enumerate(G.nodes())}
        G = nx.relabel_nodes(G, mapping)
    
    if networkType == 'kc':
        G = nx.karate_club_graph()
        
    return G

