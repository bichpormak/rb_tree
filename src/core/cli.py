from src.core.rb_tree import RBTree
from src.core.working_with_json import save_to_file, remove_from_file

def run(pupils: list, rb_tree: RBTree):
    while True:
        choice = input("Enter the operation number or 'help': ").lower()

        if choice in ('help', 'h'):
            print_help()

        elif choice == '1':
            print("Enter the data in the following format:")
            print("Full Name")
            try:
                full_name = input("Enter Full Name: ").strip()
                if not full_name:
                    print("Full Name cannot be empty.")
                    continue

                math_input = input("Enter Math score: ").strip()
                informatics_input = input("Enter Informatics score: ").strip()
                russian_input = input("Enter Russian language score: ").strip()

                try:
                    math_score = int(math_input)
                    informatics_score = int(informatics_input)
                    russian_score = int(russian_input)
                except ValueError:
                    print("Scores must be integers.")
                    continue

                if any(score < 0 for score in [math_score, informatics_score, russian_score]):
                    print("Scores cannot be negative.")
                    continue

                # Add to tree and list
                rb_tree.insert(full_name, math_score, informatics_score, russian_score)
                rb_tree.save_sorted_to_file('core/pupils.txt')

                pupil_data = {
                    "full_name": full_name,
                    "math": math_score,
                    "informatics": informatics_score,
                    "russian": russian_score,
                    "total_points": math_score + informatics_score + russian_score
                }
                pupils.append(pupil_data)
                save_to_file(pupil_data)

                print(f"Student {full_name} successfully added.")

            except EOFError:
                continue
            except KeyboardInterrupt:
                continue

        elif choice == '2':
            full_name = input("Enter the Full Name of the student to delete: ").strip()
            if not full_name:
                print("Full Name cannot be empty.")
                continue

            if rb_tree.search_by_name(full_name) is None:
                print("Student with such a Full Name not found.")
                continue

            rb_tree.delete_by_name(full_name)
            rb_tree.save_sorted_to_file('core/pupils.txt')
            remove_from_file(full_name, 'visualization/data.json')

            # Remove from list
            pupils[:] = [pupil for pupil in pupils if pupil['full_name'] != full_name]

            print(f"Student {full_name} successfully deleted.")

        elif choice == '3':
            full_name = input("Enter the Full Name of the student to search for: ").strip()
            if not full_name:
                print("Full Name cannot be empty.")
                continue

            node = rb_tree.search_by_name(full_name)
            if node is None:
                print("Student with such a Full Name not found.")
            else:
                print(f"{node.full_name} - Total points: {node.total_points}, "
                      f"Math: {node.math}, Informatics: {node.informatics}, Russian: {node.russian}")

        elif choice == '4':
            try:
                rb_tree.save_sorted_to_file('core/pupils.txt')
                with open('core/pupils.txt', 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(content)
            except FileNotFoundError:
                print("The file with students was not found.")

        elif choice == '5':
            print("Program terminated.")
            break

        else:
            print("Invalid input...")
            print_help()


def print_help():
    print("Available operations:")
    print("1. Add a student")
    print("2. Delete a student")
    print("3. Search for a student")
    print("4. Display all students in sorted order")
    print("5. Exit")
