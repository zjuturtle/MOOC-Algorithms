import math
from typing import Set


class City:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


city_list = []
city_num = -1
INFINITY = 10000000
choose_S_list = []
dis = []


def set_to_num(S: Set[int])->int:
    """
    transform S set form into int form
    :param S: Set
    :return:  int
    """
    S_num = 0
    for node in S:
        S_num += (1 << (node-1))
    return S_num


def num_to_set(S: int)->Set[int]:
    """
    transform S in form into set form
    :param S: in
    :return:  Set
    """
    S_set = set()
    current_index = 1
    while S:
        if S % 2:
            S_set.add(current_index)
        current_index += 1
        S = S >> 1
    return S_set


def generate_S_set(num_chosen: int, bits_decided: int, bits_left: int, available: int):
    global choose_S_list
    if available < 0:
        return
    if available == 0:
        choose_S_list.append(num_chosen)
        return
    if bits_left == 0:
        return
    generate_S_set(num_chosen, bits_decided+1, bits_left-1, available)
    generate_S_set(num_chosen + (1 << bits_decided), bits_decided+1, bits_left-1, available-1)


def tsp()->float:
    global city_list
    global city_num
    global choose_S_list
    global dis
    A = {}

    # fill in base case
    for node in range(1, city_num+1):
        A[(1 << node)-1] = {}
        A[(1 << node)-1][1] = INFINITY
    A[1][1] = 0

    # main for loop
    for m in range(2, city_num+1):

        # for each set S in {1,2,...,n} of size m that contains 1
        choose_S_list = []
        generate_S_set(1, 1, city_num-1, m-1)
        for S_num in choose_S_list:
            S = num_to_set(S_num)
            A[S_num] = {}
            # for each j in S, j not 1
            for j in S:
                if j == 1:
                    continue
                S_j = S.copy()  # S-{j}
                S_j.discard(j)
                S_j_num = set_to_num(S_j)
                minimum = INFINITY
                for k in S:
                    if k == j:
                        continue
                    if k not in A[S_j_num]:
                        A[S_j_num][k] = INFINITY
                    val = A[S_j_num][k] + dis[k-1][j-1]
                    if val < minimum:
                        minimum = val
                A[S_num][j] = minimum

        # clean memory
        choose_S_list = []
        generate_S_set(1, 1, city_num - 1, m - 2)

        for item in choose_S_list:
            del A[item]

    # calculate final result
    res = INFINITY
    S_num = (1 << city_num) - 1
    for j in range(2, city_num+1):
        val = A[S_num][j] + dis[j-1][0]
        if val < res:
            res = val
    return int(res)


def main():
    """
    This implementation could be a little slow. May take about half hour or longer.
    :return:
    """
    global city_list
    global city_num
    global dis
    with open('tsp.txt', 'r') as file:
        meta_line = file.readline().split()
        city_num = int(meta_line[0])
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                line = line.split()
                city_list.append(City(x=float(line[0]), y=float(line[1])))
        dis = [[INFINITY]*city_num for i in range(city_num)]
        for a in range(0, city_num):
            for b in range(a, city_num):
                city_a = city_list[a]
                city_b = city_list[b]
                dx = city_a.x - city_b.x
                dy = city_a.y - city_b.y
                c = math.sqrt(dx*dx + dy*dy)
                dis[a][b] = c
                dis[b][a] = c

    print(tsp())


if __name__ == "__main__":
    main()
