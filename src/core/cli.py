from src.core.rb_tree import *
from src.core.working_with_json import *

def run(pupils: list, rb_tree: RBTree):
    while True:
        choice = input("Enter the number of the operation or input 'help': ").lower()

        if choice in ('help', 'h'):
            print_help()

        elif choice == '1':
            try:
                full_name = input("Enter full name: ")
                math_score = int(input("Enter Math score: "))
                cs_score = int(input("Enter CS score: "))
                rus_score = int(input("Enter Russian score: "))
                pupils.append((full_name, math_score, cs_score, rus_score))
                rb_tree.insert(full_name, math_score, cs_score, rus_score)
                rb_tree.save_sorted_to_file('core/pupils.txt')

                save_to_file({
                    "full_name": full_name,
                    "math_score": math_score,
                    "cs_score": cs_score,
                    "rus_score": rus_score
                })
            except ValueError:
                print("Invalid input. Please enter numbers for scores.")

        elif choice == '2':
            full_name = input("Enter full name: ")
            rb_tree.delete_by_name(full_name)
            rb_tree.save_sorted_to_file('core/pupils.txt')
            remove_from_file(full_name, 'visualization/data.json')

        elif choice == '3':
            full_name = input("Enter the fullname to search: ")
            information = rb_tree.search_by_name(full_name)
            if information is None:
                print("The full name entered does not exist.")
            else:
                print(f"{information.full_name} - total points: {information.key}")

        elif choice == '4':
            try:
                rb_tree.save_sorted_to_file('core/pupils.txt')
                sorted_nodes = rb_tree.reverse_inorder_traversal(rb_tree.root)
                for index, node in enumerate(sorted_nodes, start=1):
                    print(
                        f"{index}) {node.full_name} - Total: {node.total_score} (Math: {node.math_score}, CS: {node.cs_score}, Russian: {node.rus_score})")
            except FileNotFoundError:
                print("The path entered does not exist.")

        elif choice == '5':
            print("Program completed )")
            break

        else:
            print("Invalid input...")
            print_help()



def print_help():
    print("1. Add pupils")
    print("2. Delete pupils")
    print("3. Search pupil")
    print("4. Display all students in sorted order")
    print("5. Exit")