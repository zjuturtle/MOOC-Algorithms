from typing import List
W = []
vertex_num = 0


def max_set(check_list: List[int]) -> str:
    global W
    global vertex_num
    res = ''

    # dynamic programming solve
    A = [0, W[0]]  # A[index] means W[0 ~ (index-1)] subproblem max sum weight
    for i in range(2, len(W) + 1):
        A.append(max(A[i-1], A[i-2] + W[i-1]))

    # reconstruction
    S = set()
    i = len(W)
    while i >= 1:
        if A[i-1] >= A[i-2] + W[i-1]:
            i -= 1
        else:
            S.add(i)
            i -= 2

    for i in range(0, len(check_list)):
        if check_list[i] in S:
            res += '1'
        else:
            res += '0'
    return res


def main():
    global W
    global vertex_num
    with open('mwis.txt', 'r') as file:
        meta_line = file.readline().split()
        vertex_num = int(meta_line[0])
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                W.append(int(line))
    print(max_set([1, 2, 3, 4, 17, 117, 517, 997]))


if __name__ == "__main__":
    main()
