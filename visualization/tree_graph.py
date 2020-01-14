import os
import json
import graphviz as gv


def trace_path(start):
    """ Build dict representing directory tree from start """
    count = 0
    layout = {}

    for root, dirs, files in os.walk(start):
        current_dict = layout
        path = root.split('/')
        if path[-1] == '':
            path.pop()
        if path[-1][0] == '.':
            print('hidden')
            # time.sleep(10)
            continue
        for folder in path:
            if folder == '':
                continue
            if folder not in current_dict:
                current_dict[folder] = {}

            current_dict = current_dict[folder]
        for di in dirs:
            if not di[0] == '.':
                current_dict[di] = {}
        for fi in files:
            if not fi[0] == '.':
                current_dict[fi] = None
        count += 1

    return layout


def write_to_file(file_name, data):
    """ Write json data to file name """
    with open(file_name, 'w') as fp:
        json.dump(data, fp)


def load_from_file(file_name):
    """ Read from a json formatted file and return dict """
    with open(file_name, 'r') as fp:
        return json.load(fp)


def visualize(data, out_file):
    """ Create a render for a graph given a dict """
    g = gv.Graph()
    queue = ['Users']
    visited = set('Users')
    g.node('Users')
    prev = {'Users': None}
    while queue:
        node = queue.pop()
        if node[0] == '.':
            print('hidden')
            continue
        for neighbor in traverse_to_dict(data, get_path(prev, node)):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                prev[neighbor] = node
                if check_encode(neighbor):
                    print(node)
                    g.node(neighbor)
                    g.edge(node, neighbor)

    g.save(out_file)
    os.system('dot -Tsvg -Ksfdp {0} > {1}'.format(out_file, out_file + '.svg'))
    os.system('rm {0}'.format(out_file))


def get_path(prev, node):
    """ Get the path from the root to the current node """
    current = node
    path = [current]
    while current:
        path.append(prev[current])
        current = prev[current]

    path.pop()

    return path[::-1]


def traverse_to_dict(data, path):
    """ Given a path return the proper dict """
    current_dict = data
    for node in path:
        if current_dict[node] is None:
            return current_dict
        current_dict = current_dict[node]

    return current_dict


def check_encode(to_check):
    """  Check to make sure we can utf encode """
    try:
        to_check.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


def render_tree(path):
    default_file = 'graph.json'

    structure = trace_path(os.path.expanduser(path))
    write_to_file(default_file, structure)

    data = load_from_file(default_file)

    out_file = "dir_tree"
    visualize(data, out_file)
