array = []
comparisons = 0


def find_mid(a: int, b: int, c: int) -> int:
    if array[a] <= array[b] <= array[c] or array[c] <= array[b] <= array[a]:
        return b
    if array[b] <= array[a] <= array[c] or array[c] <= array[a] <= array[b]:
        return a
    if array[a] <= array[c] <= array[b] or array[b] <= array[c] <= array[a]:
        return c


def partition(left_index: int, right_index: int) -> int:
    global array
    if left_index == right_index:
        return left_index

    # define mid_index and find pivot index
    mid_index = int((right_index-left_index)/2)+left_index
    pivot_index = find_mid(left_index, mid_index, right_index)

    # exchange pivot element and left element
    tmp = array[left_index]
    array[left_index] = array[pivot_index]
    array[pivot_index] = tmp
    pivot_index = left_index
    pivot = array[pivot_index]
    i = left_index + 1
    for j in range(left_index+1, right_index+1):
        if array[j] < pivot:
            tmp = array[j]
            array[j] = array[i]
            array[i] = tmp
            i = i+1
    tmp = array[pivot_index]
    array[pivot_index] = array[i-1]
    array[i-1] = tmp
    pivot_index = i-1
    return pivot_index


def quick_sort(left_index: int, right_index: int):
    global array
    global comparisons
    if left_index >= right_index:
        return
    comparisons += (right_index - left_index)
    pivot_index = partition(left_index, right_index)
    quick_sort(left_index, pivot_index-1)
    quick_sort(pivot_index+1, right_index)


def main():
    with open('QuickSort.txt', 'r') as array_file:
        for val in array_file.read().split():
            array.append(int(val))
    quick_sort(0, len(array)-1)
    print(comparisons)


if __name__ == "__main__":
    main()
