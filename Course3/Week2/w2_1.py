import gzip
import shutil


class UnionFind:
    """
    Union Find implementation with rank union and path compression
    """
    class Node:
        """
        element in UnionFind
        """
        def __init__(self, pre_index: int):
            self.pre_index = pre_index
            self.rank = 0

    def __init__(self, size: int):
        """
        init UnionFind with given size. The index in self.__data means the node name or index. Node info give its pre.
        Hint: you can leave self.__data[0] alone
        :param size: size
        """
        self.__data = []
        for i in range(0, size):
            self.__data.append(self.Node(pre_index=i))

    def find(self, node_index: int)->int:
        """
        Find the leader node index of node self.__data[node_index]
        :param node_index:
        :return: leader node index
        """
        if node_index < 0 or node_index >= len(self.__data):
            print('index '+str(node_index)+' out of range!')
            return -1
        node = self.__data[node_index]
        index_chain = [node_index]
        while node_index != node.pre_index:
            node_index = node.pre_index
            node = self.__data[node_index]
            index_chain.append(node_index)

        # path compression
        for n in index_chain:
            self.__data[n].pre_index = node_index
        return node_index

    def union(self, a_index: int, b_index: int):
        if a_index < 0 or a_index >= len(self.__data):
            print('index ' + str(a_index) + ' out of range!')
        if b_index < 0 or b_index >= len(self.__data):
            print('index ' + str(b_index) + ' out of range!')

        a_leader_index = self.find(a_index)
        b_leader_index = self.find(b_index)
        if a_leader_index == b_leader_index:
            return
        a_leader_node = self.__data[a_leader_index]
        b_leader_node = self.__data[b_leader_index]
        # union by rank
        if a_leader_node.rank > b_leader_node.rank:
            b_leader_node.pre_index = a_leader_index
            return
        if a_leader_node.rank < b_leader_node.rank:
            a_leader_node.pre_index = b_leader_index
            return
        if a_leader_node.rank == b_leader_node.rank:
            a_leader_node.rank += 1
            b_leader_node.pre_index = a_leader_index


class Edge:
    def __init__(self, start_node: int, end_node: int, cost: int):
        self.start_node = start_node
        self.end_node = end_node
        self.cost = cost


G = {}
edge_list = []
node_num = 0


def max_k_clustering(k: int)->int:
    global G
    global edge_list
    global node_num
    edge_list.sort(key=lambda edge: edge.cost)
    current_edge_index = 0
    node_union = UnionFind(size=node_num+1)

    # merge until left k clusters
    while k != node_num:
        current_edge = edge_list[current_edge_index]
        start_node = current_edge.start_node
        end_node = current_edge.end_node
        if node_union.find(start_node) != node_union.find(end_node):
            node_union.union(start_node, end_node)
            k += 1
        current_edge_index += 1

    # find min spacing between clusters
    while True:
        current_edge = edge_list[current_edge_index]
        start_node = current_edge.start_node
        end_node = current_edge.end_node
        if node_union.find(start_node) != node_union.find(end_node):
            return edge_list[current_edge_index].cost
        current_edge_index += 1


def main():
    global G
    global edge_list
    global node_num

    # decompress clustering1.txt file
    with gzip.open('clustering1.txt.gz', 'rb') as read, open('clustering1.txt', 'wb') as write:
        shutil.copyfileobj(read, write)

    # load graph data
    with open('clustering1.txt', 'r') as file:
        meta_line = file.readline().split()
        node_num = int(meta_line[0])
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                line = line.split()
                start_node = int(line[0])
                end_node = int(line[1])
                cost = int(line[2])
                if start_node not in G:
                    G[start_node] = {}
                G[start_node][end_node] = cost
                edge_list.append(Edge(start_node=start_node, end_node=end_node, cost=cost))

    print(max_k_clustering(4))


if __name__ == "__main__":
    main()
