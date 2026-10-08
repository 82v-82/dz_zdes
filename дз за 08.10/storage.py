"""Сохранение и загрузка задач из файла."""

FILE_NAME = "tasks.txt"

def save_tasks(tasks, filename=FILE_NAME):
    """Сохраняет список задач в текстовый файл."""
    with open(filename, "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")
    print("Задачи сохранены.")

def load_tasks(filename=FILE_NAME):
    """Загружает задачи из файла. Если файла нет, возвращает пустой список."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []
