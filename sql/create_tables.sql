CREATE TABLE employers (
	employer_id INT PRIMARY KEY,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE vacancies (
	vacancy_id INT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	salary_from FLOAT,
	salary_to FLOAT,
	url TEXT NOT NULL,
	employer_id INT REFERENCES employers(employer_id)
);