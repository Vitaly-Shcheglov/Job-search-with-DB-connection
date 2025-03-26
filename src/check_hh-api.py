import requests


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    def get_companies(self, company_ids):
        companies = []
        for company_id in company_ids:
            try:
                response = requests.get(f"{self.BASE_URL}/employers/{company_id}", timeout=5)
                response.raise_for_status()
                company_data = response.json()
                companies.append(company_data)
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred for company_id {company_id}: {http_err}")
            except Exception as err:
                print(f"An error occurred for company_id {company_id}: {err}")
        return companies

    def get_vacancies(self, company_id):
        vacancies = []
        try:
            response = requests.get(f"{self.BASE_URL}/vacancies?employer_id={company_id}", timeout=5)
            response.raise_for_status()
            vacancies = response.json().get("items", [])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred for company_id {company_id}: {http_err}")
        except Exception as err:
            print(f"An error occurred for company_id {company_id}: {err}")
        return vacancies


def main():
    hh_api = HHAPI()

    company_ids = [2794209]

    companies = hh_api.get_companies(company_ids)

    if not companies:
        print("Не удалось получить компании. Проверьте идентификаторы.")
        return

    print("Полученные компании:")
    for company in companies:
        print(f"Название: {company.get('name', 'не указано')}")

    first_company_id = companies[0].get("id")
    if first_company_id:
        vacancies = hh_api.get_vacancies(first_company_id)

        print(f"\nВакансии для компании {first_company_id}:")
        if not vacancies:
            print("Нет доступных вакансий.")
        else:
            for vacancy in vacancies:
                print(
                    f"Название: {vacancy.get('name', 'не указано')}, ЗП: {vacancy.get('salary', {}).get('from', 'не указана')} - {vacancy.get('salary', {}).get('to', 'не указана')}"
                )


if __name__ == "__main__":
    main()
