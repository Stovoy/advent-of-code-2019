from advent import *

with open('input.txt') as input_file:
    lines = input_file.readlines()

nodes = defaultdict(lambda: set())
for line in lines:
    a, b = line.strip().split(")")
    nodes[a].add(b)
    nodes[b].add(a)


def bfs(nodes, start):
    queue = [(start, 0)]
    seen = set()
    for node, depth in queue:
        seen.add(node)
        next_nodes = nodes.get(node, [])
        queue += [(new_node, depth + 1) for new_node in next_nodes if new_node not in seen]
        yield node, depth


def total_connections(nodes, start):
    return sum(depth for node, depth in bfs(nodes, start))


def distance(nodes, start, end):
    return next(depth - 2 for node, depth in bfs(nodes, start) if node == end)


print(total_connections(nodes, 'COM'))
print(distance(nodes, 'YOU', 'SAN'))
