item_list = []
knapsack_size = 0
number_of_items = 0


class Item:
    def __init__(self, value: int, weight: int):
        self.value = value
        self.weight = weight


def knapsack()->int:
    global item_list
    global knapsack_size
    global number_of_items
    A = [([0] * (knapsack_size+1)) for i in range(number_of_items+1)]
    for i in range(1, number_of_items+1):
        item = item_list[i - 1]
        for x in range(0, knapsack_size+1):
            if item.weight > x:
                A[i][x] = A[i-1][x]
            else:
                A[i][x] = max(A[i-1][x], A[i-1][x-item.weight] + item.value)
    return A[number_of_items][knapsack_size]


def main():
    global knapsack_size
    global number_of_items
    global item_list
    with open('knapsack1.txt', 'r') as file:
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
    print(knapsack())


if __name__ == "__main__":
    main()
