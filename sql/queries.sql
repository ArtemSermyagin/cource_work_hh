SELECT employers.name AS "Название компании", COUNT(vacancy_id) AS "Количество вакансий"
FROM vacancies
INNER JOIN employers USING (employer_id)
GROUP BY employers.name;


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


SELECT AVG(salary_from) AS "Средняя зарплата"
FROM vacancies;


SELECT *
FROM vacancies
WHERE salary_from > (
	SELECT AVG(salary_from)
	FROM vacancies
);


SELECT *
FROM vacancies
WHERE name ILIKE '%коммерческой%' OR name ILIKE '%Директор%';
