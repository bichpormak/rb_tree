import graphviz

from src.core.rb_tree import *
from src.core.working_with_json import *
from src.visualization.visualization import *
from src.core.cli import run

def main():
    # try:
    #     pupils = load_data_from_json("visualization/data.json")
    # except FileNotFoundError:
    #     pupils = []
    pupils = []
    rb_tree = RBTree()
    # for pupil in pupils:
    #     rb_tree.insert(pupil[0], pupil[1], pupil[2], pupil[3])
    run(pupils, rb_tree)

    for index, node in enumerate(pupils):
        dot = graphviz.Digraph()
        breadth_first_search(rb_tree.root, dot)
        dot.render('visualization/files_for_visualization/g{}.gv'.format(index))

    save_visualization()

if __name__ == '__main__':
    main()