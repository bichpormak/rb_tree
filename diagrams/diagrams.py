import time
import matplotlib.pyplot as plt
import random
import io
from contextlib import redirect_stdout
from src.core.rb_tree import *


def measure_time(func, *args, **kwargs):
    start_time = time.perf_counter()
    func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time


def plot_performance(operation, size, times, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(times) + 1), times, marker='o', linestyle='-', color='blue')
    plt.xlabel("Номер операции")
    plt.ylabel("Время (сек.)")
    plt.title(f"Производительность операции '{operation}' для {size} элементов")
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.savefig(filename)
    print(f"График '{operation}' для размера {size} сохранён как '{filename}'.")
    plt.close()


def generate_balanced_order(elements):
    if not elements:
        return []
    mid = len(elements) // 2
    return [elements[mid]] + generate_balanced_order(elements[:mid]) + generate_balanced_order(elements[mid + 1:])


def run_insertions(tree, data_order):
    insert_times = []
    for key in data_order:
        full_name = f"Pupil_{key}"
        time_taken = measure_time(tree.insert, full_name, key)
        insert_times.append(time_taken)
    return insert_times


def run_deletions(tree, data_order):
    delete_times = []
    for key in data_order:
        full_name = f"Pupil_{key}"
        time_taken = measure_time(tree.delete_by_name, full_name)
        delete_times.append(time_taken)
    return delete_times


def run_search_existing(tree, data_order):
    search_existing_times = []
    for key in data_order:
        full_name = f"Pupil_{key}"
        time_taken = measure_time(tree.search_by_name, full_name)
        search_existing_times.append(time_taken)
    return search_existing_times


def run_search_nonexistent(tree, data_order):
    search_nonexistent_times = []
    for key in data_order:
        full_name = f"NonExistent_{key}"
        time_taken = measure_time(tree.search_by_name, full_name)
        search_nonexistent_times.append(time_taken)
    return search_nonexistent_times


def run_sorting(tree, filename):
    sort_time = measure_time(tree.save_sorted_to_file, filename)
    return sort_time


def rb_tree():
    data_sizes = [10, 1000, 100000]

    for size in data_sizes:
        print(f"\n=== Тестирование для размера данных: {size} ===")

        data = list(range(1, size + 1))

        if size == 10:
            data_order = generate_balanced_order(data)
        elif size == 1000:
            data_order = data.copy()
            random.shuffle(data_order)
        else:
            data_order = list(range(size, 0, -1))

        tree = RBTree()

        print("Выполняется вставка...")
        insert_times = run_insertions(tree, data_order)
        plot_performance(
            operation='Вставка',
            size=size,
            times=insert_times,
            filename=f"performance_insert_size_{size}.png"
        )
        avg_insert = sum(insert_times) / len(insert_times)
        print(f"Среднее время вставки: {avg_insert:.6f} секунд")

        print("Выполняется удаление...")
        delete_times = run_deletions(tree, data_order)
        plot_performance(
            operation='Удаление',
            size=size,
            times=delete_times,
            filename=f"performance_delete_size_{size}.png"
        )
        avg_delete = sum(delete_times) / len(delete_times)
        print(f"Среднее время удаления: {avg_delete:.6f} секунд")

        print("Восстанавливается дерево для операций поиска...")
        tree = RBTree()
        for key in data_order:
            full_name = f"Pupil_{key}"
            tree.insert(full_name, key)

        print("Выполняется поиск существующих элементов...")
        search_existing_times = run_search_existing(tree, data_order)
        plot_performance(
            operation='Поиск существующих',
            size=size,
            times=search_existing_times,
            filename=f"performance_search_existing_size_{size}.png"
        )
        avg_search_existing = sum(search_existing_times) / len(search_existing_times)
        print(f"Среднее время поиска существующих элементов: {avg_search_existing:.6f} секунд")

        print("Выполняется поиск несуществующих элементов...")
        search_nonexistent_times = run_search_nonexistent(tree, data_order)
        plot_performance(
            operation='Поиск несуществующих',
            size=size,
            times=search_nonexistent_times,
            filename=f"performance_search_nonexistent_size_{size}.png"
        )
        avg_search_nonexistent = sum(search_nonexistent_times) / len(search_nonexistent_times)
        print(f"Среднее время поиска несуществующих элементов: {avg_search_nonexistent:.6f} секунд")

        print("Выполняется сортировка (сохранение в файл)...")
        sort_filename = f"sorted_pupils_size_{size}.txt"
        sort_time = run_sorting(tree, sort_filename)
        plot_performance(
            operation='Сортировка',
            size=size,
            times=[sort_time],
            filename=f"performance_sort_size_{size}.png"
        )
        print(f"Время сортировки: {sort_time:.6f} секунд")

        print(f"\n--- Средние значения времени для размера данных {size} ---")
        print(f"Среднее время вставки: {avg_insert:.6f} секунд")
        print(f"Среднее время удаления: {avg_delete:.6f} секунд")
        print(f"Среднее время поиска существующих элементов: {avg_search_existing:.6f} секунд")
        print(f"Среднее время поиска несуществующих элементов: {avg_search_nonexistent:.6f} секунд")
        print(f"Время сортировки: {sort_time:.6f} секунд")
        print("Тестирование для данного размера данных завершено.")


if __name__ == "__main__":
    rb_tree()
