from sqlalchemy.orm import Session
from .token import RevokedToken


def add_revoke_token(db: Session, jti: str):
    revoked_token = RevokedToken(jti=jti)
    db.add(revoked_token)
    db.commit()
    db.refresh(revoked_token)


def is_token_revoked(db: Session, jti: str) -> bool:
    return db.query(RevokedToken).filter(RevokedToken.jti == jti).first() is not None
