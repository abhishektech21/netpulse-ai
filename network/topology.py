import networkx as nx
import matplotlib.pyplot as plt


def create_network():

    G = nx.Graph()

    # Devices
    devices = {
        "R1": "router",
        "SW1": "switch",
        "SW2": "switch",
        "H1": "host",
        "H2": "host",
        "H3": "host",
        "H4": "host"
    }

    for device, device_type in devices.items():
        G.add_node(device, type=device_type)

    # Links
    G.add_edge("R1", "SW1", interface="Gi0/1")
    G.add_edge("R1", "SW2", interface="Gi0/2")

    G.add_edge("SW1", "H1", interface="Gi0/10")
    G.add_edge("SW1", "H2", interface="Gi0/11")

    G.add_edge("SW2", "H3", interface="Gi0/10")
    G.add_edge("SW2", "H4", interface="Gi0/11")

    return G


def display_network(G):

    position = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        position,
        with_labels=True,
        node_size=2500,
        font_size=12
    )

    edge_labels = nx.get_edge_attributes(G, "interface")

    nx.draw_networkx_edge_labels(
        G,
        position,
        edge_labels=edge_labels
    )

    plt.title("NetPulse AI - Network Topology")
    plt.show()


if __name__ == "__main__":

    network = create_network()

    print("Devices:")
    print(network.nodes(data=True))

    print("\nLinks:")
    print(network.edges(data=True))

    display_network(network)