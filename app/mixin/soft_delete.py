from datetime import datetime
from sqlalchemy import Column, DateTime

class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    def restore(self):
        self.deleted_at = None

    @property
    def is_deleted(self):
        return self.deleted_at is not None
