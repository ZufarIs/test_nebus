from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.organization import organization_activity
from typing import List

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
    level = Column(Integer)
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)
    
    # Отношения
    children = relationship("Activity", 
                          backref="parent",
                          remote_side=[id],
                          lazy="joined")
    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities"
    )

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', level={self.level})>"

    @property
    def child_activities(self) -> List['Activity']:
        """Возвращает список дочерних активностей или пустой список."""
        return self.children if self.children is not None else []
