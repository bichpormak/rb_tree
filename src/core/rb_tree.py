import json
import os

BLACK = 'black'
RED = 'red'


class Node:
    def __init__(self, full_name, key, color, parent=None):
        self.key = key
        self.full_name = full_name
        self.left = None
        self.right = None
        self.color = color
        self.parent = parent

    def __str__(self):
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        parent = self.parent.key if self.parent else None
        return 'key: {}, left: {}, right: {}, color: {}, parent: {}'.format(
            self.key, left, right, self.color, parent)


class RBTree:
    def __init__(self):
        self.root = None
        self.name_to_key = {}

    def insert(self, full_name, key):
        if not self.root:
            self.root = Node(full_name, key, BLACK)

        else:
            current = self.root
            while True:
                if key < current.key:
                    if not current.left:
                        new_node = Node(full_name, key, RED, parent=current)
                        current.left = new_node
                        break
                    current = current.left
                else:
                    if not current.right:
                        new_node = Node(full_name, key, RED, parent=current)
                        current.right = new_node
                        break
                    current = current.right

            self.fix_tree(new_node)

        self.name_to_key[full_name] = key

    def fix_tree(self, node):
        while node.parent and node.parent.color == RED:
            grandparent = node.parent.parent
            if node.parent == grandparent.left:
                uncle = grandparent.right

                if uncle and uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
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

        if self.root and self.root.color == RED:
            self.root.color = BLACK

    def left_rotate(self, node):
        new_node = node.right
        parent = node.parent

        if new_node is None:
            return

        node.right = new_node.left
        if node.right:
            node.right.parent = node

        new_node.left = node
        node.parent = new_node
        new_node.parent = parent  # Устанавливаем родителя для нового узла

        if not parent:
            self.root = new_node
        else:
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node

    def right_rotate(self, node):
        new_node = node.left
        parent = node.parent

        if new_node is None:
            return

        node.left = new_node.right
        if node.left:
            node.left.parent = node

        new_node.right = node
        node.parent = new_node
        new_node.parent = parent  # Устанавливаем родителя для нового узла

        if not parent:
            self.root = new_node
        else:
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node

    def search_by_key(self, key):
        current = self.root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        return None

    def search_by_name(self, full_name):
        key = self.name_to_key.get(full_name)
        if key is not None:
            return self.search_by_key(key)
        return None

    def reverse_inorder_traversal(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.reverse_inorder_traversal(node.right, result)
            result.append(node)
            self.reverse_inorder_traversal(node.left, result)
        return result

    def delete_by_name(self, full_name):
        key = self.name_to_key.get(full_name)
        if key is not None:
            self._delete_node_by_key(key)
            del self.name_to_key[full_name]

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

    def _delete_node_by_key(self, key):
        node = self.search_by_key(key)
        if node:
            self._delete_node(node)

    def _delete_node(self, node):
        if node.left and node.right:
            successor = self._minimum(node.right)
            node.key = successor.key
            node.full_name = successor.full_name
            self.name_to_key[node.full_name] = node.key
            node = successor

        child = node.right if node.right else node.left
        original_color = node.color
        if child:
            self._replace_node_in_parent(node, child)
            if original_color == BLACK:
                self._fix_deletion(child)
        else:
            if original_color == BLACK:
                self._fix_deletion(node)
            self._replace_node_in_parent(node, None)

    def _fix_deletion(self, node):
        while node != self.root and (node is None or node.color == BLACK):
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling and sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                if ((sibling.left is None or sibling.left.color == BLACK) and
                        (sibling.right is None or sibling.right.color == BLACK)):
                    if sibling:
                        sibling.color = RED
                    node = node.parent
                else:
                    if sibling.right is None or sibling.right.color == BLACK:
                        if sibling.left:
                            sibling.left.color = BLACK
                        if sibling:
                            sibling.color = RED
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    if sibling:
                        sibling.color = node.parent.color
                    node.parent.color = BLACK
                    if sibling and sibling.right:
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
                if ((sibling.left is None or sibling.left.color == BLACK) and
                        (sibling.right is None or sibling.right.color == BLACK)):
                    if sibling:
                        sibling.color = RED
                    node = node.parent
                else:
                    if sibling.left is None or sibling.left.color == BLACK:
                        if sibling.right:
                            sibling.right.color = BLACK
                        if sibling:
                            sibling.color = RED
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    if sibling:
                        sibling.color = node.parent.color
                    node.parent.color = BLACK
                    if sibling and sibling.left:
                        sibling.left.color = BLACK
                    self.right_rotate(node.parent)
                    node = self.root
        if node:
            node.color = BLACK

    def save_sorted_to_file(self, filename='core/pupils.txt'):
        sorted_nodes = self.reverse_inorder_traversal(self.root)
        with open(filename, 'w', encoding='utf-8') as file:
            index = 1
            for node in sorted_nodes:
                line = f"{index}) {node.full_name} - {node.key}\n"
                file.write(line)
                index += 1