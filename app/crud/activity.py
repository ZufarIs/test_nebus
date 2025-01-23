from sqlalchemy.orm import Session
from app.models.activity import Activity
from typing import List, Dict

def build_activity_tree(activities: List[Activity]) -> List[Dict]:
    """
    Строит дерево видов деятельности из плоского списка.
    Возвращает список словарей для сериализации.
    """
    # Создаем словарь для быстрого доступа к активностям по id
    activity_dict = {}
    
    # Преобразуем Activity в словари и подготавливаем структуру
    for activity in activities:
        activity_dict[activity.id] = {
            "id": activity.id,
            "name": activity.name,
            "level": activity.level,
            "parent_id": activity.parent_id,
            "children": []
        }
    
    # Строим дерево
    roots = []
    for activity_id, activity_data in activity_dict.items():
        if activity_data["parent_id"] is None:
            roots.append(activity_data)
        else:
            parent = activity_dict.get(activity_data["parent_id"])
            if parent:
                parent["children"].append(activity_data)
    
    return roots

def get_activities(db: Session) -> List[Dict]:
    """
    Получает все виды деятельности и строит дерево.
    """
    activities = db.query(Activity).all()
    return build_activity_tree(activities)

def get_activity(db: Session, activity_id: int) -> Activity:
    """
    Получает конкретный вид деятельности.
    """
    return db.query(Activity).filter(Activity.id == activity_id).first() 
