"""Функции отображения Task Manager."""

def show_menu():
    print("\n--- TASK MANAGER v0.1.0 ---")
    print("1 - Добавить задачу")
    print("2 - Показать задачи")
    print("3 - Изменить задачу")
    print("4 - Удалить задачу")
    print("5 - Сохранить задачи")
    print("0 - Выход")

def show_tasks(tasks):
    if not tasks:
        print("Список задач пуст")
        return
    print("\nСписок задач:")
    for index, task in enumerate(tasks, start=1):
        print(f"{index} - {task}")

def show_message(message):
    print(message)
