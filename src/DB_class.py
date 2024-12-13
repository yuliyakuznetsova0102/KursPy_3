import psycopg2

from config import config


class DBManager:
    """Класс для получения данных по вакансиям и компаниям из БД"""

    def __init__(self):
        self.params = config()
        self.conn = psycopg2.connect(dbname="hh_db", **self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Печатает список всех компаний и количество вакансий у каждой компании."""
        query = """
                SELECT c.company_name, COUNT(v.vacancy_id) AS vacancy_count
                FROM companies c
                LEFT JOIN vacancies v ON c.company_id = v.company_id
                GROUP BY c.company_id
                ORDER BY c.company_name;
            """

        try:
            self.cur.execute(query)
            results = self.cur.fetchall()
            # Печатаем результаты
            print("Список компаний и количество вакансий:\n")
            for row in results:
                company_name, vacancy_count = row
                print(f"Компания: {company_name}, Количество вакансий: {vacancy_count}")
            print(f"Всего {len(results)} компаний.")
            print("-" * 50)

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            self.cur.close()
            self.conn.close()

    def get_all_vacancies(self) -> None:
        """Печатает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        query = """
                SELECT c.company_name, v.vacancy_name, 
                COALESCE(v.salary_from, 0) AS salary_from, 
                COALESCE(v.salary_to, 0) AS salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                ORDER BY c.company_name"""

        try:
            self.cur.execute(query)
            results = self.cur.fetchall()

            # Печатаем результаты
            print("Список вакансий:")
            for row in results:
                company_name, vacancy_name, salary_from, salary_to, url = row
                print(
                    f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: от {salary_from} до {salary_to}, "
                    f"Ссылка: {url}"
                )
            print(f"Всего {len(results)} вакансий.")
            print("-" * 50)

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            self.cur.close()
            self.conn.close()

    def get_avg_salary(self) -> None:
        """Печатает среднюю зарплату по вакансиям."""
        query = """
                    SELECT AVG((salary_from + salary_to) / 2.0) AS average_salary
                    FROM vacancies
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                """

        try:
            self.cur.execute(query)
            result = self.cur.fetchall()

            # Печатаем результаты
            if result and result[0] is not None:
                avg_salary = round(float(result[0][0]), 2)
                print(f"Средняя зарплата по вакансиям: {avg_salary}")
            else:
                print("Нет доступных данных о зарплате.")
            print("-" * 50)

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            self.cur.close()
            self.conn.close()

    def get_vacancies_with_higher_salary(self) -> None:
        """Печатает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary_query = """
                SELECT AVG((salary_from + salary_to) / 2.0) AS average_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
                """

        try:
            self.cur.execute(avg_salary_query)
            avg_salary_result = self.cur.fetchone()
            avg_salary = (
                float(avg_salary_result[0])
                if avg_salary_result and avg_salary_result[0] is not None
                else 0
            )

            vacancies_query = """
                    SELECT v.vacancy_name, v.salary_from, v.salary_to, v.city, v.url
                    FROM vacancies v
                    WHERE (v.salary_from + v.salary_to) / 2.0 > %s;
                    """

            self.cur.execute(vacancies_query, (avg_salary,))
            vacancies = self.cur.fetchall()

            # Печатаем результаты
            if vacancies:
                print("Список вакансий с зарплатой выше средней:")
                for vacancy in vacancies:
                    print(
                        f"Вакансия: {vacancy[0]}, Зарплата от: {vacancy[1]}, "
                        f"Зарплата до: {vacancy[2]}, Город: {vacancy[3]}, Ссылка на вакансию: {vacancy[4]}"
                    )
            else:
                print("Нет вакансий с зарплатой выше средней.")
            print(f"Всего {len(vacancies)} вакансии.")
            print("-" * 50)

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            self.cur.close()
            self.conn.close()

    def get_vacancies_with_keyword(self, keywords: list[str]) -> None:
        """Возвращает список всех вакансий, в названии которых содержатся переданные в
        метод слова, например python."""
        conditions = " OR ".join(["vacancy_name ILIKE %s " for _ in keywords])
        query = f"""
               SELECT v.vacancy_id, v.vacancy_name, c.company_name, v.city, v.salary_from, v.salary_to, v.currency
               FROM vacancies v
               JOIN companies c ON v.company_id = c.company_id
               WHERE {conditions}
           """
        params = [f"%{keyword}%" for keyword in keywords]

        try:
            self.cur.execute(query, params)
            vacancies = self.cur.fetchall()
            # Печатаем результаты
            for vacancy in vacancies:
                print(
                    {
                        "id": vacancy[0],
                        "Вакансия": vacancy[1],
                        "Компания": vacancy[2],
                        "Город": vacancy[3],
                        "Зарплата от": vacancy[4],
                        "Зарплата до": vacancy[5],
                        "Валюта": vacancy[6],
                    }
                )
            print(f"\nНайдено {len(vacancies)} вакансий.")
            print("-" * 50)

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            self.cur.close()
            self.conn.close()