import gzip
import shutil
from typing import List, Set


class SCCComputer:
    def __init__(self, graph: dict):
        self.__graph = graph
        self.__graph_rev = {}  # same graph with edge reversed
        self.__graph_explored = set()  # node explored
        self.__graph_rev_explored = set()
        self.__finish_nodes = set()    # nodes have been set finish time on first pass
        self.__t = 0         # finish time
        self.__f_rev = {}    # f_rev[t] = i  means node i's finish time is t
        self.__node_set = set()  # all nodes

        # fill in reverse graph
        for from_node in graph:
            for to_node in graph[from_node]:
                if to_node not in self.__graph_rev:
                    self.__graph_rev[to_node] = {}
                if from_node not in self.__graph_rev:
                    self.__graph_rev[from_node] = {}
                self.__graph_rev[to_node][from_node] = graph[from_node][to_node]
                self.__node_set.add(to_node)
                self.__node_set.add(from_node)

    def compute_scc(self)->List[Set]:
        """
        compute SCC on given graph
        :return: List of SCC
        """
        self.__dfs_loop_rev()
        return self.__dfs_loop()

    def __dfs_loop(self) -> List[Set]:
        scc_list = []
        for i in range(self.__t, 0, -1):
            if self.__f_rev[i] not in self.__graph_explored:

                scc_list.append(self.__dfs(self.__f_rev[i]))
        return scc_list

    def __dfs(self, i) -> Set:
        """
        DFS visit on self.__graph, non-recursive version
        :param i: start node
        :return: SCC nodes
        """
        node_stack = []
        scc = set()
        if i in self.__graph:
            node_stack.append(i)
            while bool(node_stack):
                current_node = node_stack.pop()
                if current_node not in self.__graph_explored:
                    self.__graph_explored.add(current_node)
                    scc.add(current_node)
                    for n in self.__graph[current_node]:
                        if n not in self.__graph_explored:
                            node_stack.append(n)
        return scc

    def __dfs_loop_rev(self):
        for i in self.__node_set:
            if i in self.__graph_rev_explored:
                continue
            else:
                self.__dfs_rev(i)

    def __dfs_rev(self, i: int):
        """
        DFS visit on self.__graph_rev, non-recursive version
        :param i: start node
        :return:
        """
        node_stack = []
        if i in self.__graph_rev:
            node_stack.append(i)
            while bool(node_stack):
                current_node = node_stack[-1]
                self.__graph_rev_explored.add(current_node)
                next_node = None
                for n in self.__graph_rev[current_node]:
                    if n in self.__graph_rev_explored:
                        continue
                    node_stack.append(n)
                    next_node = n
                if next_node is None:
                    node_stack.pop()
                    if current_node not in self.__finish_nodes:
                        self.__t += 1
                        self.__f_rev[self.__t] = current_node
                        self.__finish_nodes.add(current_node)


def two_sat(file_name: str)->bool:
    # decompress file
    with gzip.open(file_name, 'rb') as read, open(file_name[:-3], 'wb') as write:
        shutil.copyfileobj(read, write)

    with open(file_name[:-3], 'r') as file:
        meta_line = file.readline().split()
        bit_num = int(meta_line[0])
        graph = {}
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                line = line.split()
                a = int(line[0])
                b = int(line[1])
                if a not in graph:
                    graph[a] = {}
                if b not in graph:
                    graph[b] = {}
                if -a not in graph:
                    graph[-a] = {}
                if -b not in graph:
                    graph[-b] = {}
                graph[-a][b] = True
                graph[-b][a] = True
        computer = SCCComputer(graph=graph)
        sccs = computer.compute_scc()
        for scc in sccs:
            for node in scc:
                if -node in scc:
                    return False
    return True


def main():
    """
    use SCC to compute 2sat problem
    :return:
    """
    res_list = [two_sat('2sat1.txt.gz'), two_sat('2sat2.txt.gz'), two_sat('2sat3.txt.gz'),
                two_sat('2sat4.txt.gz'), two_sat('2sat5.txt.gz'), two_sat('2sat6.txt.gz')]
    print(''.join(map(lambda x: str(int(x)), res_list)))


if __name__ == "__main__":
    main()
