import argparse
import csv
import logging
import os
import sys

logging.basicConfig(filename='hw.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

class NameDescriptor:
    """
    Дескриптор для проверки и установки имени студента.

    Проверяет, что имя состоит только из букв и начинается с заглавной буквы.
    """
    def __get__(self, instance, owner):
        return instance._name
    
    def __set__(self, instance, value):
        if not value.istitle() or not value.replace(' ', '').isalpha():
            raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        instance._name = value

class Student:
    """
    Класс, представляющий студента.

    Attributes:
        name (str): Имя студента.
        subjects (dict): Словарь для хранения предметов и связанных с ними оценок и результатов тестов.
        subjects_file (str): Путь к файлу с предметами и оценками.
    """
    name = NameDescriptor()
    
    def __init__(self, name, subjects_file=None):
        """
        Инициализация студента.

        Args:
            name (str): Имя студента.
            subjects_file (str, optional): Путь к файлу с предметами и оценками. По умолчанию None.
        """
        self.name = name
        self.subjects = {}
        self.subjects_file = subjects_file
        if subjects_file:
            self.load_subjects(subjects_file)

    def __setattr__(self, name, value):
        """
        Переопределение метода для установки атрибутов.

        Args:
            name (str): Имя атрибута.
            value: Значение атрибута.
        """
        if name == "name":
            super().__setattr__(name, value)
        else:
            self.__dict__[name] = value

    def load_subjects(self, subjects_file):
        """
        Загрузка предметов и их начальных оценок из CSV файла.

        Args:
            subjects_file (str): Путь к файлу с предметами и оценками.
        
        Raises:
            Exception: Если происходит ошибка загрузки файла.
        """
        try:
            if not os.path.exists(subjects_file):
                raise FileNotFoundError(f"Файл {subjects_file} не найден")
            
            with open(subjects_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student_name = row['Студент']
                    subject = row['Предмет']
                    grade = int(row['Оценка'])
                    test_score = int(row['Результат теста'])

                    if student_name == self.name:
                        if subject not in self.subjects:
                            self.subjects[subject] = {'grades': [], 'test_scores': []}
                        self.subjects[subject]['grades'].append(grade)
                        self.subjects[subject]['test_scores'].append(test_score)
        except FileNotFoundError as e:
            logging.warning(f"Файл с оценками {subjects_file} не найден")
            print(f"Файл с оценками {subjects_file} не найден")
        except Exception as e:
            logging.error(f"Ошибка загрузки предметов из файла {subjects_file}: {e}")
            raise

    def add_grade(self, subject, grade):
        """
        Добавление оценки для указанного предмета и запись в файл.

        Args:
            subject (str): Название предмета.
            grade (int): Оценка (целое число от 2 до 5).
        
        Raises:
            ValueError: Если оценка не соответствует допустимому диапазону.
        """
        try:
            if subject not in self.subjects:
                self.subjects[subject] = {'grades': [], 'test_scores': []}  # Создаем запись для нового предмета
            if not isinstance(grade, int) or grade < 2 or grade > 5:
                raise ValueError("Оценка должна быть целым числом от 2 до 5")
            self.subjects[subject]['grades'].append(grade)
            self._save_to_csv()
            logging.info(f"Добавлена оценка {grade} по предмету {subject} для студента {self.name}")
        except Exception as e:
            logging.error(f"Ошибка добавления оценки для предмета {subject}: {e}")
            raise

    def add_test_score(self, subject, test_score):
        """
        Добавление результата теста для указанного предмета и запись в файл.

        Args:
            subject (str): Название предмета.
            test_score (int): Результат теста (целое число от 0 до 100).
        
        Raises:
            ValueError: Если результат теста не соответствует допустимому диапазону.
        """
        try:
            if subject not in self.subjects:
                self.subjects[subject] = {'grades': [], 'test_scores': []}  # Создаем запись для нового предмета
            if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
                raise ValueError("Результат теста должен быть целым числом от 0 до 100")
            self.subjects[subject]['test_scores'].append(test_score)
            self._save_to_csv()
            logging.info(f"Добавлен результат теста {test_score} по предмету {subject} для студента {self.name}")
        except Exception as e:
            logging.error(f"Ошибка добавления результатов теста для предмета {subject}: {e}")
            raise

    def get_average_test_score(self, subject):
        """
        Вычисление среднего результата тестов для указанного предмета.

        Args:
            subject (str): Название предмета.
        
        Returns:
            float: Средний результат тестов.
        
        Raises:
            ValueError: Если предмет не найден.
        """
        try:
            if subject not in self.subjects:
                raise ValueError(f"Предмет {subject} не найден")
            test_scores = self.subjects[subject]['test_scores']
            return sum(test_scores) / len(test_scores) if test_scores else 0.0
        except Exception as e:
            logging.error(f"Ошибка вычисления среднего результата тестов для предмета {subject}: {e}")
            raise

    def get_average_grade(self):
        """
        Вычисление среднего балла по всем предметам.

        Returns:
            float: Средний балл.
        
        Raises:
            ValueError: Если не удалось вычислить средний балл (например, отсутствуют оценки по предметам).
        """
        try:
            total_grades = []
            for subject in self.subjects:
                total_grades.extend(self.subjects[subject]['grades'])
            return sum(total_grades) / len(total_grades) if total_grades else 0.0
        except Exception as e:
            logging.error(f"Ошибка вычисления среднего балла: {e}")
            raise

    def _save_to_csv(self):
        """
        Сохранение данных о предметах и оценках в файл subjects.csv.
        """
        try:
            with open(self.subjects_file, mode='a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Студент', 'Предмет', 'Оценка', 'Результат теста']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                for subject, data in self.subjects.items():
                    for i in range(max(len(data['grades']), len(data['test_scores']))):
                        writer.writerow({
                            'Студент': self.name,
                            'Предмет': subject,
                            'Оценка': data['grades'][i] if i < len(data['grades']) else '',
                            'Результат теста': data['test_scores'][i] if i < len(data['test_scores']) else ''
                        })

            logging.info(f"Данные о предметах и оценках для студента {self.name} сохранены в файл {self.subjects_file}")
        except Exception as e:
            logging.error(f"Ошибка сохранения данных в файл {self.subjects_file}: {e}")
            raise

    def __str__(self):
        """
        Строковое представление объекта Student.

        Returns:
            str: Информация о студенте и его предметах.
        """
        subjects_with_data = [subject for subject in self.subjects if self.subjects[subject]['grades'] or self.subjects[subject]['test_scores']]
        subjects_str = ", ".join(subjects_with_data)
        return f"Студент: {self.name}\nПредметы: {subjects_str}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Управление данными студента')
    parser.add_argument('name', metavar='name', type=str, nargs='?', help='Имя студента')
    parser.add_argument('--subjects_file', type=str, default='subjects.csv', help='Путь к файлу с предметами и оценками')
    parser.add_argument('--add_grade', nargs=2, metavar=('subject', 'grade'), help='Добавить оценку по предмету')
    parser.add_argument('--add_test_score', nargs=2, metavar=('subject', 'test_score'), help='Добавить результат теста по предмету')
    parser.add_argument('--average_grade', action='store_true', help='Вычислить средний балл по всем предметам')
    parser.add_argument('--average_test_score', type=str, metavar='subject', help='Вычислить средний результат по тестам по указанному предмету')
    args = parser.parse_args()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)

    try:
        if not args.name:
            students = set()
            try:
                with open(args.subjects_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        students.add(row['Студент'])
            except FileNotFoundError:
                logging.warning(f"Файл с предметами и оценками {args.subjects_file} не найден")
                print(f"Файл с предметами и оценками {args.subjects_file} не найден")
                sys.exit(1)

            if students:
                print("Укажите имя студента. Доступные имена:")
                for student in students:
                    print(student)
            else:
                logging.warning(f"В файле {args.subjects_file} не найдены данные о студентах")
                print(f"В файле {args.subjects_file} не найдены данные о студентах")
            sys.exit(1)

        logging.info(f"Запуск скрипта с аргументами: {sys.argv}")

        student = Student(args.name, args.subjects_file)

        if args.add_grade:
            subject, grade = args.add_grade
            student.add_grade(subject, int(grade))
        
        if args.add_test_score:
            subject, test_score = args.add_test_score
            student.add_test_score(subject, int(test_score))

        if args.average_grade:
            average_grade = student.get_average_grade()
            print(f"Средний балл: {average_grade}")
            logging.info(f"Вычислен средний балл {average_grade}")

        if args.average_test_score:
            average_test_score = student.get_average_test_score(args.average_test_score)
            print(f"Средний результат по тестам по предмету {args.average_test_score}: {average_test_score}")
            logging.info(f"Вычислен средний результат по тестам {average_test_score} по предмету {args.average_test_score}")

        if not args.add_grade and not args.add_test_score and not args.average_grade and not args.average_test_score:
            print(str(student))
            logging.info(f"Выведена информация о студенте: {student.name}")

    except Exception as e:
        logging.error(f"Ошибка выполнения скрипта: {e}")
        sys.exit(1)
