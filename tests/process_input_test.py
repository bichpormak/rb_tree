import pytest
from io import StringIO
from unittest.mock import patch
from threading import Thread
import time
from src.core.process_input import *  # Здесь замените на путь до вашего кода

@pytest.fixture
def capture_stdout():
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        yield mock_stdout

# Тестирование корректного ввода
def test_valid_input(capture_stdout):
    with patch("builtins.input", return_value="John Doe - 95"):
        result = get_information()
        assert result == ["John Doe", 95]
        assert capture_stdout.getvalue() == ""

# Тестирование пустой строки
def test_empty_input(capture_stdout):
    with patch("builtins.input", return_value=""):
        result = get_information()
        assert result is None
        assert "Enter data:" in capture_stdout.getvalue()

# Тестирование неправильного формата
def test_invalid_format(capture_stdout):
    with patch("builtins.input", return_value="John Doe 95"):
        result = get_information()
        assert result is None
        assert "Invalid format. Please use 'full name - total points'" in capture_stdout.getvalue()

# Тестирование неправильных баллов (нечисловое значение)
def test_invalid_points(capture_stdout):
    with patch("builtins.input", return_value="John Doe - abc"):
        result = get_information()
        assert result is None
        assert "Invalid number of points. Please enter an integer." in capture_stdout.getvalue()

# Тестирование корректного ввода с завершением программы после нажатия ESC
def test_valid_input_then_escape(capture_stdout):
    # Создадим поток для имитации нажатия клавиши ESC
    def mock_input():
        time.sleep(0.1)  # имитация времени для того, чтобы программа успела запросить ввод
        stop_event.set()  # имитируем нажатие ESC, которое завершает программу
        return "John Doe - 95"  # возвращаем корректные данные

    # Запускаем в отдельном потоке, чтобы имитировать взаимодействие с пользователем
    with patch("builtins.input", side_effect=mock_input):
        thread = Thread(target=get_information)
        thread.start()
        thread.join()  # ждем завершения потока

    # Проверяем, что программа завершилась корректно
    assert capture_stdout.getvalue().strip().endswith("Completing data entry...")
    assert stop_event.is_set()

# Тест на завершение с клавишей ESC, используя мок для Listener
def test_esc_key_to_stop(capture_stdout):
    stop_event.clear()

    # Используем mock для Listener, чтобы завершить выполнение
    with patch("pynput.keyboard.Listener") as mock_listener:
        # Настроим mock, чтобы сразу вернуть False (это как нажатие клавиши ESC)
        mock_listener.return_value = None
        start_listener()

    assert stop_event.is_set()  # Проверяем, что stop_event был установлен
