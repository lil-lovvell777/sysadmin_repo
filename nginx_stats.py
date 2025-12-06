#!/usr/bin/env python3
"""
Скрипт для обработки лога веб-сервера nginx и подсчёта статистики обращений.

Формат вывода в файл статистики:
    IP: OS: count
например:
    188.41.16.190: Windows: 10
"""

import sys
import argparse
from collections import Counter


def detect_os(user_agent: str) -> str:
    """
    Примитивное определение ОС по User-Agent.
    Этого достаточно для учебного задания.
    """
    ua = (user_agent or "").lower()

    if "windows" in ua:
        return "Windows"
    if "macintosh" in ua or "mac os" in ua:
        return "Macintosh"
    if "linux" in ua or "x11" in ua:
        return "Linux"

    return "Other"


def parse_log_line(line: str):
    """
    Парсит строку лога nginx.
    Возвращает (ip, user_agent) или (None, None), если строка мусорная.

    Пример строки:
    128.148.46.126 - - [20/Jun/2024:12:56:06 +0300] "GET /something HTTP/1.1" 200 1359 "-" "User-Agent..."
    """
    line = line.strip()
    if not line:
        return None, None

    parts = line.split()
    if len(parts) < 1:
        return None, None

    ip = parts[0]

    # User-Agent обычно — последнее поле в кавычках
    user_agent = ""
    if '"' in line:
        quoted_parts = line.split('"')
        if len(quoted_parts) >= 2:
            # Обычно схема такая:
            # 0: префикс
            # 1: запрос ("GET ...")
            # 2: префикс
            # 3: реферер
            # 4: префикс
            # 5: User-Agent
            # поэтому берём предпоследний элемент
            user_agent = quoted_parts[-2].strip()

    return ip, user_agent


def process_log(input_path: str):
    """
    Читает лог-файл построчно и возвращает Counter с ключами (ip, os).
    """
    stats = Counter()

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            ip, ua = parse_log_line(line)
            if not ip:
                continue

            os_name = detect_os(ua)
            stats[(ip, os_name)] += 1

    return stats


def write_stats(output_path: str, stats: Counter):
    """
    Записывает статистику в файл в формате:
        IP: OS: count

    Сортируем по IP, затем по названию ОС.
    """
    with open(output_path, "w", encoding="utf-8") as out:
        for (ip, os_name), count in sorted(
            stats.items(), key=lambda x: (x[0][0], x[0][1])
        ):
            out.write(f"{ip}: {os_name}: {count}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для подсчёта статистики обращений по логам nginx."
    )
    parser.add_argument("input_log", help="Путь к лог-файлу nginx (например, nginx.log)")
    parser.add_argument(
        "output_txt", help="Путь к выходному TXT-файлу со статистикой"
    )

    args = parser.parse_args()

    stats = process_log(args.input_log)
    write_stats(args.output_txt, stats)


if __name__ == "__main__":
    # Если запуск через python3 nginx_stats.py nginx.log stats.txt
    # — сюда и попадём.
    if len(sys.argv) == 1:
        print("Использование: python3 nginx_stats.py nginx.log stats.txt")
        sys.exit(1)

    main()
