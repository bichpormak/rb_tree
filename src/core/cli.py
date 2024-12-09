from src.core.rb_tree import *
from src.core.working_with_json import *

def run(pupils: list, rb_tree: RBTree):
    while True:
        choice = input("Enter the number of the operation or input 'help': ").lower()

        if choice in ('help', 'h'):
            print_help()

        elif choice == '1':
            print("Enter  (full name - total points). Press Esc to complete entry.")
            try:
                pupil = input("Enter data: ")

                if pupil.strip() == "":
                    continue
                pupil = pupil.strip().split("-")
                if len(pupil) != 2:
                    print("Invalid format. Please use 'full name - total points'")
                    continue
                pupil[0] = pupil[0].strip()
                pupil[1] = pupil[1].strip()
                try:
                    pupil[1] = int(pupil[1])
                except ValueError:
                    print("Invalid number of points. Please enter an integer.")
            except EOFError:
                continue
            except KeyboardInterrupt:
                continue

            pupils.append(pupil)
            rb_tree.insert(pupil[0], pupil[1])
            rb_tree.save_sorted_to_file('core/pupils.txt')

            save_to_file({
                "full_name": pupil[0],
                "total_points": pupil[1]
            })

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
                with open('core/pupils.txt', 'r', encoding='utf-8') as file:
                    for line in file:
                        print(line, end='')
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