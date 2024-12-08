import threading
from pynput.keyboard import Key, Listener

stop_event = threading.Event()

def get_information():
    while not stop_event.is_set():
        try:
            input_str = input("Enter data: ")
            if stop_event.is_set():
                break
            if input_str.strip() == "":
                continue
            information_about_pupil = input_str.strip().split("-")
            if len(information_about_pupil) != 2:
                print("Invalid format. Please use 'full name - total points'")
                continue
            full_name = information_about_pupil[0].strip()
            total_points_str = information_about_pupil[1].strip()
            try:
                total_points = int(total_points_str)
                return [full_name, total_points]
            except ValueError:
                print("Invalid number of points. Please enter an integer.")
        except EOFError:
            break
        except KeyboardInterrupt:
            break
    return None

def on_press(key):
    pass

def on_release(key):
    if key == Key.esc:
        print("\nCompleting data entry...")
        stop_event.set()
        return False

def start_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()