from copy import deepcopy
from itertools import chain
import math
import numpy as np


# takes inout from user
def num_input(msg):
    tnode = []
    print(msg)
    for i in range(3):
        temp = input().split()
        tnode += [temp]
    for i in tnode:
        if len(i) != 3:
            print('Invalid Input')
            exit()
    if len(tnode) == 3:
        tnode = list(chain.from_iterable(tnode))
        tnode = list(map(int, tnode))
        tnode.append(0)
        tnode.append('P')
        return tnode
    else:
        print('Invalid Input')
        exit()


# finds and returns the 0 position in the list
def zero_pos(n):
    pos = 0
    # list slicing not required as first occurred '0' is the null position
    for i in n:
        if i == 0:
            return pos
        pos += 1


# moves the blank tile up and returns a new node
def move_up(n, pos):
    n1 = deepcopy(n)
    if pos > 2:
        # array indexed from 0
        n1[pos] = n1[pos - 3]
        n1[pos - 3] = 0
        n1[9] += 1
        n1[10] = 'U'
    return n1


def move_left(n, pos):
    n2 = deepcopy(n)
    if pos != 0 and pos != 3 and pos != 6:
        n2[pos] = n2[pos - 1]
        n2[pos - 1] = 0
        n2[9] += 1
        n2[10] = 'L'
    return n2


def move_right(n, pos):
    n3 = deepcopy(n)
    if pos != 2 and pos != 5 and pos != 8:
        n3[pos] = n3[pos + 1]
        n3[pos + 1] = 0
        n3[9] += 1
        n3[10] = 'R'
    return n3


def move_down(n, pos):
    n4 = deepcopy(n)
    if pos < 6:
        n4[pos] = n4[pos + 3]
        n4[pos + 3] = 0
        n4[9] += 1
        n4[10] = 'D'
    return n4


# find the predecessor node for the given node
def predecessor(np):
    zp = zero_pos(np)
    if np[-1] == 'U':
        np = move_down(np, zp)
        np[-2] -= 2

    elif np[-1] == 'L':
        np = move_right(np, zp)
        np[-2] -= 2

    elif np[-1] == 'R':
        np = move_left(np, zp)
        np[-2] -= 2

    elif np[-1] == 'D':
        np = move_up(np, zp)
        np[-2] -= 2
    return np


def config_exits(chk):
    # exclusive for DFS to check if the node is already in parent list
    global parent
    for node in parent:
        if chk[:9] == node[:9]:
            return True
    return False


# Finds all successors nodes for a given node
def successor(n):
    p = zero_pos(n)
    a1 = move_up(n, p)
    a2 = move_left(n, p)
    a3 = move_right(n, p)
    a4 = move_down(n, p)
    a = []
    global inp_choice
    if inp_choice == 1 or inp_choice == 3:
        ap = predecessor(n)
        if a1[:9] != n[:9] and a1[:9] != ap[:9]:
            a.append(a1)
        if a2[:9] != n[:9] and a2[:9] != ap[:9]:
            a.append(a2)
        if a3[:9] != n[:9] and a3[:9] != ap[:9]:
            a.append(a3)
        if a4[:9] != n[:9] and a4[:9] != ap[:9]:
            a.append(a4)
    elif inp_choice == 2:
        if not config_exits(a1):
            a.append(a1)
        if not config_exits(a2):
            a.append(a2)
        if not config_exits(a3):
            a.append(a3)
        if not config_exits(a4):
            a.append(a4)

    return a


# Checks if the initial state is solvable
def solvability(inp):
    l = len(inp[:-2])
    n = abs(math.sqrt(l))
    count = 0
    for i in range(l):
        for j in range(i + 1, l):
            if inp[j] < inp[i] != 0 and inp[j] != 0:
                count += 1
    if n % 2 == 0:
        # solvable if sum of inversions and row no. of blank space starting from 0 is odd

        zp = zero_pos(inp)
        rw = (zp + 1) // n
        if (rw + count) % 2 != 0:
            return True
        return False
    else:
        # solvable if no of inversions is an even number
        if count % 2 == 0:
            return True
        return False


# Generates the final path after finding the solution
def generate_path(parent):
    print('Generating Path')
    index = 0
    path = []
    a = []
    nds = []
    for node in parent:
        if node[:9] != [1, 2, 3, 4, 5, 6, 7, 8, 0]:
            # if node[:9] != [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            index += 1
        else:
            break
    k = deepcopy(index)
    d = parent[index][-2]
    rev_search = deepcopy(parent[index])
    while d != 0:
        nds.append(rev_search[:9])
        index = 0
        if rev_search[-1] == 'U':
            path.append('U')

        elif rev_search[-1] == 'L':
            path.append('L')

        elif rev_search[-1] == 'R':
            path.append('R')

        elif rev_search[-1] == 'D':
            path.append('D')

        a = predecessor(rev_search)

        for node in parent:
            if node[:10] != a[:10]:
                index += 1
            else:
                rev_search = deepcopy(parent[index])
                d -= 1
                break
    nds.append(parent[0][:9])
    nds.reverse()
    del nds[-1]
    path.reverse()
    nds = np.array(nds).reshape(-1, 3, 3)
    for i in nds:
        for j in i:
            print(j)
        print("  | ")
        print("  | ")
        print(" \\\'/ \n")
    end = parent[k][:9]
    end = np.array(end).reshape(3, 3)
    for i in end:
        print(i)
    print('\nOptimal Path:')
    print(path)


# Breadth First Search Algorithm
def bfs(node_list):
    new_nodes = []
    global parent

    for node in node_list:
        if node[:9] == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
            print('Solution Found!')
            print('Total Nodes: ', len(parent))
            generate_path(parent)
            exit()
    # loop to calculate all child nodes of current nodes
    for node in node_list:
        new_nodes += successor(node)
        parent += new_nodes

    if new_nodes is not None:
        bfs(new_nodes)
    else:
        print('Solution could not be found')


# Depth First Search Algorithm
def dfs(node):
    global parent
    if node[:9] == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        # if node[:9] == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        return True
    new_nodes = successor(node)
    parent += new_nodes
    while new_nodes:
        if dfs(new_nodes[0]):
            print('Solution Found!')
            print('Total Nodes: ', len(parent))
            generate_path(parent)
            exit()
        new_nodes = new_nodes[1:]
    return False


# Iterative Depth First Search Algorithm
def dfsb(node, depth, limit):
    global parent
    if node[:9] == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        # if node[:9] == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        return True

    new_nodes = successor(node)
    for each_node in new_nodes:
        if not config_exits(each_node):
            parent.append(each_node)
    while new_nodes and depth < limit:
        if dfsb(new_nodes[0], depth + 1, limit):
            print('Solution Found!')
            print('Total Nodes: ', len(parent))
            generate_path(parent)
            exit()
        new_nodes = new_nodes[1:]
    return False


def idfs(node):
    depth_limit = 0
    global res
    while not res:
        print('Checking at depth Limit:', depth_limit)
        res = dfsb(node, 0, depth_limit)
        depth_limit += 1


if __name__ == '__main__':
    inp_choice = input("Enter your search method\n1 for BFS\n2 for DFS\n3 for IDFS\n4 to exit\n")
    inp_choice = int(inp_choice)
    if inp_choice != 4:
        all_nodes = [num_input("Enter the numbers row wise with 0 as blank position\n")]
        parent = deepcopy(all_nodes)
        if solvability(parent[0]):
            if inp_choice == 1:
                print('Solving with BFS')
                bfs(all_nodes)
            elif inp_choice == 2:
                print('Solving with DFS')
                dfs(all_nodes[0])
            else:
                print('Solving with IDFS')
                res = False

                idfs(all_nodes[0])
        else:
            print('Solution doesnt exist for the given configuration\n')
    else:
        exit()
