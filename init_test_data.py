from app.db.session import SessionLocal
from app.db.init_db import init_db

def main():
    """
    Функция для инициализации базы данных тестовыми данными из CSV файлов.
    
    Загружает данные из следующих файлов:
    - activities.csv: Виды деятельности
    - buildings.csv: Здания
    - organizations.csv: Организации
    - organization_activities.csv: Связи организаций с видами деятельности
    - organization_phones.csv: Телефоны организаций
    
    Raises:
        Exception: При ошибке инициализации базы данных
    """
    db = SessionLocal()
    try:
        init_db(db)
        print("База данных успешно инициализирована тестовыми данными из CSV файлов")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 
