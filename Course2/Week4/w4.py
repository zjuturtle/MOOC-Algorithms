import gzip
import shutil
from bisect import bisect_left, bisect_right


def main():
    # decompress 2sum.txt file
    with gzip.open('2sum.txt.gz', 'rb') as read, open('2sum.txt', 'wb') as write:
        shutil.copyfileobj(read, write)

    data = []
    with open('2sum.txt', 'r') as file:
        for val in file.read().split():
            data.append(int(val))
        data.sort()

    target = set()
    for num in data:
        left = bisect_left(data, -10000 - num)
        right = bisect_right(data, 10000 - num)
        for item in data[left:right]:
            if item != num:
                target.add(num+item)

    print(len(target))


if __name__ == "__main__":
    main()
