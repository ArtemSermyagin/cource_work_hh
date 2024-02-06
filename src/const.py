import os
from dotenv import load_dotenv

load_dotenv()

employers_id = [
    36227, 3643187, 5912899, 10035323, 10158780, 4429980, 4717703, 5064090, 54794, 4775363
]

host = os.environ.get("HOST")
database = os.environ.get("DATABASE")
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")

create_tables = [
    "CREATE TABLE employers (employer_id INT PRIMARY KEY, name VARCHAR(255) NOT NULL);",
    "CREATE TABLE vacancies (vacancy_id INT PRIMARY KEY,name VARCHAR(255) NOT NULL,salary_from FLOAT,salary_to FLOAT,url TEXT NOT NULL,employer_id INT REFERENCES employers(employer_id));"
]
