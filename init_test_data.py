from app.db.session import SessionLocal
from app.db.init_db import init_db

def main():
    """
    Функция для инициализации базы данных тестовыми данными.
    Создает:
    - Дерево видов деятельности (Food -> Meat/Dairy, Automobiles -> Trucks/Cars -> Parts/Accessories)
    - Здания с координатами
    - Организации с телефонами и видами деятельности
    """
    db = SessionLocal()
    try:
        init_db(db)
        print("База данных успешно инициализирована тестовыми данными")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 
