import requests
import json
import time
import os

# Токен для доступу до API
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkX2F0IjoxNzQwNzI1Mjk5LCJhcHBfaWQiOjE3NDA3MjUyOTl9.pfVUCnbhPoeiPhffMJO47wwPfekKkWEFagf0nFn9yVw"

# Конфігурація API
API_URL = "https://api.usersbox.ru/v1/search"

# Функція для пошуку за номером телефону
def search_phone(phone_number):
    headers = {
        "Authorization": TOKEN
    }
    params = {
        "q": phone_number
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Перевіряємо статус відповіді
        data = response.json()

        # Для дебагінгу виведемо всю відповідь
        #print("Отримана відповідь API:", json.dumps(data, indent=4))  # Це допоможе побачити структуру даних
        return data  # Повертаємо JSON об'єкт

    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту: {e}")
        return None

# Функція для декодування Unicode escape
def decode_unicode(value):
    if isinstance(value, bytes):
        # Якщо значення є байтами, спочатку перекодуємо його в рядок
        value = value.decode('unicode_escape')  # Перетворюємо байти на строку, передаючи кодування UTF-8
    return value  # Якщо значення не є рядком чи байтами, повертаємо його без змін


# Основний код
#phone_number = "79505246441"
#response_data = search_phone(phone_number)



def data_processing(response_data):
    best_result = ["", "", "", ""]  # Прізвище, Ім'я, По батькові, Дата народження

    if response_data and 'data' in response_data:
        items = response_data['data'].get('items', [])

        if items:
            for item in items:
                hits = item.get('hits', {}).get('items', [])

                for hit in hits:
                    full_name = decode_unicode(hit.get('full_name', '')).strip()
                    surname = decode_unicode(hit.get('surname', '')).strip()
                    name = decode_unicode(hit.get('name', '')).strip()
                    middle_name = decode_unicode(hit.get('middle_name', '')).strip()
                    birth_date = hit.get('birth_date', '').strip()

                    #print(f"\nОтримані дані: {full_name} | {surname} | {name} | {middle_name} | {birth_date}")

                    # Видаляємо значення 'R' і порожні поля
                    def clean(value):
                        return value if value and value != "R" else ""

                    surname, name, middle_name, birth_date = map(clean, [surname, name, middle_name, birth_date])

                    # Якщо є full_name, розбиваємо його та фільтруємо
                    if full_name and birth_date:
                        split_full_name = [clean(part) for part in full_name.split(" ")] + [birth_date]
                        while len(split_full_name) < 4:
                            split_full_name.append("")  # Доповнюємо до 4 елементів
                    else:
                        split_full_name = [surname, name, middle_name, birth_date]

                    # Лог результату після очищення
                    #print(f"Очищені дані: {split_full_name}")

                    # Оновлення найкращого варіанту
                    if sum(1 for x in split_full_name if x) > sum(1 for x in best_result if x):
                        best_result = split_full_name

            return best_result  # Повертаємо найкращий варіант

        else:
            #print("Не знайдено жодної інформації про цей номер.")
            return ["", "", "", ""]

    else:
        #print("Помилка при отриманні даних.")
        return ["", "", "", ""]

#a = data_processing(response_data)

def find_inf_db(phone, output_file='output.json'):
    api_url = "https://api.usersbox.ru/v1"
    headers = {"Authorization": TOKEN}

    try:
        # 1. Виконуємо /explain, щоб знайти бази з даними
        explain_response = requests.get(f"{api_url}/explain?q={phone}", headers=headers)
        explain_response.raise_for_status()
        explain_data = explain_response.json()

        if explain_data.get("status") != "success":
            return {}

        sources = explain_data.get("data", {}).get("items", [])
        if not sources:
            return {}

        filtered_results = []
        required_fields = {"surname", "name", "middle_name", "birth_date", "full_name"}

        # 2. Запускаємо /search по кожній базі з /explain
        for source in sources:
            database = source["source"]["database"]
            collection = source["source"]["collection"]
            search_response = requests.get(f"{api_url}/{database}/{collection}/search?q={phone}", headers=headers)
            search_response.raise_for_status()
            search_data = search_response.json()

            if search_data.get("status") != "success":
                continue

            # 3. Фільтруємо результати
            for item in search_data.get("data", {}).get("items", []):
                if any(field in item for field in required_fields):
                    filtered_results.append(item)

            # Додаємо затримку між запитами
            time.sleep(1)

        # 4. Записуємо результат в JSON файл
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(filtered_results, json_file, ensure_ascii=False, indent=4)

        return filtered_results  # Повертаємо список для внутрішнього використання, якщо потрібно

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return {}


def process_json_file(file_path):
    best_result = ["", "", "", ""]  # Прізвище, Ім'я, По батькові, Дата народження

    def clean(value):
        """ Видаляє значення 'R' і порожні поля """
        return value.strip() if value and value != "R" else ""

    # 1. Завантажуємо дані з файлу
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не знайдено.")
        return best_result

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            response_data = json.load(file)
        except json.JSONDecodeError:
            print(f"Помилка декодування JSON у файлі {file_path}.")
            return best_result

    # Переконуємося, що response_data — це список
    if not isinstance(response_data, list):
        print("Очікувався список JSON-об'єктів.")
        return best_result

    # 2. Обробляємо кожен запис у списку
    for item in response_data:
        full_name = clean(item.get("full_name", ""))
        name = clean(item.get("name", ""))
        birth_date = clean(item.get("birth_date", ""))

        surname, middle_name = "", ""

        # Якщо є повне ім'я — розбиваємо його на частини
        if full_name:
            parts = full_name.split()
            surname = clean(parts[0]) if len(parts) > 0 else ""
            name = clean(parts[1]) if len(parts) > 1 else name  # Перезаписуємо, якщо є окреме ім'я
            middle_name = clean(parts[2]) if len(parts) > 2 else ""

        # Формуємо список з 4 полів
        split_full_name = [surname, name, middle_name, birth_date]

        # Оновлюємо найкращий варіант, якщо у нього більше заповнених полів
        if sum(bool(x) for x in split_full_name) > sum(bool(x) for x in best_result):
            best_result = split_full_name

    # 3. Очищаємо JSON-файл після обробки
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump([], file)  # Записуємо пустий список

    return best_result


