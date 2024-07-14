import os
import logging
from collections import namedtuple
from argparse import ArgumentParser

# Определение namedtuple для хранения информации о файлах и каталогах
FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_dir', 'parent'])

def get_directory_contents(directory):
    """
    Функция для получения содержимого директории.

    Args:
    - directory (str): Путь до директории, содержимое которой нужно получить.

    Returns:
    - list: Список объектов namedtuple FileInfo, содержащих информацию о файлах и каталогах.
    """
    contents = []

    # Рекурсивно обходим директорию
    for root, dirs, files in os.walk(directory):
        parent_dir = os.path.basename(root)  # Получаем имя родительской директории

        # Обрабатываем файлы в текущей директории
        for name in files:
            file_name, extension = os.path.splitext(name)
            # Добавляем информацию о файле в список contents
            contents.append(FileInfo(name=file_name, extension=extension, is_dir=False, parent=parent_dir))
            # Логируем информацию о файле
            logging.info(f'File - Name: {file_name}, Extension: {extension}, Parent: {parent_dir}')

        # Обрабатываем поддиректории в текущей директории
        for name in dirs:
            # Добавляем информацию о директории в список contents
            contents.append(FileInfo(name=name, extension='', is_dir=True, parent=parent_dir))
            # Логируем информацию о директории
            logging.info(f'Directory - Name: {name}, Parent: {parent_dir}')

    return contents

def main():
    # Настройка парсера аргументов командной строки
    parser = ArgumentParser(description='Process directory path.')
    parser.add_argument('directory', type=str, help='Path to the directory')
    args = parser.parse_args()

    # Получаем путь до директории из аргументов командной строки
    directory = args.directory

    # Проверяем, является ли указанный путь действительной директорией
    if not os.path.isdir(directory):
        print(f"The path {directory} is not a valid directory.")
        return

    # Настройка логирования для записи в файл text.txt
    logging.basicConfig(filename='task15_6.txt', level=logging.INFO, format='%(message)s', encoding='utf-8')

    # Получаем содержимое директории
    contents = get_directory_contents(directory)

    # Выводим содержимое на экран
    for item in contents:
        print(item)

if __name__ == '__main__':
    main()
