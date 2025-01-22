from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, organization_phones

def init_db(db: Session) -> None:
    # Создаем активности
    food = Activity(name="Food", level=1)
    db.add(food)
    db.flush()

    meat = Activity(name="Meat products", parent_id=food.id, level=2)
    dairy = Activity(name="Dairy products", parent_id=food.id, level=2)
    db.add_all([meat, dairy])

    auto = Activity(name="Automobiles", level=1)
    db.add(auto)
    db.flush()

    trucks = Activity(name="Trucks", parent_id=auto.id, level=2)
    cars = Activity(name="Cars", parent_id=auto.id, level=2)
    db.add_all([trucks, cars])
    
    parts = Activity(name="Spare parts", parent_id=cars.id, level=3)
    accessories = Activity(name="Accessories", parent_id=cars.id, level=3)
    db.add_all([parts, accessories])
    db.flush()

    # Создаем здания
    building1 = Building(
        address="Moscow, Lenina St. 1, office 3",
        latitude=55.7558,
        longitude=37.6173
    )
    building2 = Building(
        address="32/1 Bluchera",
        latitude=55.7558,
        longitude=37.6173
    )
    db.add_all([building1, building2])
    db.flush()

    # Создаем организации
    org1 = Organization(
        name="Horns and Hooves LLC",
        building_id=building1.id
    )
    org1.activities.extend([meat, dairy])
    db.add(org1)
    db.flush()

    # Добавляем телефоны
    db.execute(
        organization_phones.insert(),
        [
            {"organization_id": org1.id, "phone": "2-222-222"},
            {"organization_id": org1.id, "phone": "3-333-333"}
        ]
    )

    org2 = Organization(
        name="AutoParts Plus",
        building_id=building2.id
    )
    org2.activities.extend([parts, accessories])
    db.add(org2)
    db.flush()

    db.execute(
        organization_phones.insert(),
        [
            {"organization_id": org2.id, "phone": "8-923-666-13-13"}
        ]
    )

    db.commit() 
