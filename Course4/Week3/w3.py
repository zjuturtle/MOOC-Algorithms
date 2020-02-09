import numpy as np
import gzip
import shutil


class City:
    def __init__(self, x: np.float64, y: np.float64):
        self.x = x
        self.y = y


city_list = []
city_num = 0
INFINITY = np.float64(10000000000000000)


def distance_square(a: City, b: City)->np.float64:
    dx = a.x - b.x
    dy = a.y - b.y
    return dx*dx + dy*dy


def greedy_tsp()->int:
    global city_list
    global city_num
    global INFINITY
    res = np.float64(0)
    unvisited = set(range(1, city_num))
    visited_count = 1
    current_city_index = 0
    while visited_count != city_num:
        next_city_index = -1
        min_distance = INFINITY
        for index in unvisited:
            d = distance_square(city_list[index], city_list[current_city_index])
            if d > min_distance:
                continue
            if d < min_distance:
                min_distance = d
                next_city_index = index
                continue
            if index < next_city_index:
                next_city_index = index
        res += np.sqrt(min_distance)
        visited_count += 1
        unvisited.discard(next_city_index)
        current_city_index = next_city_index
    res += np.sqrt(distance_square(city_list[0], city_list[current_city_index]))
    return int(res)


def main():
    global city_list
    global city_num

    # decompress file
    with gzip.open('nn.txt.gz', 'rb') as read, open('nn.txt', 'wb') as write:
        shutil.copyfileobj(read, write)

    with open('nn.txt', 'r') as file:
        meta_line = file.readline().split()
        city_num = int(meta_line[0])
        while True:
            lines = file.readlines(5000)
            if not lines:
                break
            for line in lines:
                line = line.split()
                city_list.append(City(x=(np.float64(line[1])), y=np.float64(line[2])))

    print(greedy_tsp())


if __name__ == "__main__":
    main()
