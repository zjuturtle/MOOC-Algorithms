class HeapMin:
    def __init__(self):
        self.__map = {}
        self.__data = []
        self.__size = 0

    def insert(self, k: int):
        self.__data.append(k)
        current_index = len(self.__data) - 1
        while current_index != 0:
            father_index = (current_index - 1) // 2
            if self.__data[father_index] > self.__data[current_index]:
                tmp = self.__data[father_index]
                self.__data[father_index] = self.__data[current_index]
                self.__data[current_index] = tmp
            current_index = father_index

    def pop_min(self) -> int:
        min_element = self.__data[0]
        self.__data[0] = self.__data[-1]
        del self.__data[-1]
        current_index = 0
        heap_size = len(self.__data)
        while current_index*2 + 1 < heap_size:
            left_index = current_index*2 + 1
            right_index = current_index*2 + 2
            if right_index == heap_size:
                right_index = left_index
            min_child_index = left_index if self.__data[left_index] < self.__data[right_index] else right_index
            tmp = self.__data[min_child_index]
            self.__data[min_child_index] = self.__data[current_index]
            self.__data[current_index] = tmp
            current_index = min_child_index
        return min_element

    def get_min(self) -> int:
        return self.__data[0]

    def size(self) -> int:
        return len(self.__data)

    def empty(self) -> bool:
        return len(self.__data) == 0


class HeapMax:
    def __init__(self):
        self.__map = {}
        self.__data = []
        self.__size = 0

    def insert(self, k: int):
        self.__data.append(k)
        current_index = len(self.__data) - 1
        while current_index != 0:
            father_index = (current_index - 1) // 2
            if self.__data[father_index] < self.__data[current_index]:
                tmp = self.__data[father_index]
                self.__data[father_index] = self.__data[current_index]
                self.__data[current_index] = tmp
            current_index = father_index

    def pop_max(self) -> int:
        max_element = self.__data[0]
        self.__data[0] = self.__data[-1]
        del self.__data[-1]
        current_index = 0
        heap_size = len(self.__data)
        while current_index*2 + 1 < heap_size:
            left_index = current_index*2 + 1
            right_index = current_index*2 + 2
            if right_index == heap_size:
                right_index = left_index
            min_child_index = left_index if self.__data[left_index] > self.__data[right_index] else right_index
            tmp = self.__data[min_child_index]
            self.__data[min_child_index] = self.__data[current_index]
            self.__data[current_index] = tmp
            current_index = min_child_index
        return max_element

    def get_max(self) -> int:
        return self.__data[0]

    def size(self) -> int:
        return len(self.__data)

    def empty(self) -> bool:
        return len(self.__data) == 0


def main():
    #  elements in [heap_max] < elements in [heap_min]
    heap_min = HeapMin()
    heap_max = HeapMax()
    sum = 0
    with open('Median.txt', 'r') as file:
        for val in file.read().split():
            # 插入数据
            data = int(val)
            if heap_max.empty():
                heap_max.insert(data)
            else:
                if data < heap_max.get_max():
                    heap_max.insert(data)
                else:
                    heap_min.insert(data)

            # 调整两个 Heap 的大小
            if heap_min.size() == heap_max.size()+2:
                heap_max.insert(heap_min.pop_min())

            if heap_max.size() == heap_min.size()+2:
                heap_min.insert(heap_max.pop_max())

            # 获得当前的中间值
            if heap_min.size() == heap_max.size():
                sum += heap_max.get_max()
            else:
                if heap_min.size() == heap_max.size()+1:
                    sum += heap_min.get_min()
                if heap_max.size() == heap_min.size()+1:
                    sum += heap_max.get_max()
    print(sum % 10000)


if __name__ == "__main__":
    main()
