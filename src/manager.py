import psycopg2
from psycopg2.extras import DictCursor


class DBManager:

    def __init__(self, host, database, user, password):
        self.conn = self.connect(host, database, user, password)

    @staticmethod
    def connect(host, database, user, password):
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    @staticmethod
    def display(rows):
        if rows:
            print("".join([f'{key:<50}' for key in rows[0].keys()]))
            print("=" * 223)
            for row in rows:
                print("".join([f'{str(key):<50}' for key in row.values()]))
            print("=" * 223)
        else:
            print("Empty")

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT employers.name AS "Название компании", COUNT(vacancy_id) AS "Количество вакансий"
                FROM vacancies
                INNER JOIN employers USING (employer_id)
                GROUP BY employers.name
            """)
            self.display(cur.fetchall())

    def get_all_vacancies(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT
                    employers.name AS "Название компании", 
                    vacancies.name AS "Название вакансии", 
                    CASE 
                        WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN 'от ' || salary_from || ' до ' || salary_to
                        WHEN salary_from IS NOT NULL THEN 'от ' || salary_from
                        WHEN salary_to IS NOT NULL THEN 'до ' || salary_to
                        ELSE 'Не указана'
                    END AS "Зарплата",
                    url AS "Ссылка"
                FROM vacancies
                INNER JOIN employers USING (employer_id);
            """)
            self.display(cur.fetchall())

    def get_avg_salary(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT AVG(salary_from) AS "Средняя зарплата"
                FROM vacancies;
            """)
            self.display(cur.fetchall())

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT *
                FROM vacancies
                WHERE salary_from > (
                    SELECT AVG(salary_from)
                    FROM vacancies
                );
            """)
            self.display(cur.fetchall())

    def get_vacancies_with_keyword(self, words: list[str]):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            like_string = " OR ".join([f"name ILIKE '%{word}%'" for word in words])
            cur.execute(f"""
                SELECT *
                FROM vacancies
                WHERE {like_string};
            """)
            self.display(cur.fetchall())
