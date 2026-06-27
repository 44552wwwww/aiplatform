"""Auth API — 用户注册、登录、当前用户"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserInfo
from app.services.auth_service import auth_service
from app.core.dependency import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册 — 注册成功直接返回 JWT"""
    try:
        user = auth_service.register(db, username=body.username, password=body.password)
        result = auth_service.login(db, username=body.username, password=body.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    """用户登录 — 返回 JWT"""
    try:
        return auth_service.login(db, username=body.username, password=body.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息（需 JWT）"""
    return current_user
