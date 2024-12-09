import os
import json

def save_to_file(data, filename='visualization/data.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def remove_from_file(full_name, filename='visualization/data.json'):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"File {filename} is empty or contains wrong format JSON")
            return

    updated_data = [pupil for pupil in data if pupil.get("full_name", "").lower() != full_name.lower()]

    if len(updated_data) == len(data):
        print(f"Node with name '{full_name}' is not found in the file.")
        return

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)

    print(f"Node with name '{full_name}' successfully deleted from the file")


def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    extracted_data = [[entry["full_name"], entry["total_points"]] for entry in data]

    return extracted_data