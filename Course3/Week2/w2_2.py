import gzip
import shutil

node_list = []
node_num = 0
bits_num = 0
high_bit_num = 0


class Node:
    def __init__(self, index: int, val: int):
        self.index = index
        self.val = val
        self.probe_val = 0


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


def max_k_clustering_with_spacing_3() -> int:
    global node_list
    global node_num
    global bits_num
    cluster_num = node_num
    node_union = UnionFind(size=node_num)
    for col_1 in range(0, bits_num-1):
        for col_2 in range(col_1+1, bits_num):
            # make col 1 bit and col 2 bit set to 1 and assign to probe_val
            for i in range(0, node_num):
                node = node_list[i]
                node.probe_val = node.val | ((1 << col_1) + (1 << col_2))
            node_list.sort(key=lambda node: node.probe_val)
            for i in range(0, len(node_list) - 1):
                first_node = node_list[i]
                latter_node = node_list[i + 1]

                # if Hamming distance <= 2
                if (first_node.probe_val ^ latter_node.probe_val) == 0:
                    # if first_node and latter_node has not yet merged(not belong to same cluster)
                    if node_union.find(first_node.index) != node_union.find(latter_node.index):
                        cluster_num -= 1
                        node_union.union(first_node.index, latter_node.index)

    return cluster_num


def main():
    global node_list
    global bits_num
    global node_num
    global high_bit_num
    # decompress clustering1.txt file
    with gzip.open('clustering_big.txt.gz', 'rb') as read, open('clustering_big.txt', 'wb') as write:
        shutil.copyfileobj(read, write)

    # load graph data
    with open('clustering_big.txt', 'r') as file:
        meta_line = file.readline().split()
        node_num = int(meta_line[0])
        bits_num = int(meta_line[1])
        high_bit_num = pow(2, bits_num-1)
        index = 0
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                data = 0
                line = line.split()
                for i in range(0, bits_num):
                    data = data*2 + int(line[i])
                node_list.append(Node(index=index, val=data))
                index += 1
    print(max_k_clustering_with_spacing_3())


if __name__ == "__main__":
    main()
