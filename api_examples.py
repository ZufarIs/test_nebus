import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Базовый URL API
BASE_URL = "http://localhost:8000/api/v1"

# API ключ из .env
API_KEY = os.getenv("API_KEY")

# Заголовки для запросов
headers = {
    "X-API-Key": API_KEY
}

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

# 1. Получение списка организаций
print_section("Получение списка организаций")
response = requests.get(f"{BASE_URL}/organizations", headers=headers)
print(f"Статус: {response.status_code}")
pprint(response.json())

# 2. Поиск организаций по параметрам
print_section("Поиск по названию")
params = {"name": "Tech"}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
pprint(response.json())

print_section("Поиск по радиусу")
params = {
    "lat": 55.7558,
    "lon": 37.6173,
    "radius": 1.0
}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
pprint(response.json())

# 3. Работа со зданиями
print_section("Список зданий")
response = requests.get(f"{BASE_URL}/buildings", headers=headers)
pprint(response.json())

print_section("Информация о здании")
building_id = 1
response = requests.get(f"{BASE_URL}/buildings/{building_id}", headers=headers)
pprint(response.json())

# 4. Работа с видами деятельности
print_section("Дерево видов деятельности")
response = requests.get(f"{BASE_URL}/activities", headers=headers)
pprint(response.json())

print_section("Организации по виду деятельности")
params = {"activity_id": 1}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
pprint(response.json())

# 5. Комбинированные запросы
print_section("Поиск по виду деятельности в радиусе")
params = {
    "activity_id": 1,
    "lat": 55.7558,
    "lon": 37.6173,
    "radius": 1.0
}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
pprint(response.json()) 
