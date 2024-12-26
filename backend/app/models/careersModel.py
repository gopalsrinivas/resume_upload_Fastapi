from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.core.database import Base


class CareersUsers(Base):
    __tablename__ = "careersusers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    mobile = Column(String(150), unique=True, index=True)
    resume_filename = Column(String(500))
    is_active = Column(Boolean, default=False)
    created_on = Column(DateTime, default=func.now(), nullable=False)
    updated_on = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<User {self.name} (ID: {self.user_id}) created on {self.created_on}>"
