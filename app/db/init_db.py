import csv
import os
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, PhoneNumber, organization_activity
from typing import List, Dict

def load_csv(filename: str) -> List[Dict]:
    """
    Загрузить данные из CSV файла.
    
    Args:
        filename (str): Имя файла CSV
        
    Returns:
        List[Dict]: Список словарей с данными из CSV
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
                elif key in ['id', 'parent_id', 'level', 'building_id']:
                    row[key] = int(value) if value else None
                else:
                    row[key] = value.strip() if value else None
            data.append(row)
    return data

def init_db(db: Session) -> None:
    """
    Инициализировать базу данных тестовыми данными из CSV файлов.
    
    Args:
        db (Session): Сессия базы данных
    """
    # Загружаем данные из CSV файлов
    activities_data = load_csv('activities.csv')
    buildings_data = load_csv('buildings.csv')
    organizations_data = load_csv('organizations.csv')

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

    # Создаем организации и их телефоны
    for org_data in organizations_data:
        phones = org_data.pop('phones', '').split(';')
        activity_ids = [int(id) for id in org_data.pop('activity_ids', '').split(',') if id]
        
        org = Organization(**org_data)
        
        # Добавляем телефоны
        for phone in phones:
            if phone:
                phone_number = PhoneNumber(phone=phone)
                org.phones.append(phone_number)
        
        # Добавляем виды деятельности
        for activity_id in activity_ids:
            activity = db.query(Activity).get(activity_id)
            if activity:
                org.activities.append(activity)
        
        db.add(org)

    db.commit() 
 