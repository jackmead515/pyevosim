import networkx as nx

class KDTree():

    def __init__(self, data, leaf_size=10):
        self.data = data
        self.leaf_size = leaf_size

        self.tree = self.build_tree(data, 0)        

    def build_tree(self, data, depth):
        n = len(data)

        if n <= self.leaf_size:
            return data

        axis = depth % len(data[0])

        data = sorted(data, key=lambda x: x[axis])

        return [
            self.build_tree(data[:n//2], depth+1),
            self.build_tree(data[n//2:], depth+1)
        ]

    def find_nearest(self, point, depth=0):
        axis = depth % len(point)

        if isinstance(self.tree, list):
            if point[axis] < self.tree[0][0][axis]:
                return self.tree[0].find_nearest(point, depth+1)
            else:
                return self.tree[1].find_nearest(point, depth+1)
        else:
            return self.tree

    def find_within(self, point, radius, depth=0):
        axis = depth % len(point)

        if isinstance(self.tree, list):
            if point[axis] < self.tree[0][0][axis]:
                return self.tree[0].find_within(point, radius, depth+1)
            else:
                return self.tree[1].find_within(point, radius, depth+1)
        else:
            return self.tree

    def __repr__(self):
        return str(self.tree)


if __name__ == "__main__":

    import matplotlib.pyplot as plot

    tree = KDTree([
        [2, 3],
        [5, 4],
        [9, 6],
        [4, 7],
        [8, 1],
        [7, 2]
    ])

    print(tree.find_within([3, 4], 1))
