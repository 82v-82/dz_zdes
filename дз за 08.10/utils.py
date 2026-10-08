"""Вспомогательные функции приложения."""

def check_confirm(message="Подтвердить действие? [y/n]: "):
    """Запрашивает подтверждение и возвращает True/False."""
    while True:
        answer = input(message).strip().lower()
        if answer in ("y", "yes", "д", "да"):
            return True
        if answer in ("n", "no", "н", "нет"):
            return False
        print("Введите y/д для подтверждения или n/н для отмены.")
