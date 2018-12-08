import fileinput

def parse(it):
    num_children, num_metadata = next(it), next(it)
    children = [parse(it) for _ in range(num_children)]
    metadata = [next(it) for _ in range(num_metadata)]
    return (metadata, children)

root = parse(map(int, next(fileinput.input()).split()))

# part 1
def sum_metadata(node):
    metadata, children = node
    return sum(metadata) + sum(sum_metadata(x) for x in children)

print(sum_metadata(root))

# part 2
def node_value(node):
    metadata, children = node
    if children:
        return sum(node_value(children[i-1]) for i in metadata
            if 1 <= i <= len(children))
    return sum(metadata)

print(node_value(root))
