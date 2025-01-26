# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.organization import Organization, PhoneNumber  # noqa
from app.models.building import Building  # noqa
from app.models.activity import Activity  # noqa
