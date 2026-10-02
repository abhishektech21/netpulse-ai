import networkx as nx

from network.topology import create_network


def get_neighbors(graph, device):

    if device not in graph:
        return []

    return list(graph.neighbors(device))


def get_connected_interfaces(graph, device):

    interfaces = []

    if device not in graph:
        return interfaces

    for neighbor in graph.neighbors(device):

        edge_data = graph.get_edge_data(
            device,
            neighbor
        )

        interfaces.append({
            "neighbor": neighbor,
            "interface": edge_data.get(
                "interface",
                "unknown"
            )
        })

    return interfaces


def find_affected_paths(graph, device):

    affected_paths = []

    for target in graph.nodes:

        if target == device:
            continue

        try:

            path = nx.shortest_path(
                graph,
                source=device,
                target=target
            )

            affected_paths.append({
                "target": target,
                "path": path
            })

        except nx.NetworkXNoPath:

            pass

    return affected_paths


if __name__ == "__main__":

    graph = create_network()

    device = "SW2"

    print("\nDevice:")
    print(device)

    print("\nNeighbors:")
    print(
        get_neighbors(
            graph,
            device
        )
    )

    print("\nConnected interfaces:")

    for item in get_connected_interfaces(
        graph,
        device
    ):

        print(item)

    print("\nAffected paths:")

    for path in find_affected_paths(
        graph,
        device
    ):

        print(path)