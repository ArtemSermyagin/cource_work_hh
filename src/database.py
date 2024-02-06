import psycopg2
import requests

from psycopg2.extensions import cursor as db_cursor
from psycopg2.errors import UniqueViolation, DuplicateTable
from src.const import employers_id, host, database, user, password, create_tables


def insert_query(cur: db_cursor, table_name: str, fields: list[str], values: tuple) -> None:
    """
    Функция выполняет вставку записи в таблицу
    :param cur: курсор базы данных
    :param table_name: название таблицы, куда выполнить запрос
    :param fields: список полей
    :param values: список значений
    :return:
    """
    try:
        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s' for _ in fields])})"
        cur.execute(query, values)
    except UniqueViolation as e:
        ...
    finally:
        cur.connection.commit()


def create_table() -> None:
    """
    Функция создаёт таблицы в БД, если их нет
    :return:
    """
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


def insert_data() -> None:
    """
    Функция берет данные с api hh.ri, и вставляет данные в нужные таблицы
    :return:
    """
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
