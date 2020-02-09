from typing import List


def count_split_inv(b: List[int], c: List[int]) -> int:
    d = []
    n = len(b) + len(c)
    i = 0
    j = 0
    res = 0
    for k in range(0, n):
        if i == len(b):
            break
        if j == len(c):
            break

        if b[i] < c[j]:
            d.append(b[i])
            i += 1
        else:
            d.append(c[j])
            j += 1
            res += (len(b) - i)
    return res


def sort_count(a: List[int]) -> (List[int], int):
    if len(a) == 1:
        return a, 0
    else:
        a1 = a[:int(len(a)/2)]
        a2 = a[int(len(a)/2):]
        b, x = sort_count(a1)
        c, y = sort_count(a2)
        z = count_split_inv(b, c)
        return sorted(a), x + y + z


def main():
    array = []
    with open('IntegerArray.txt', 'r') as array_file:
        for val in array_file.read().split():
            array.append(int(val))
    print(sort_count(array)[1])


if __name__ == "__main__":
    main()
