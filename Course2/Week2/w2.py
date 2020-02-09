from typing import List


class Element:
    def __init__(self, start_node, end_node, value):
        self.start_node = start_node
        self.end_node = end_node
        self.value = value


class Item:
    def __init__(self, key: int, val: int, addition=None):
        self.key = key
        self.val = val
        self.addition = addition


class Heap:
    def __init__(self, data: List[Item]=None):
        if data is None:
            self.__data = []
            self.__map = {}
            return

        # fill in array
        self.__data = data[:]
        self.__map = {}

        for index in range(0, len(data)):
            self.__map[data[index].key] = index

        if len(data) <= 1:
            return

        # adjust position
        height = 1
        while ((1 << height)-1) < len(data):
            height += 1

        while height >= 2:
            for index in range(((1 << (height - 1)) - 1), (1 << height) - 1):
                if index >= len(self.__data):
                    break

                # bubble up
                while True:
                    father_index = (index - 1) // 2
                    if father_index < 0:
                        break
                    if self.__data[index].val < self.__data[father_index].val:

                        # swap index item and father_index item
                        tmp = self.__data[index]
                        self.__data[index] = self.__data[father_index]
                        self.__data[father_index] = tmp

                        # modify key index map
                        self.__map[self.__data[index].key] = index
                        self.__map[self.__data[father_index].key] = father_index
                        index = father_index
                    else:
                        break
            height -= 1

    def insert(self, item: Item):
        if self.contain_key(item.key):
            print('!!!!!!!!already has key '+str(item.key))

        self.__data.append(item)
        self.__map[item.key] = len(self.__data)-1
        current_index = len(self.__data) - 1
        while current_index != 0:
            father_index = (current_index - 1) // 2
            if self.__data[father_index].val > self.__data[current_index].val:

                # swap father_index item and current_index item
                tmp = self.__data[father_index]
                self.__data[father_index] = self.__data[current_index]
                self.__data[current_index] = tmp

                # modify key index map
                self.__map[self.__data[current_index].key] = current_index
                self.__map[self.__data[father_index].key] = father_index
            current_index = father_index

    def pop_min(self) -> Item:
        min_item = self.__data[0]
        self.__map.pop(min_item.key)

        # swap last item and first(min) item, then delete last item(min item)
        self.__data[0] = self.__data[-1]
        del self.__data[-1]

        # in case heap is empty after pop
        if 0 == len(self.__data):
            return min_item

        # modify key index map
        self.__map[self.__data[0].key] = 0

        current_index = 0
        heap_size = len(self.__data)
        while current_index*2 + 1 < heap_size:
            left_index = current_index*2 + 1
            right_index = current_index*2 + 2
            if right_index == heap_size:
                right_index = left_index
            min_child_index = left_index if self.__data[left_index].val < self.__data[right_index].val else right_index

            # swap current_index item and min_child_index item
            tmp = self.__data[min_child_index]
            self.__data[min_child_index] = self.__data[current_index]
            self.__data[current_index] = tmp

            # modify key index map
            self.__map[self.__data[min_child_index].key] = min_child_index
            self.__map[self.__data[current_index].key] = current_index
            current_index = min_child_index
        return min_item

    def get_min(self) -> Item:
        return self.__data[0]

    def size(self) -> int:
        return len(self.__data)

    def empty(self) -> bool:
        return len(self.__data) == 0

    def delete_by_item(self, item: Item) -> Item:
        return self.delete_by_key(item.key)

    def delete_by_key(self, key: int) -> Item:
        index = self.__map[key]
        delete_item = self.__data[index]

        # swap data[index] and data[-1]
        self.__data[index] = self.__data[-1]
        del self.__data[-1]

        # if delete item is the last item in data array
        self.__map.pop(key)
        if index == len(self.__data):
            return delete_item

        self.__map[self.__data[index].key] = index

        left_child_index = index * 2 + 1
        if left_child_index >= len(self.__data):
            left_child_index = index
        father_index = max((index-1)//2, 0)

        while self.__data[father_index].val > self.__data[index].val:

            # swap data[father_index] and data[index]
            tmp = self.__data[father_index]
            self.__data[father_index] = self.__data[index]
            self.__data[index] = tmp

            # modify key index map
            self.__map[self.__data[father_index].key] = father_index
            self.__map[self.__data[index].key] = index

            # update index and father_index
            index = father_index
            father_index = (index-1)//2
            if father_index < 0:
                break

        while self.__data[left_child_index].val < self.__data[index].val:

            # swap data[left_child_index] and data[index]
            tmp = self.__data[left_child_index]
            self.__data[left_child_index] = self.__data[index]
            self.__data[index] = tmp

            # modify key index map
            self.__map[self.__data[left_child_index].key] = left_child_index
            self.__map[self.__data[index].key] = index

            # update index and left_child_index
            index = left_child_index
            left_child_index = index * 2 + 1
            if left_child_index >= len(self.__data):
                break
        return delete_item

    def contain_key(self, key: int)->bool:
        return key in self.__map

    def get_by_key(self, key: int)->Item:
        return self.__data[self.__map[key]]


G = {}
node_max_index = 0
INFINITY = 10000000


def dijkstra(s: int):
    global G
    global node_max_index
    global INFINITY

    # init heap holds item as: key[v]=smallest Dijkstra greedy score of an edge(u,v) in E with u in X but v not in X
    heap_list = []
    for v, edge_to in G.items():
        if v == s:
            continue
        if v in G[s]:
            heap_list.append(Item(key=v, val=G[s][v], addition=s))
        else:
            heap_list.append(Item(key=v, val=INFINITY, addition=s))

    heap = Heap(data=heap_list)

    # A: computed shortest path distance
    # X: vertices processed so far
    A = [INFINITY] * (node_max_index+1)
    A[s] = 0
    X = set([s])

    while len(X) != len(G):

        # extract from heap
        item = heap.pop_min()
        v = item.addition
        w = item.key
        A[w] = A[v] + G[v][w]

        # for each edge(w,v) in E
        for vv, _ in G[w].items():
            if heap.contain_key(vv):
                tmp_item = heap.get_by_key(vv)
                tmp_val = A[w] + G[w][vv]
                # update heap if necessary
                if tmp_item.val > tmp_val:
                    heap.delete_by_key(vv)
                    heap.insert(Item(key=vv, val=tmp_val, addition=w))
        X.add(w)

    print(str(A[7])+',' +
          str(A[37])+',' +
          str(A[59]) + ',' +
          str(A[82]) + ',' +
          str(A[99]) + ',' +
          str(A[115]) + ',' +
          str(A[133]) + ',' +
          str(A[165]) + ',' +
          str(A[188]) + ',' +
          str(A[197]))


def main():
    global G
    global node_max_index

    with open('dijkstraData.txt', 'r') as graph_file:
        while True:
            lines = graph_file.readlines(200)
            if not lines:
                break
            for line in lines:
                line = line.split()
                start_node = int(line[0])
                if start_node not in G:
                    G[start_node] = {}
                for index in range(1, len(line)):
                    edge = line[index].split(sep=',')
                    end_node, length = [int(edge[0]), int(edge[1])]
                    G[start_node][end_node] = length
                    if end_node not in G:
                        G[end_node] = {}

                    node_max_index = max(node_max_index, start_node, end_node)
    dijkstra(1)


if __name__ == "__main__":
    main()
