import sys

item_list = []
cache = {}


class Item:
    def __init__(self, value: int, weight: int):
        self.value = value
        self.weight = weight


def knapsack(i: int, x: int) -> int:
    global item_list
    global cache
    if i < 1:
        return 0
    item = item_list[i-1]
    if x < item.weight:
        return 0
    if i in cache:
        if x in cache[i]:
            return cache[i][x]
    res = max(knapsack(i-1, x), item.value + knapsack(i-1, x - item.weight))
    if i not in cache:
        cache[i] = {}
    cache[i][x] = res
    return res


def main():
    global knapsack_size
    global number_of_items
    global item_list
    sys.setrecursionlimit(100000)
    with open('knapsack_big.txt', 'r') as file:
        meta_line = file.readline().split()
        knapsack_size = int(meta_line[0])
        number_of_items = int(meta_line[1])
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                line = line.split()
                item_list.append(Item(value=int(line[0]), weight=int(line[1])))
        item_list.sort(key=lambda item: item.weight)
    print(knapsack(number_of_items, knapsack_size))


if __name__ == "__main__":
    main()
