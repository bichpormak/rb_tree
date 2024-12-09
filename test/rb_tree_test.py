import pytest
import os
from src.core.rb_tree import *


@pytest.fixture
def empty_tree():
    return RBTree()


@pytest.fixture
def populated_tree():
    tree = RBTree()
    nodes = [
        ("Alice Smith", 10),
        ("Bob Johnson", 20),
        ("Charlie Lee", 15),
        ("Diana King", 25),
        ("Evan Young", 5),
    ]
    for full_name, key in nodes:
        tree.insert(full_name, key)
    return tree


def test_insert_empty_tree(empty_tree):
    empty_tree.insert("Root Node", 100)
    assert empty_tree.root is not None
    assert empty_tree.root.key == 100
    assert empty_tree.root.color == BLACK
    assert empty_tree.root.full_name == "Root Node"


def test_insert_left_child(populated_tree):
    populated_tree.insert("Frank Moore", 2)
    node = populated_tree.search_by_name("Frank Moore")
    assert node is not None
    assert node.key == 2


def test_insert_right_child(populated_tree):
    populated_tree.insert("Grace Hall", 30)
    node = populated_tree.search_by_name("Grace Hall")
    assert node is not None
    assert node.key == 30
    assert node.color == RED



def test_search_existing_name(populated_tree):
    node = populated_tree.search_by_name("Charlie Lee")
    assert node is not None
    assert node.key == 15


def test_search_non_existing_name(populated_tree):
    node = populated_tree.search_by_name("Non Existent")
    assert node is None


def test_delete_leaf_node(populated_tree):
    populated_tree.delete_by_name("Evan Young")
    node = populated_tree.search_by_name("Evan Young")
    assert node is None


def test_delete_node_with_one_child(populated_tree):
    populated_tree.insert("Ivy Scott", 8)
    populated_tree.delete_by_name("Evan Young")
    node_ev = populated_tree.search_by_name("Evan Young")
    assert node_ev is None
    node_ivy = populated_tree.search_by_name("Ivy Scott")
    assert node_ivy is not None


def test_delete_node_with_two_children(populated_tree):
    populated_tree.delete_by_name("Alice Smith")
    node_alice = populated_tree.search_by_name("Alice Smith")
    assert node_alice is None
    node_charlie = populated_tree.search_by_name("Charlie Lee")
    assert node_charlie is not None


def test_delete_root_node(populated_tree):
    populated_tree.delete_by_name("Alice Smith")
    node = populated_tree.search_by_name("Alice Smith")
    assert node is None
    assert populated_tree.root is not None
    assert populated_tree.root.color == BLACK


def test_delete_from_empty_tree(empty_tree):
    empty_tree.delete_by_name("Any Name")
    assert empty_tree.root is None


def test_reverse_inorder_traversal(populated_tree):
    sorted_nodes = populated_tree.reverse_inorder_traversal(populated_tree.root)
    keys = [n.key for n in sorted_nodes]
    assert keys == sorted(keys, reverse=True)


def test_save_sorted_to_file(populated_tree, tmp_path):
    file_path = tmp_path / "pupils.txt"
    populated_tree.save_sorted_to_file(str(file_path))
    assert os.path.exists(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    assert len(lines) == 5
    keys_in_file = [int(line.split(' - ')[1]) for line in lines]
    assert keys_in_file == sorted(keys_in_file, reverse=True)


def test_left_rotate():
    tree = RBTree()
    tree.insert("Root", 10)
    tree.insert("Right", 20)
    root = tree.root
    tree.left_rotate(root)
    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.left.left is None
    assert tree.root.left.right is None


def test_right_rotate():
    tree = RBTree()
    tree.insert("Root", 20)
    tree.insert("Left", 10)
    root = tree.root
    tree.right_rotate(root)
    assert tree.root.key == 10
    assert tree.root.right.key == 20
    assert tree.root.right.right is None
    assert tree.root.right.left is None


def test_fix_tree_after_insert(populated_tree):
    populated_tree.insert("Jack White", 17)

    def check_red_properties(node):
        if node is None:
            return True
        if node.color == RED:
            if (node.left and node.left.color == RED) or (node.right and node.right.color == RED):
                return False
        return check_red_properties(node.left) and check_red_properties(node.right)

    assert check_red_properties(populated_tree.root)
