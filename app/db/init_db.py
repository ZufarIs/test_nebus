import csv
import os
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, organization_phones, organization_activities
from typing import List, Dict

def load_csv(filename: str) -> List[Dict]:
    """
    Загрузить данные из CSV файла.
    
    Args:
        filename (str): Имя файла CSV
        
    Returns:
        List[Dict]: Список словарей с данными из CSV
        
    Raises:
        FileNotFoundError: Если файл не найден
    """
    data = []
    with open(os.path.join('data', filename), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Преобразуем 'null' в None и обрабатываем строковые поля
            for key, value in row.items():
                if value == 'null' or value == '':
                    row[key] = None
                elif key in ['latitude', 'longitude']:
                    row[key] = float(value)
                elif key in ['id', 'parent_id', 'level', 'building_id', 'organization_id', 'activity_id']:
                    row[key] = int(value) if value else None
                else:
                    # Обработка строковых полей (name, address и т.д.)
                    row[key] = value.strip() if value else None
            data.append(row)
    return data

def init_db(db: Session) -> None:
    """
    Инициализировать базу данных тестовыми данными из CSV файлов.
    
    Args:
        db (Session): Сессия базы данных
        
    Raises:
        Exception: При ошибке загрузки данных
    """
    # Загружаем данные из CSV файлов
    activities_data = load_csv('activities.csv')
    buildings_data = load_csv('buildings.csv')
    organizations_data = load_csv('organizations.csv')
    org_activities_data = load_csv('organization_activities.csv')
    org_phones_data = load_csv('organization_phones.csv')

    # Создаем активности
    for activity in activities_data:
        db_activity = Activity(**activity)
        db.add(db_activity)
    db.flush()

    # Создаем здания
    for building in buildings_data:
        db_building = Building(**building)
        db.add(db_building)
    db.flush()

    # Создаем организации
    for org in organizations_data:
        db_org = Organization(**org)
        db.add(db_org)
    db.flush()

    # Добавляем связи организаций с активностями
    for relation in org_activities_data:
        db.execute(
            organization_activities.insert(),
            [relation]
        )

    # Добавляем телефоны организаций
    for phone in org_phones_data:
        db.execute(
            organization_phones.insert(),
            [phone]
        )

    db.commit() 
 