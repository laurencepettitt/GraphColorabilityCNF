import sys
import itertools

vertices = []
edges = []


def read_graph(filename):
    with open(filename) as f:
        vert_num = -1
        edg_num = -1
        for line in f.readlines():
            if line.startswith('c '):  # ignore comments
                continue
            if line.startswith('e '):  # add an edge, check vertex number are consistent
                parts = line.split(' ')
                u, v = int(parts[1]), int(parts[2])
                if u > vert_num or v > vert_num:
                    print('Warning: invalid vertex number found in edge:', line)
                edges.append((u, v))

            if line.startswith('p edge'):  # parse problem specification
                parts = line.split(' ')
                vert_num = int(parts[2])
                edg_num = int(parts[3])
                vertices = list(range(1, vert_num + 1))

        if edg_num != len(edges):
            print('Warning: number of edges does not match file header: %d != %d' % (
                len(edges), edg_num))

    return vertices, edges


def write_cnf(cnf, filename):

    # find the maximum number of a variable used
    variables = max(map(abs, itertools.chain(*cnf)))
    # concatenate clauses into a string
    cnf_str = '\n'.join(map(lambda c: ' '.join(map(str, c)) + ' 0', cnf))

    print('CNF created, it has %d variables and %d clauses' %
          (variables, len(cnf)))

    with open(filename, 'w') as f:
        # write basic CNF information
        f.write('p cnf %d %d\n' % (variables, len(cnf)))
        f.write(cnf_str)

def generate_cnf(vertices, edges, k):
    clauses = []

    def p(i, j):
        return i*k + j + 1

    clauses += [[p(i, j) for j in range(k)] for i in range(len(vertices))]

    for i in range(len(vertices)):
        for c in range(k - 1):
                for d in range(c+1, k):
                    clauses += [[-p(i, c), -p(i, d)]]

    for i,j in edges:
        u = int(i) - 1
        v = int(j) - 1
        for c  in range(k):
            clauses += [[-p(u, c), -p(v, c)]]

    return clauses


if __name__ == '__main__':
    k = int(sys.argv[2])
    vertices, edges = read_graph(sys.argv[1])

    print('Number of vertices:', len(vertices))
    print('Number of edges:', len(edges))

    cnf = generate_cnf(vertices, edges, k)

    write_cnf(cnf, sys.argv[1] + '-' + str(k) + '-col.cnf')
