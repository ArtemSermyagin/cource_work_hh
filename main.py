from src.database import create_table, insert_data
from src.manager import DBManager
from src.const import host, database, user, password

db = DBManager(host, database, user, password)
functions = {
    1: ["Получить список всех компаний", db.get_companies_and_vacancies_count],
    2: ["Получить список всех вакансий", db.get_all_vacancies],
    3: ["Получить среднюю зарплату по вакансиям", db.get_avg_salary],
    4: ["Получить список вакансий, у которых зарплата выше средней", db.get_vacancies_with_higher_salary],
    5: ["Получить список вакансий, в названии которых содержатся ключевые слова", db.get_vacancies_with_keyword]
}
index = -1

if __name__ == "__main__":
    create_table()
    insert_data()
    while True:
        for key, value in functions.items():
            print(f"{key}. {value[0]}")
        try:
            index = int(input("Выберите(число): "))
        except ValueError as e:
            print(f"Введите число от 1 до {len(functions)}")
            continue
        if index not in functions.keys():
            print(f"Введите число от 1 до {len(functions)}")
            continue
        elif index == 5:
            words = input("Введите через запятую список ключевых слов: ").replace(" ", "").split(',')
            functions[index][1](words)
        else:
            functions[index][1]()
