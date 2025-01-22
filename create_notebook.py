import nbformat as nbf

nb = nbf.v4.new_notebook()

markdown_cell1 = nbf.v4.new_markdown_cell("""# Примеры использования API справочника организаций

Этот ноутбук демонстрирует примеры работы с API через библиотеку requests.""")

code_cell1 = nbf.v4.new_code_cell("""import requests
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
}""")

markdown_cell2 = nbf.v4.new_markdown_cell("## 1. Получение списка организаций")

code_cell2 = nbf.v4.new_code_cell("""# Получение всех организаций
response = requests.get(f"{BASE_URL}/organizations", headers=headers)
print(f"Статус: {response.status_code}")
pprint(response.json())""")

markdown_cell3 = nbf.v4.new_markdown_cell("## 2. Поиск организаций по параметрам")

code_cell3 = nbf.v4.new_code_cell("""# Поиск по названию
params = {"name": "Tech"}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
print(f"Поиск организаций с 'Tech' в названии:")
pprint(response.json())""")

code_cell4 = nbf.v4.new_code_cell("""# Поиск по радиусу
params = {
    "lat": 55.7558,
    "lon": 37.6173,
    "radius": 1.0
}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
print(f"Организации в радиусе 1 км от точки:")
pprint(response.json())""")

markdown_cell4 = nbf.v4.new_markdown_cell("## 3. Работа со зданиями")

code_cell5 = nbf.v4.new_code_cell("""# Получение списка зданий
response = requests.get(f"{BASE_URL}/buildings", headers=headers)
print(f"Список всех зданий:")
pprint(response.json())""")

code_cell6 = nbf.v4.new_code_cell("""# Получение конкретного здания
building_id = 1
response = requests.get(f"{BASE_URL}/buildings/{building_id}", headers=headers)
print(f"Информация о здании {building_id}:")
pprint(response.json())""")

markdown_cell5 = nbf.v4.new_markdown_cell("## 4. Работа с видами деятельности")

code_cell7 = nbf.v4.new_code_cell("""# Получение дерева видов деятельности
response = requests.get(f"{BASE_URL}/activities", headers=headers)
print(f"Дерево видов деятельности:")
pprint(response.json())""")

code_cell8 = nbf.v4.new_code_cell("""# Поиск организаций по виду деятельности
params = {"activity_id": 1}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
print(f"Организации с видом деятельности 1:")
pprint(response.json())""")

markdown_cell6 = nbf.v4.new_markdown_cell("## 5. Комбинированные запросы")

code_cell9 = nbf.v4.new_code_cell("""# Поиск организаций по виду деятельности в радиусе
params = {
    "activity_id": 1,
    "lat": 55.7558,
    "lon": 37.6173,
    "radius": 1.0
}
response = requests.get(f"{BASE_URL}/organizations", headers=headers, params=params)
print(f"Организации с видом деятельности 1 в радиусе 1 км:")
pprint(response.json())""")

nb.cells = [markdown_cell1, code_cell1, 
            markdown_cell2, code_cell2,
            markdown_cell3, code_cell3, code_cell4,
            markdown_cell4, code_cell5, code_cell6,
            markdown_cell5, code_cell7, code_cell8,
            markdown_cell6, code_cell9]

# Сохраняем ноутбук
with open('api_examples.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f) 
