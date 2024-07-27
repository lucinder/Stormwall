import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random, math

stormwall_ids = {
    **{key : "Aldenia" for key in range(1,7)},
    **{key : "Cavern A" for key in range(7,9)},
    **{key : "Cavern B" for key in range(9,13)},
    **{key : "Cavern C" for key in range(13,15)},
    **{key : "Cavern E" for key in range(15,18)},
    **{key : "Cavern D" for key in range(18,20)},
    **{key : "Cavern G" for key in range(20,24)},
    **{key : "Cavern H" for key in range(24,27)},
    **{key : "Cavern F" for key in range(27,29)},
    **{key : "Cavern I" for key in range(29,31)},
    **{key : "Cavern J" for key in range(31,34)},
    **{key : "Starford Keep" for key in range(34,37)},
    **{key : "Elysium" for key in range(37,38)},
    **{key : "Calhas" for key in range(38,40)},
    **{key : "GGC" for key in range(40,44)},
    **{key : "Stormwall" for key in range(44,45)}
}
maxY = 50*70
stormwall_info = {
    "Stormwall" : {"pos":[25*70, maxY-0],"nTunnels":1,"minTunnel":44},
    "Elysium" : {"pos":[46*70, maxY-(9*70)],"nTunnels":1,"minTunnel":37},
    "Calhas" : {"pos":[0, maxY-(9*70)],"nTunnels":2,"minTunnel":38},
    "GGC" : {"pos":[0, maxY-(31*70)],"nTunnels":4,"minTunnel":40},
    "Aldenia" : {"pos":[24*70, maxY-(46*70)],"nTunnels":6,"minTunnel":1},
    "Starford Keep" : {"pos":[46*70, maxY-(31*70)],"nTunnels":3,"minTunnel":34},
    "Cavern A" : {"pos":[35*70, maxY-(38*70)],"nTunnels":2,"minTunnel":7},
    "Cavern B" : {"pos":[25*70, maxY-(36*70)],"nTunnels":4,"minTunnel":9},
    "Cavern C" : {"pos":[14*70, maxY-(33*70)],"nTunnels":2,"minTunnel":13},
    "Cavern D" : {"pos":[30*70, maxY-(30*70)],"nTunnels":2,"minTunnel":18},
    "Cavern E" : {"pos":[21*70, maxY-(26*70)],"nTunnels":3,"minTunnel":15},
    "Cavern F" : {"pos":[9*70, maxY-(20*70)],"nTunnels":2,"minTunnel":27},
    "Cavern G" : {"pos":[32*70, maxY-(23*70)],"nTunnels":4,"minTunnel":20},
    "Cavern H" : {"pos":[22*70, maxY-(16*70)],"nTunnels":3,"minTunnel":24},
    "Cavern I" : {"pos":[33*70, maxY-(12*70)],"nTunnels":2,"minTunnel":29},
    "Cavern J" : {"pos":[15*70, maxY-(7*70)],"nTunnels":3,"minTunnel":31}
}

def generate_matching_graph(num_vertices):
    if num_vertices % 2 != 0:
        raise ValueError("Number of vertices must be even for a perfect matching.")

    # Create an empty graph
    G = nx.Graph()

    # Generate and shuffle vertex IDs
    vertices = list(range(1,num_vertices+1))
    random.shuffle(vertices)
    
    # Add vertices
    G.add_nodes_from(vertices)

    # Add edges with random weights
    pairs = []
    for i in range(0, num_vertices, 2):
        v1, v2 = vertices[i], vertices[i + 1]
        log_divider = 3.5
        weight = np.random.lognormal(mean=np.log(0.5 + (168*log_divider))/2, sigma=0.7)/log_divider
        weight = min(max(weight, 0.5), 168)  # Ensure weight is within the desired range
        weight = round(weight) if weight > 1 else round(weight,2)
        G.add_edge(v1, v2, weight=weight)
        pairs.append((v1, v2, weight))
    
    return G, pairs

def draw_graph(G):
    plt.figure(figsize=(50,50),dpi=70)
    positions = []
    count = 0
    offset_length = 50
    for i in list(G.nodes):
        # print(f"Test: looking for cavern with {i}")
        cavern = stormwall_ids[i] # get connecting cavern
        if cavern in stormwall_info:
            # print("Test: cavern found")
            cave = stormwall_info[cavern]
            basePos,nTunnels,minTunnel = cave["pos"],cave["nTunnels"],cave["minTunnel"]
            rot = 2.0*math.pi*((i-minTunnel)/float(nTunnels))
            x_offset = offset_length * math.cos(rot)
            y_offset = offset_length * math.sin(rot)
            pos = [basePos[0] + x_offset, basePos[1] + y_offset]
            positions.append(pos)
        # print(f"{i}: {cavern} at {positions[count]}")
        count += 1
    # print(f"Positions length: {len(positions)}\nG length:{len(list(G.nodes))}")
    pos = {list(G.nodes)[i] : positions[i] for i in range(len(positions))}
    # print(pos)
    edges = list(G.edges)
    weights = nx.get_edge_attributes(G, 'weight')
    # print(edges)
    '''
    edge_labels = {}
    for u, v in G.edges():
        edge_labels[(u, v)] = f"{u} <-> {v} ({weights.get((u, v), 'N/A')} hrs.)"
    '''
    edge_labels = weights # replace old labeling since it doesn't work
    colors = []
    color_min = 80
    color_max = 255
    for i in range(len(G.edges)):
        color = "#{:02x}{:02x}{:02x}".format(random.randint(color_min, color_max), random.randint(color_min, color_max), random.randint(color_min, color_max))
        colors.append(color)
    # print(f"Color array length: {len(colors)}\nEdges array length: {nx.number_of_edges(G)}")
    
    nx.draw(G, pos, with_labels=True, node_color='blue', node_size=50, font_color='white',font_size=24)
    nx.draw_networkx_edges(G,pos,edge_color=colors,width=5)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red',font_size=22)
    plt.title('Matching Graph')
    plt.savefig("stormwall_map.png",transparent=True)

if __name__ == "__main__":
    num_vertices = 44
    
    # Generate the matching graph
    try:
        G, pairs = generate_matching_graph(num_vertices)
        # Print the pairs and weights
        txt = "Pairs and weights:\n"
        for v1, v2, weight in pairs:
            txt += f"{v1} ({stormwall_ids[v1]}) - {v2} ({stormwall_ids[v2]}) with travel time {weight} hrs.\n"
        # Draw the graph
        connections = open("stormwall_connections.txt",'w')
        connections.write(txt)
        connections.close()
        draw_graph(G)
    except ValueError as e:
        print(e)
