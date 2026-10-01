import os
import time
from multiprocessing import Process


def first_process():
    print(f"Первая функция: процесс запущен, ID = {os.getpid()}")
    time.sleep(1)
    print(f"Первая функция: процесс завершён, ID = {os.getpid()}")


def second_process():
    print(f"Вторая функция: процесс запущен, ID = {os.getpid()}")
    time.sleep(2)
    print(f"Вторая функция: процесс завершён, ID = {os.getpid()}")


def third_process():
    print(f"Третья функция: процесс запущен, ID = {os.getpid()}")
    time.sleep(1)
    print(f"Третья функция: процесс завершён, ID = {os.getpid()}")


def fourth_process():
    print(f"Четвёртая функция: процесс запущен, ID = {os.getpid()}")
    time.sleep(2)
    print(f"Четвёртая функция: процесс завершён, ID = {os.getpid()}")


if __name__ == "__main__":
    process_1 = Process(target=first_process)
    process_2 = Process(target=second_process)
    process_3 = Process(target=third_process)

    print(f"Основной процесс: ID = {os.getpid()}")
    print("Созданы процессы:", process_1, process_2, process_3)

    process_1.start()
    process_2.start()
    process_3.start()

    fourth_process()

    process_1.join()
    process_2.join()
    process_3.join()

    print("Результат работы всех функций выведен в консоль.")
