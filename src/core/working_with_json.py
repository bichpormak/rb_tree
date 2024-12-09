# src/core/working_with_json.py

import json
import os

def save_to_file(pupil_data, filename='visualization/data.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    data.append(pupil_data)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def remove_from_file(full_name, filename='visualization/data.json'):
    if not os.path.exists(filename):
        print(f"Файл {filename} не существует.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data = [pupil for pupil in data if pupil['full_name'] != full_name]

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    extracted_data = [[entry["full_name"], entry["total_points"]] for entry in data]

    return extracted_data