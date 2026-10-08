"""Основная бизнес-логика Task Manager."""

from utils import check_confirm

def create_task(tasks):
    task = input("Введите задачу: ").strip()
    if not task:
        print("Задача не может быть пустой.")
        return
    tasks.append(task)
    print("Задача добавлена.")

def edit_task(tasks):
    if not tasks:
        print("Список задач пуст.")
        return
    number = _read_task_number(tasks, "Введите номер задачи для изменения: ")
    if number is None:
        return
    new_task = input("Введите новую задачу: ").strip()
    if not new_task:
        print("Задача не может быть пустой.")
        return
    tasks[number - 1] = new_task
    print("Задача изменена.")

def delete_task(tasks):
    if not tasks:
        print("Список задач пуст.")
        return
    number = _read_task_number(tasks, "Введите номер задачи для удаления: ")
    if number is None:
        return
    if check_confirm(f"Удалить задачу «{tasks[number - 1]}»? [y/n]: "):
        tasks.pop(number - 1)
        print("Задача удалена.")
    else:
        print("Удаление отменено.")

def _read_task_number(tasks, message):
    try:
        number = int(input(message))
    except ValueError:
        print("Нужно ввести число.")
        return None
    if not 1 <= number <= len(tasks):
        print("Такой задачи нет.")
        return None
    return number
