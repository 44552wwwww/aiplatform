"""Auth Service — 用户注册、登录、JWT 管理

所有数据库操作在此层完成。
API 层不直接操作数据库。
"""

import logging

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    def register(self, db: Session, username: str, password: str) -> User:
        """用户注册：校验 → 加密 → 入库"""
        # 检查用户名是否已存在
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            raise ValueError(f"用户名已存在: {username}")

        user = User(
            username=username,
            password_hash=hash_password(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("User registered: id=%s username=%s", user.id, user.username)
        return user

    def login(self, db: Session, username: str, password: str) -> dict:
        """用户登录：验证凭证 → 签发 JWT"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise ValueError("用户名或密码错误")
        if not verify_password(password, user.password_hash):
            raise ValueError("用户名或密码错误")

        token = create_access_token(data={"sub": str(user.id)})
        logger.info("User login: id=%s username=%s", user.id, user.username)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
            },
        }

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()


auth_service = AuthService()
