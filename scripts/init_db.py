import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db.init_db import init_db

def main():
    """
    Инициализация базы данных:
    1. Создание всех таблиц
    2. Загрузка начальных данных из CSV файлов
    """
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Инициализируем данные
    db = SessionLocal()
    try:
        init_db(db)
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 
