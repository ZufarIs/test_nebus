import os
import uvicorn
from app.db.session import engine
from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal

def init_database():
    """Создает таблицы и заполняет их начальными данными."""
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    
    print("Инициализация данными из CSV...")
    db = SessionLocal()
    try:
        init_db(db)
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        db.close()

def main():
    # Проверяем существование БД
    if not os.path.exists("sql_app.db"):
        print("База данных не найдена. Выполняется инициализация...")
        init_database()
    
    # Запускаем сервер
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 
