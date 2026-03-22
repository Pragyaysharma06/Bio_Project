import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def generate_graph_image(disease, gene, proteins, drugs):
    G = nx.Graph()

    G.add_node(disease)
    G.add_node(gene)
    G.add_edge(disease, gene)

    for p in proteins[:3]:
        G.add_node(p)
        G.add_edge(gene, p)

    for d in drugs[:3]:
        drug_name = d["name"] if isinstance(d, dict) else d

        G.add_node(drug_name)
        G.add_edge(proteins[0], drug_name)

    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(G, k=0.8)

    nx.draw(
    G, pos,
    with_labels=True,
    node_color='lightblue',
    node_size=2500,
    font_size=8,
    font_weight='bold'
)

    plt.title("Disease → Gene → Protein → Drug")

    # save image
    plt.savefig("static/graph.png")
    plt.close()