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
        return 'key: {}, left: {}, right: {}, color: {}, parent: {}'.format(self.key, left, right, self.color, parent)


class RBTree:
    def __init__(self):
        self.root = None

    def insert(self, full_name, key):
        if not self.root:
            self.root = Node(full_name, key, BLACK)

        else:
            current = self.root
            while current:
                if key < current.key:
                    if not current.left:
                        new_node = Node(full_name, key, RED, parent = current)
                        current.left = new_node
                        break

                    current = current.left

                else:
                    if not current.right:
                        new_node = Node(full_name, key, RED, parent = current)
                        current.right = new_node
                        break

                    current = current.right

            self.fix_tree(new_node)


    def fix_tree(self, node):

        while node.parent and node.parent.color == RED:
            grandparent = node.parent.parent
            if node.parent == grandparent.left:
                uncle = grandparent.right

                if not uncle or uncle.color == BLACK:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    self.right_rotate(node)
                    node.parent.color = BLACK
                    grandparent.color = RED

                else:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    grandparent.color = RED


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
        parent = node.parent

        node.right = new_node.left
        if node.right:
            node.right.parent = node

        new_node.left = node
        node.parent = new_node

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

        node.left = new_node.right
        if node.left:
            node.left.parent = node

        new_node.right = node
        node.parent = new_node

        if not parent:
            self.root = new_node

        else:
            if parent.left == node:
                parent.left = new_node
            else:
                parent.right = new_node

    def search_by_name(self, full_name):
        full_name_lower = full_name.lower()

        def _search(node):
            if node is None:
                return None
            # Проверяем текущий узел
            if node.full_name.lower() == full_name_lower:
                return node
            # Рекурсивно ищем в левом поддереве
            left_result = _search(node.left)
            if left_result:
                return left_result
            # Рекурсивно ищем в правом поддереве
            return _search(node.right)

        return _search(self.root)


    def reverse_inorder_traversal(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.reverse_inorder_traversal(node.right, result)
            result.append(node)
            self.reverse_inorder_traversal(node.left, result)
        return result

    def delete_by_name(self, full_name):
        node_to_delete = self.search_by_name(full_name)
        if node_to_delete:
            self._delete_node(node_to_delete)

    def _minimum(self, node):
        # Находим узел с минимальным ключом в поддереве node
        while node.left:
            node = node.left
        return node

    def _replace_node_in_parent(self, node, new_node):
        # Заменяет node на new_node у родителя
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
        # Классический алгоритм удаления из КЧ-дерева
        # Если у удаляемого узла два потомка, меняем его на преемника
        if node.left and node.right:
            successor = self._minimum(node.right)
            # Переносим данные преемника в удаляемый узел
            node.key = successor.key
            node.full_name = successor.full_name
            node = successor

        # Теперь node имеет не более одного ребенка
        child = node.right if node.right else node.left

        original_color = node.color
        if child:
            self._replace_node_in_parent(node, child)
            if node.color == BLACK:
                self._fix_deletion(child)
        else:
            # Нет детей
            if node.color == BLACK:
                self._fix_deletion(node)
            self._replace_node_in_parent(node, None)

    def _fix_deletion(self, node):
        # Восстанавливаем свойства КЧ-дерева после удаления
        # node может быть "пустой" узел (виртуальный), используем проверку node != self.root
        while node != self.root and (not node or node.color == BLACK):
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling and sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                if (not sibling.left or sibling.left.color == BLACK) and (
                        not sibling.right or sibling.right.color == BLACK):
                    if sibling:
                        sibling.color = RED
                    node = node.parent
                else:
                    if not sibling.right or sibling.right.color == BLACK:
                        if sibling.left:
                            sibling.left.color = BLACK
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
                if (not sibling.left or sibling.left.color == BLACK) and (
                        not sibling.right or sibling.right.color == BLACK):
                    if sibling:
                        sibling.color = RED
                    node = node.parent
                else:
                    if not sibling.left or sibling.left.color == BLACK:
                        if sibling.right:
                            sibling.right.color = BLACK
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