from PyPDF2 import PdfMerger
import glob


def breadth_first_search(root, dot):
    queue = [root]
    dot.node(str(root.key), color=root.color)
    while queue:
        tmp_queue = []
        for element in queue:
            if element.left:
                dot.node(str(element.left.key), color=element.left.color)
                dot.edge(str(element.key), str(element.left.key))
                tmp_queue.append(element.left)
            if element.right:
                dot.node(str(element.right.key), color=element.right.color)
                dot.edge(str(element.key), str(element.right.key))
                tmp_queue.append(element.right)
        queue = tmp_queue


def save_visualization():
    merger = PdfMerger()
    pdf_files = sorted(glob.glob("visualization/files_for_visualization/*.pdf"))

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write("visualization/visualization.pdf")
    merger.close()
