from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.organization import organization_activity

class Activity(Base):
    """
    Модель для представления видов деятельности организаций.
    
    Attributes:
        id (int): Уникальный идентификатор вида деятельности
        name (str): Название вида деятельности
        parent_id (int): ID родительского вида деятельности (для иерархии)
        level (int): Уровень вложенности в иерархии (1-3)
        parent (Activity): Связь с родительской активностью
        children (List[Activity]): Связь с дочерними активностями
        organizations (List[Organization]): Связь с организациями
    """
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    level = Column(Integer, default=1)
    
    # Отношения
    children = relationship(
        "Activity",
        backref="parent",
        remote_side=[id],
        lazy="joined"
    )
    organizations = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities"
    )
