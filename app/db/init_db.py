import csv
import os
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, PhoneNumber, organization_activity
from typing import List, Dict
from app.db.session import SessionLocal

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

def init_db(db: Session):
    # Получаем абсолютный путь к корню проекта
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(project_root, 'app', 'initial_data')
    
    print(f"Загрузка данных из директории: {data_dir}")
    
    # Чистим базу в правильном порядке
    db.query(organization_activity).delete()
    db.query(PhoneNumber).delete()
    db.query(Organization).delete()
    db.query(Building).delete()
    db.query(Activity).delete()
    
    try:
        # Инициализируем виды деятельности
        init_activities(db, data_dir)
        db.flush()
        
        # Инициализируем здания
        init_buildings(db, data_dir)
        db.flush()
        
        # Инициализируем организации
        init_organizations(db, data_dir)
        
        db.commit()
        print("База данных успешно инициализирована")
        
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Ошибка при инициализации базы данных: {str(e)}")

def init_activities(db: Session, data_dir: str):
    csv_path = os.path.join(data_dir, 'activities.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Файл с видами деятельности не найден по пути: {csv_path}\n"
            f"Текущая рабочая директория: {os.getcwd()}"
        )
    
    print(f"Чтение файла активностей: {csv_path}")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"Обработка строки: {row}")
            # Обработка значений parent_id
            parent_id = row['parent_id'].strip() if row['parent_id'] else None
            parent_id = int(parent_id) if parent_id and parent_id.lower() != 'null' else None
            
            activity = Activity(
                id=int(row['id']),
                name=row['name'],
                level=int(row['level']),
                parent_id=parent_id
            )
            db.add(activity)

def init_buildings(db: Session, data_dir: str):
    csv_path = os.path.join(data_dir, 'buildings.csv')
    print(f"Чтение файла зданий: {csv_path}")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            building = Building(
                id=int(row['id']),
                address=row['address'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude'])
            )
            db.add(building)

def init_organizations(db: Session, data_dir: str):
    csv_path = os.path.join(data_dir, 'organizations.csv')
    print(f"Чтение файла организаций: {csv_path}")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Файл с организациями не найден: {csv_path}")

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Обработка организации: {row}")
                # Проверяем обязательные поля
                if 'name' not in row or 'building_id' not in row:
                    raise ValueError("Отсутствуют обязательные поля в CSV файле организаций")
                
                # Создаем организацию
                org = Organization(
                    id=int(row.get('id', 0)) or None,  # Автоинкремент, если id не указан
                    name=row['name'],
                    building_id=int(row['building_id'])
                )
                
                # Обрабатываем телефоны (опциональное поле)
                phones = row.get('phones', '')
                phones = [p.strip() for p in phones.split(';')] if phones else []
                
                # Обрабатываем виды деятельности (опциональное поле)
                activities = row.get('activities', '')
                activity_ids = [int(id.strip()) for id in activities.split(';')] if activities else []
                
                # Добавляем телефоны
                if phones:
                    for phone in phones:
                        # Явное создание и привязка телефона
                        db.add(PhoneNumber(
                            phone=phone,
                            organization_id=org.id,
                            organization=org
                        ))
                
                # Добавляем виды деятельности
                if activities:
                    activity_objects = db.query(Activity).filter(
                        Activity.id.in_(activity_ids)
                    ).all()
                    for activity in activity_objects:
                        org.activities.append(activity)
                
                db.add(org)
                db.flush()  # Сохраняем изменения

            db.commit()
            
            print(f"Добавлено организаций: {db.query(Organization).count()}")
            print(f"Добавлено телефонов: {db.query(PhoneNumber).count()}")
            print(f"Добавлено связей с видами деятельности: {db.execute(organization_activity.select()).rowcount}")
            
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Ошибка при создании организаций: {str(e)}")
