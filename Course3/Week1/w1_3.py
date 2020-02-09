G = {}
V = set()
node_num = 0


class Item:
    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val


class Heap:
    def __init__(self):
        self.__map = {}
        self.__data = []
        self.__size = 0

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


def prim_min_spanning_tree() -> int:
    global G
    global V
    global node_num
    total_edge_cost = 0

    # initialize
    X = set()  # current span node
    u = 1
    X.add(u)
    heap = Heap()  # for graph G=(V,E), heap = vertices of V-X
    for v in V:
        if v in X:
            continue
        if u in G[v]:
            heap.insert(Item(key=v, val=G[v][u]))
        else:
            heap.insert(Item(key=v, val=9999999))

    while len(X) != node_num:
        item = heap.pop_min()  # pop min edge(u,v) from heap with u in X and v not in X
        total_edge_cost = total_edge_cost + item.val
        v = item.key
        X.add(v)
        # update heap
        for w, cost in G[v].items():
            if heap.contain_key(w):
                item = heap.delete_by_key(w)
                new_item = Item(key=w, val=min(item.val, G[v][w]))
                heap.insert(new_item)

    return total_edge_cost


def main():
    global G
    global V
    global node_num
    with open('edges.txt', 'r') as file:
        meta_line = file.readline().split()
        node_num = int(meta_line[0])
        for line in file.readlines():
            line = line.split()
            node1 = int(line[0])
            node2 = int(line[1])
            cost = int(line[2])
            if node1 not in G:
                G[node1] = {}
            if node2 not in G:
                G[node2] = {}
            G[node1][node2] = cost
            G[node2][node1] = cost
            V.add(node1)
            V.add(node2)
    print(prim_min_spanning_tree())


if __name__ == "__main__":
    main()
