from sqlalchemy.orm import Session

from db.db_models.user import UserModel

# Gets user using email. Returns the user or None
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def create_user(db: Session, username:str, email: str, password_hash: str):
    new_user = UserModel(username=username, email=email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user