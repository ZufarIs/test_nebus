import os
import uvicorn
from app.db.session import engine
from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.core.config import settings

def init_database():
    """
    Инициализация базы данных при первом запуске.
    """
    if not os.path.exists(settings.DB_PATH):
        # Создаем директорию data если её нет
        os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
        print(f"База данных не найдена. Выполняется инициализация в {settings.DB_PATH}")
        print("Создание таблиц...")
        Base.metadata.create_all(bind=engine)
        print("Инициализация данными из CSV...")
        db = SessionLocal()
        try:
            init_db(db)
            print("База данных успешно инициализирована.")
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    init_database()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
