from sqlalchemy import Column, Integer, String
from database.init import Base

# TODO: it's better to clear revoked tokens from database


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(255), unique=True, nullable=False)  # JWT ID as unique identifier
