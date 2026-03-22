import networkx as nx
import matplotlib.pyplot as plt

def generate_graph_image(disease, gene, proteins, drugs):
    G = nx.Graph()

    G.add_node(disease)
    G.add_node(gene)
    G.add_edge(disease, gene)

    for p in proteins[:3]:
        G.add_node(p)
        G.add_edge(gene, p)

    for d in drugs[:3]:
        G.add_node(d)
        G.add_edge(proteins[0], d)

    plt.figure(figsize=(8,6))
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=2000, font_size=8)

    plt.title("Disease → Gene → Protein → Drug")

    # save image
    plt.savefig("static/graph.png")
    plt.close()