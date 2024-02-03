import psycopg2
import requests

from psycopg2.extensions import cursor as db_cursor
from psycopg2.errors import UniqueViolation, DuplicateTable

from src.manager import DBManager
from src.const import employers_id, host, database, user, password, create_tables


def insert_query(cur: db_cursor, table_name: str, fields: list[str], values: tuple):
    try:
        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s' for _ in fields])})"
        cur.execute(query, values)
    except UniqueViolation as e:
        ...
    finally:
        cur.connection.commit()


def create_table():
    with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
    ) as conn:
        with conn.cursor() as cursor:
            for create_table_query in create_tables:
                try:
                    cursor.execute(create_table_query)
                except DuplicateTable as e:
                    ...
                finally:
                    cursor.connection.commit()


def insert_data():
    with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
    ) as conn:
        with conn.cursor() as cursor:
            for employer_id in employers_id:
                data = requests.get(f'https://api.hh.ru/employers/{employer_id}').json()
                insert_query(cursor, 'employers', ['employer_id', 'name'], (data['id'], data["name"]))

                for item in requests.get(data['vacancies_url']).json()['items']:
                    insert_query(
                        cursor,
                        'vacancies',
                        ['vacancy_id', 'name', 'salary_from', 'salary_to', 'url', 'employer_id'],
                        (
                            item["id"],
                            item["name"],
                            item["salary"].get('from'),
                            item["salary"].get('to'),
                            item["alternate_url"],
                            data['id']
                        )
                    )
        conn.commit()


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
