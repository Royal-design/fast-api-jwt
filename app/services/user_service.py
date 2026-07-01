from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate, hashed_password: str):
        db_user = User(
            **user.model_dump(exclude={"password"}),
            password=hashed_password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.get_user_by_id(user_id)

        if not db_user:
            return None

        updates = user.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)

        return db_user
        
      