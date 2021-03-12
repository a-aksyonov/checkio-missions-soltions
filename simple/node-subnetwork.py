from collections import defaultdict


def create_adjacency_matrix(connections):
    matrix = defaultdict(dict)
    for a, b in connections:
        matrix[a][b] = 1
        matrix[b][a] = 1
    return matrix


def is_connected_to_all(vertex, group, matrix):
    for v in group:
        if vertex != v and vertex not in matrix[v]:
            return False
    return True


def group_vertexes(input):
    matrix = create_adjacency_matrix(input)
    groups = []
    current_group = set()
    for vertex in matrix.keys():
        if is_connected_to_all(vertex, current_group, matrix):
            current_group.add(vertex)
        else:
            groups.append(current_group)
            current_group = {vertex}
    groups.append(current_group)
    return groups


def subnetworks(net, crushes):
    for broken in crushes:
        for conn in net:
            if broken in conn:
                conn.remove(broken)
    if [] in net:
        net.remove([])
    for conn in net:
        if len(conn) == 1:
            conn.append(conn[0])
    t_net = [(conn[0], conn[1]) for conn in net]
    return len(group_vertexes(t_net))


if __name__ == '__main__':
    # These "asserts" using only for self-checking
    # and not necessary for auto-testing
    assert subnetworks([
            ['A', 'B'],
            ['B', 'C'],
            ['C', 'D']
        ], ['B']) == 2, "First"
    assert subnetworks([
            ['A', 'B'],
            ['A', 'C'],
            ['A', 'D'],
            ['D', 'F']
        ], ['A']) == 3, "Second"
    assert subnetworks([
            ['A', 'B'],
            ['B', 'C'],
            ['C', 'D']
        ], ['C', 'D']) == 1, "Third"
    print('Done! Check button is waiting for you!')
