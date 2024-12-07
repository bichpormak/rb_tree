import graphviz

BLACK = 'black'
RED = 'red'

class Node:
    def __init__(self, key, color, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.color = color
        self.parent = parent

    def __str__(self):
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        parent = self.parent.key if self.parent else None
        return 'key: {}, left: {}, right: {}, color: {}, parent: {}'.format(self.key, left, right, self.color, parent)


def breadth_first_search(root, dot):
    pass

class RBTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key, BLACK)

        else:
            current = self.root
            while current:
                if key < current.key:
                    if not current.left:
                        new_node = Node(key, RED, parent = current)
                        current.left = new_node
                        break

                    current = current.left

                else:
                    if not current.right:
                        new_node = Node(key, RED, parent = current)
                        current.right = new_node
                        break

                    current = current.right



    def left_rotate(self, node_a):
        pass

    def right_rotate(self, node_b):
        pass


def main():
    nodes = list(map(int, input().split()))
    tb_tree = RBTree()
    for index, node in enumerate(nodes):
        dot = graphviz.Digraph()


if __name__ == '__main__':
    main()