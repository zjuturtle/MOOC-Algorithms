import random

best_min_cut = 0
node_num = 0
G = {}


def add_edge(node_from: int, node_to: int, num: int):
    global G
    if G[node_from].get(node_to):
        G[node_from][node_to] += num
        return
    G[node_from][node_to] = num


def random_contraction() -> bool:
    global best_min_cut
    global node_num
    global G
    if node_num == 2:
        for (node, edge) in G.items():
            if len(edge) == 0:
                continue
            for (k, v) in edge.items():
                best_min_cut = min(best_min_cut, v)
                return True

    edge_num = 0

    # 所有的edge数目*2(因为是无向图)
    for (node, edge) in G.items():
        edge_num += sum(edge.values())
    if edge_num == 0:
        print(node_num)

    # 在所有的edge里面随机一个
    random_edge_index = random.randint(1, edge_num)

    for node_index in range(1, len(G)+1):
        edge = G[node_index]
        current_sum = sum(edge.values())

        if random_edge_index < current_sum:
            choice_edge_from = node_index  # 选中的edge的一头为choice_edge_from
            choice_edge_to = -1
            for (current_edge, current_edge_num) in edge.items():
                random_edge_index -= current_edge_num
                if random_edge_index <= 0:
                    choice_edge_to = current_edge  # 选中edge的另一头为choice_edge_to
                    break

            # 合并节点，将choice_edge_to合并到choice_edge_from
            G[choice_edge_from].pop(choice_edge_to)

            # 遍历与choice_edge_to邻接的所有节点
            for choice_edge_to_node in G[choice_edge_to]:

                if choice_edge_to_node == choice_edge_from:  # 该邻接节点为choice_edge_from则不操作
                    continue
                tmp = G[choice_edge_to_node].pop(choice_edge_to)  # 取该邻接节点与choice_edge_to的边数目
                add_edge(choice_edge_to_node, choice_edge_from, tmp)  # 修改 choice_edge_to_node 和 choice_edge_to_node之间的边
                add_edge(choice_edge_from, choice_edge_to_node, tmp)

            G[choice_edge_to].clear()
            node_num -= 1
            break
        random_edge_index -= current_sum

    return False


def graph_copy(initial_g):
    global G
    for (key, value) in initial_g.items():
        G[key] = value.copy()


def main():
    global G
    global best_min_cut
    global node_num
    initial_g = {}

    with open('kargerMinCut.txt', 'r') as graph_file:
        while True:
            lines = graph_file.readlines(300)
            if not lines:
                break
            for line in lines:
                edge = {}
                first = True
                node_index = -1
                for x in line.split():
                    if first:
                        node_index = int(x)
                        first = False
                        continue
                    edge[int(x)] = 1
                initial_g[node_index] = edge
        best_min_cut = len(initial_g)
    for count in range(0, 1000):
        graph_copy(initial_g)
        node_num = len(G)
        while True:
            if random_contraction():
                break
    print('min cut '+str(best_min_cut))


if __name__ == "__main__":
    main()
