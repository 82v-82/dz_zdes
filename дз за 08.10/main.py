"""Точка входа в Task Manager версии 0.1.0."""

from core import create_task, delete_task, edit_task
from storage import load_tasks, save_tasks
from view import show_menu, show_tasks

def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()
        match choice:
            case "1": create_task(tasks)
            case "2": show_tasks(tasks)
            case "3": edit_task(tasks)
            case "4": delete_task(tasks)
            case "5": save_tasks(tasks)
            case "0":
                save_tasks(tasks)
                print("Программа завершена.")
                break
            case _: print("Неверный выбор.")

if __name__ == "__main__":
    main()
