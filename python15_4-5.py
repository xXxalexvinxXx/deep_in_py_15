# Задание №4 Функция получает на вход текст вида: “1-й четверг ноября”, “3-я среда мая” и т.п.
# Преобразуйте его в дату в текущем году.
# Логируйте ошибки, если текст не соответсвует формату.

import datetime
import logging
import re
import argparse
import doctest

# Настраиваем логирование: ошибки будут записываться в файл errors.log
logging.basicConfig(level=logging.ERROR, filename='task15_4.log')

# Словарь для преобразования названий дней недели в числовые значения (0 = понедельник, 6 = воскресенье)
days_of_week = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6,
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6
}

# Словарь для преобразования названий месяцев в числовые значения (1 = январь, 12 = декабрь)
months = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "11": 11,
    "12": 12
}

def parse_date(text):
    """
    Функция для преобразования текста вида "1-й четверг ноября" в дату текущего года.
    Если параметры опущены, используются текущие значения.

        Примеры:
    >>> parse_date("1-й четверг ноября")
    datetime.date(2024, 11, 7)
    >>> parse_date("3-я среда мая")
    datetime.date(2024, 5, 15)
    >>> parse_date("2-я пятница июня")
    datetime.date(2024, 6, 14)
    >>> parse_date("5-й вторник февраля")  # Пример, когда 5-й вторник выходит за пределы месяца
    None
    >>> parse_date("1-й вторник 12")  # Числовой месяц
    datetime.date(2024, 12, 3)
    >>> parse_date("2-я 3 6")  # Числовые день недели и месяц
    datetime.date(2024, 6, 12)
    >>> parse_date("3-я 2 7")  # Числовые день недели и месяц
    datetime.date(2024, 7, 16)
    >>> parse_date("")  # Пустая строка, берутся текущие значения
    datetime.date(2024, 7, 11)
    >>> parse_date("3-я")  # Опущены день недели и месяц, берутся текущие значения
    datetime.date(2024, 7, 24)
    >>> parse_date("4-й вторник")  # Опущен месяц, берется текущий месяц
    datetime.date(2024, 7, 23)
    """

    # Получаем текущие значения для года, месяца и дня недели
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_day_num = now.weekday()
    current_day = now.day

    # Если строка пустая, используем текущие значения
    if not text.strip():
        return datetime.date(current_year, current_month, current_day)
    else:
        # Регулярное выражение для извлечения номера недели, дня недели и месяца из строки
        match = re.match(r'(\d+)-[йя]?\s?(\w+)?\s?(\w+)?', text.strip())

        if not match:
            logging.error(f"Неправильный формат строки: {text}")
            return None

        # Извлекаем номер недели, день недели и месяц из найденных групп
        week_num, day_name, month_name = match.groups()

        try:
            # Преобразуем номер недели в целое число
            week_num = int(week_num) if week_num else 1
            # Преобразуем название дня недели в его числовое значение
            day_num = days_of_week[day_name.lower()] if day_name else current_day_num
            # Преобразуем название месяца в его числовое значение
            month_num = months[month_name.lower()] if month_name else current_month
        except KeyError as e:
            # Логируем ошибку, если не удалось преобразовать название дня недели или месяца
            logging.error(f"Ошибка при разборе строки: {e}")
            return None

    # Определяем первый день заданного месяца
    first_day_of_month = datetime.date(current_year, month_num, 1)
    # Определяем день недели первого дня месяца (0 = понедельник, 6 = воскресенье)
    first_day_of_month_weekday = first_day_of_month.weekday()

    # Вычисляем первый заданный день недели в этом месяце
    if first_day_of_month_weekday <= day_num:
        # Если первый день месяца раньше или совпадает с нужным днем недели, вычисляем дату
        day = 1 + day_num - first_day_of_month_weekday
    else:
        # Если первый день месяца позже нужного дня недели, переходим на следующую неделю
        day = 1 + 7 - (first_day_of_month_weekday - day_num)

    # Вычисляем дату нужной недели
    day += (week_num - 1) * 7

    # Получаем итоговую дату, прибавляя рассчитанное количество дней к первому дню месяца
    result_date = first_day_of_month + datetime.timedelta(days=day - 1)

    # Проверяем, что полученная дата попадает в правильный месяц
    if result_date.month != month_num:
        logging.error(f"Дата выходит за пределы месяца: {text}")
        return None

    return result_date

'''
# Пример использования, согласно семинара - передаём параметры в теле кода
text = "7-й четверг ноября"
date = parse_date(text)
if date:
    print(f"Дата: {date}")
else:
    print("Ошибка при обработке даты.")
'''

# пример с передачей параметра из командной строки
# например 'python python15_4.py "1-й четверг ноября"'
# например 'python python15_4.py "3-я 2 7"' 
# например 'python python15_4.py

def main():
    # Настраиваем аргументы командной строки
    parser = argparse.ArgumentParser(description="Преобразование текста вида '1-й четверг ноября' в дату текущего года.")
    parser.add_argument("text", type=str, nargs='?', default="", help="Текст для преобразования в дату")
    
    # Парсим аргументы командной строки
    args = parser.parse_args()
    
    # Получаем дату из текста
    date = parse_date(args.text)
    
    # Выводим результат
    if date:
        print(f"Дата: {date}")
    else:
        print("Ошибка при обработке даты.")

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()  # Запуск тестов doctest
    main()