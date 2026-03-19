from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserSearch(Base):
    __tablename__ = 'user_searches'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming there's a users table
    location = Column(String, index=True)
    keyword = Column(String, default="pet friendly")
    radius = Column(Integer, default=3000)

    user = relationship("User", back_populates="searches")  # Assuming a User model exists

    def __repr__(self):
        return f"<UserSearch(id={self.id}, user_id={self.user_id}, location={self.location}, keyword={self.keyword}, radius={self.radius})>"