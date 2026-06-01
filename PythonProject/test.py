import requests
import time


def fetch_infosec_vacancies(pages=1):

    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "infosec-script/1.0"}

    all_vacancies = []

    for page in range(pages):
        params = {
            "text": "cybersecurity",
            "area": 113,
            "page": page,
            "per_page": 50,
        }

        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        if "items" not in data:
            print("Ошибка или пустой ответ:", data)
            break

        all_vacancies.extend(data["items"])

    return all_vacancies


def print_vacancies(vacancies):
    for v in vacancies:

        try:
            print(f"Профессия: {v.get("name")}")
            print(f"Компания: {v.get("employer", {}).get("name")}")
            print(f"Город: {v.get("address", {}).get("city")}")

            print(f"Зарплата: {v.get("salary", {}).get("from")} {v.get("salary", {}).get("currency")}")

            print()
        except Exception as e:
            print()


if __name__ == "__main__":
    # vacancies = fetch_infosec_vacancies(pages=1)
    # print_vacancies(vacancies)
    i = 0
    for i in range(20):
        pass
    print(i)


for index, elem in enumerate(tracks):
    artists = ", ".join(map(lambda a: a.name, elem.artists))
    print(f"{index}. {elem.title} — {artists}") if is_num else print(f"{elem.title} — {artists}")
print(f"It is {len(tracks)} tracks.")
