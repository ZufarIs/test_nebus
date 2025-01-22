# Organization Directory API

REST API приложение для справочника организаций, зданий и видов деятельности.

## Описание проекта

Приложение предоставляет API для управления:
- Организациями (с телефонами и видами деятельности)
- Зданиями (с адресами и географическими координатами)
- Видами деятельности (в виде дерева с максимальной глубиной 3 уровня)

### Основные возможности
- Получение списка организаций по зданию
- Получение списка организаций по виду деятельности
- Поиск организаций в заданном радиусе от точки на карте
- Поиск организаций по названию
- Поиск по иерархии видов деятельности

## Технологический стек

- FastAPI + Pydantic
- SQLAlchemy + Alembic
- PostgreSQL
- Docker + Docker Compose

## Установка и запуск

### Через Docker

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd organization_directory
```

2. Создайте файл .env:
```bash
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=organization_directory
POSTGRES_PORT=5432
API_KEY=your_secret_api_key
```

3. Запустите контейнеры:
```bash
docker-compose -f docker/docker-compose.yml up -d
```

4. Примените миграции:
```bash
docker-compose exec web alembic upgrade head
```

### Локальная разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или
venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте базу данных в .env

4. Примените миграции:
```bash
alembic upgrade head
```

5. Запустите приложение:
```bash
uvicorn main:app --reload
```

## API Документация

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Аутентификация

Все запросы к API должны содержать заголовок X-API-Key:
```bash
curl -H "X-API-Key: your_secret_api_key" http://localhost:8000/api/v1/organizations
```

### Примеры запросов

1. Получение списка организаций в здании:
```bash
curl -H "X-API-Key: your_secret_api_key" \
     http://localhost:8000/api/v1/organizations?building_id=1
```

2. Поиск организаций по виду деятельности:
```bash
curl -H "X-API-Key: your_secret_api_key" \
     http://localhost:8000/api/v1/organizations?activity_id=1
```

3. Поиск организаций в радиусе:
```bash
curl -H "X-API-Key: your_secret_api_key" \
     "http://localhost:8000/api/v1/organizations?lat=55.7558&lon=37.6173&radius=5"
```

## Структура проекта

```
organization_directory/
├── alembic/              # Миграции БД
├── app/                  # Основной код
│   ├── api/             # API endpoints
│   ├── core/            # Конфигурация
│   ├── db/              # Работа с БД
│   ├── models/          # SQLAlchemy модели
│   └── schemas/         # Pydantic схемы
├── docker/              # Docker файлы
└── tests/               # Тесты
```

## Разработка

### Создание миграций

```bash
alembic revision --autogenerate -m "описание_изменений"
alembic upgrade head
```

### Тестовые данные

Для инициализации БД тестовыми данными:
```bash
python init_test_data.py
```

## Лицензия

MIT
