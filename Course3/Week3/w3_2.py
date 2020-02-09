symbol_num = 0
symbol_list = []
min_len = 0


class Node:
    def __init__(self, weight: int, largest_weight: bool):
        self.weight = weight
        self.largest_weight = largest_weight  # flag for contains largest weight symbol

    def __add__(self, other):
        global min_len
        if self.largest_weight or other.largest_weight:
            min_len += 1
            return Node(self.weight + other.weight, True)
        else:
            return Node(self.weight + other.weight, False)


def huffman_code_min_len()->int:
    global symbol_num
    global symbol_list
    symbol_list.sort()
    raw_queue = []
    for i in range(0, symbol_num):
        raw_queue.append(Node(weight=symbol_list[i], largest_weight=False))
    raw_queue[-1].largest_weight = True
    meta_queue = []
    merge_count = 0
    while merge_count < symbol_num - 1:
        merge_count += 1
        if len(meta_queue) == 0:
            meta_queue.append(raw_queue[0] + raw_queue[1])
            raw_queue.pop(0)
            raw_queue.pop(0)
            continue
        if len(meta_queue) == 1:
            if meta_queue[0].weight < raw_queue[1].weight:  # case for merge in meta_queue and raw_queue
                tmp = raw_queue.pop(0) + meta_queue.pop(0)
                meta_queue.append(tmp)
            else:  # case for merge in raw_queue
                meta_queue.append(raw_queue[0] + raw_queue[1])
                raw_queue.pop(0)
                raw_queue.pop(0)
            continue
        if len(raw_queue) == 0:
            tmp = meta_queue[0] + meta_queue[1]
            meta_queue.pop(0)
            meta_queue.pop(0)
            meta_queue.append(tmp)
            continue
        if len(raw_queue) == 1:
            if raw_queue[0].weight < meta_queue[1].weight:
                tmp = raw_queue.pop(0) + meta_queue.pop(0)
                meta_queue.append(tmp)
            else:
                tmp = meta_queue[0] + meta_queue[1]
                meta_queue.pop(0)
                meta_queue.pop(0)
                meta_queue.append(tmp)
            continue

        # case for both queue length >=2, choose two from raw_queue
        if raw_queue[1].weight < meta_queue[0].weight:
            meta_queue.append(raw_queue[0] + raw_queue[1])
            raw_queue.pop(0)
            raw_queue.pop(0)
            continue
        # case for both queue length >=2, choose two from meta_queue
        if raw_queue[0].weight > meta_queue[1].weight:
            tmp = meta_queue[0] + meta_queue[1]
            meta_queue.pop(0)
            meta_queue.pop(0)
            meta_queue.append(tmp)
            continue
        # case for both queue length >=2, choose one from each queue
        tmp = meta_queue.pop(0) + raw_queue.pop(0)
        meta_queue.append(tmp)
    return min_len


def main():
    global symbol_num
    global symbol_list
    with open('huffman.txt', 'r') as file:
        meta_line = file.readline().split()
        symbol_num = int(meta_line[0])
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                symbol_list.append(int(line))
    print(huffman_code_min_len())


if __name__ == "__main__":
    main()





