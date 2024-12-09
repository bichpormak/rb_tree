BLACK = 'black'
RED = 'red'


class Node:
    def __init__(self, full_name, math, informatics, russian, color=RED, parent=None):
        self.full_name = full_name
        self.math = math
        self.informatics = informatics
        self.russian = russian
        self.total_points = math + informatics + russian
        self.color = color
        self.parent = parent
        self.left = None
        self.right = None

    @property
    def key(self):
        return (self.total_points, self.math, self.informatics, self.russian)

    def __str__(self):
        parent_name = self.parent.full_name if self.parent else None
        return (f"Full Name: {self.full_name}, Total Points: {self.total_points}, "
                f"Math: {self.math}, Informatics: {self.informatics}, Russian: {self.russian}, "
                f"Color: {self.color}, Parent: {parent_name}")


class RBTree:
    def __init__(self):
        self.root = None
        self.name_to_node = {}

    def insert(self, full_name, math, informatics, russian):
        new_node = Node(full_name, math, informatics, russian)
        if not self.root:
            self.root = new_node
            self.root.color = BLACK
        else:
            current = self.root
            while True:
                if new_node.key < current.key:
                    if current.left is None:
                        current.left = new_node
                        new_node.parent = current
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        new_node.parent = current
                        break
                    current = current.right
            self.fix_tree(new_node)
        self.name_to_node[full_name] = new_node

    def fix_tree(self, node):
        while node.parent and node.parent.color == RED:
            grandparent = node.parent.parent
            if not grandparent:
                break
            if node.parent == grandparent.left:
                uncle = grandparent.right
                if uncle and uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    node = grandparent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = BLACK
                    grandparent.color = RED
                    self.right_rotate(grandparent)
            else:
                uncle = grandparent.left
                if uncle and uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    node = grandparent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = BLACK
                    grandparent.color = RED
                    self.left_rotate(grandparent)
        if self.root.color == RED:
            self.root.color = BLACK

    def left_rotate(self, node):
        new_node = node.right
        if not new_node:
            return
        node.right = new_node.left
        if new_node.left:
            new_node.left.parent = node
        new_node.parent = node.parent
        if not node.parent:
            self.root = new_node
        elif node == node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        new_node.left = node
        node.parent = new_node

    def right_rotate(self, node):
        new_node = node.left
        if not new_node:
            return
        node.left = new_node.right
        if new_node.right:
            new_node.right.parent = node
        new_node.parent = node.parent
        if not node.parent:
            self.root = new_node
        elif node == node.parent.right:
            node.parent.right = new_node
        else:
            node.parent.left = new_node
        new_node.right = node
        node.parent = new_node

    def search_by_name(self, full_name):
        return self.name_to_node.get(full_name, None)

    def delete_by_name(self, full_name):
        node = self.search_by_name(full_name)
        if node:
            self._delete_node(node)
            del self.name_to_node[full_name]

    def _minimum(self, node):
        while node.left:
            node = node.left
        return node

    def _replace_node_in_parent(self, node, new_node):
        if node.parent:
            if node == node.parent.left:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        else:
            self.root = new_node
        if new_node:
            new_node.parent = node.parent

    def _delete_node(self, node):
        if node.left and node.right:
            successor = self._minimum(node.right)
            node.full_name = successor.full_name
            node.math = successor.math
            node.informatics = successor.informatics
            node.russian = successor.russian
            node.total_points = successor.total_points
            self.name_to_node[node.full_name] = node
            self._delete_node(successor)
            return

        child = node.left if node.left else node.right
        original_color = node.color
        if child:
            self._replace_node_in_parent(node, child)
            if original_color == BLACK:
                self._fix_deletion(child)
        else:
            self._replace_node_in_parent(node, None)
            if original_color == BLACK:
                self._fix_deletion(node)

    def _fix_deletion(self, node):
        while node != self.root and (node.color == BLACK if node else True):
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling and sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                if (sibling.left is None or sibling.left.color == BLACK) and \
                   (sibling.right is None or sibling.right.color == BLACK):
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.right is None or sibling.right.color == BLACK:
                        if sibling.left:
                            sibling.left.color = BLACK
                        sibling.color = RED
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    if sibling.right:
                        sibling.right.color = BLACK
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling and sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                if (sibling.left is None or sibling.left.color == BLACK) and \
                   (sibling.right is None or sibling.right.color == BLACK):
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.left is None or sibling.left.color == BLACK:
                        if sibling.right:
                            sibling.right.color = BLACK
                        sibling.color = RED
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    if sibling.left:
                        sibling.left.color = BLACK
                    self.right_rotate(node.parent)
                    node = self.root
        if node:
            node.color = BLACK

    def reverse_inorder_traversal(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.reverse_inorder_traversal(node.right, result)
            result.append(node)
            self.reverse_inorder_traversal(node.left, result)
        return result

    def save_sorted_to_file(self, filename='core/pupils.txt'):
        sorted_nodes = self.reverse_inorder_traversal(self.root)
        with open(filename, 'w', encoding='utf-8') as file:
            for index, node in enumerate(sorted_nodes, 1):
                line = (f"{index}) {node.full_name} - Total Points: {node.total_points}, "
                        f"Math: {node.math}, Informatics: {node.informatics}, Russian: {node.russian}\n")
                file.write(line)
