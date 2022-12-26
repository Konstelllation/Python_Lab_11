#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import jsonschema


def get_student():
    """
    Запросить данные о студенте.
    """
    name = input("Фамилия и инициалы? ")
    number = input("Номер группы? ")
    z = input("Успеваемость: ")

    # Создать словарь.
    return {
        'name': name,
        'number': number,
        'z': z,
    }


def display_students(students):
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if students:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
            )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('number', ''),
                    student.get('z', 0)
                )
            )
        print(line)

    else:
        print("Список студентов пуст")


def select_students(undergraduates):
    """
    Выбрать cтудентов с оценкой 2.
    """
    # Сформировать список студентов.
    result = []
    for pupil in undergraduates:
        if "2" in pupil.get('z', ''):
            result.append(pupil)
    # Возвратить список выбранных студентов.
    return result


def save_students(file_name, undergraduates):
    """
    Сохранить всех студентов в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установить ensure_ascii=False
        json.dump(undergraduates, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузить всех студентов из файла JSON.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "$id": "http://example.com/example.json",
        "type": "array",
        "default": [],
        "title": "Root Schema",
        "items": {
            "type": "object",
            "title": "A Schema",
            "required": [
                "name",
                "number",
                "z"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "title": "The name Schema",
                    "examples": [
                        "Горшков В.И.",
                        "Харченко Б.Р."
                    ]
                },
                "number": {
                    "type": "string",
                    "title": "The number Schema",
                    "examples": [
                        "1",
                        "2"
                    ]
                },
                "z": {
                    "type": "string",
                    "title": "The z Schema",
                    "examples": [
                        "2 3 4 5 5",
                        "5 4 5 4 3"
                    ]
                }
            },
            "examples": [{
                "name": "Горшков В.И.",
                "number": "1",
                "z": "2 3 4 5 5"
            },
                {
                    "name": "Харченко Б.Р.",
                    "number": "2",
                    "z": "5 4 5 4 3"
                }]
        },
        "examples": [
            [{
                "name": "Горшков В.И.",
                "number": "1",
                "z": "2 3 4 5 5"
            },
                {
                    "name": "Харченко Б.Р.",
                    "number": "2",
                    "z": "5 4 5 4 3"
                }]
        ]
    }
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", list(validator.iter_errors(loadfile)))
            exit()
    return loadfile


def main():
    """
    Главная функция программы.
    """
    # Список студентов.
    students = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == "exit":
            break

        elif command == "add":
            # Запросить данные о работнике.
            student = get_student()

            # Добавить словарь в список.
            students.append(student)
            # Отсортировать список в случае необходимости.
            if len(students) > 1:
                students.sort(key=lambda item: item.get('name', ''))

        elif command == "list":
            # Отобразить всех студентов.
            display_students(students)

        elif command == "select":
            # Выбрать работников с заданным стажем.
            selected = select_students(students)
            # Отобразить выбранных работников.
            display_students(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]


# Сохранить данные в файл с заданным именем.
            save_students(file_name, students)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            students = load_students(file_name)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить студента;")
            print("list - вывести список студентов;")
            print("select - запросить студентов с оценкой 2;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()