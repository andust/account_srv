
import json
from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.infra.database.sqlalchemy import get_db
from src.infra.events.nats.client import nats_connection
from src.authentication.adapters.repository import UserSqlAlchemyRepository
from src.authentication.adapters.services import Argon2HashService, JWTService
from src.authentication.service_layer import services
from src.authentication.entrypoints.dto import user_dto
from src.authentication.domain.model import Token, User
from src.authentication.domain.exceptions import EmailNotUniqueError, PasswordValidationError, UserNotFoundError


router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=user_dto.User,
)
async def register(user: user_dto.UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = services.register_user(
            user=User(full_name=user.full_name,
                      email=user.email,
                      password=user.password),
            hash_service=Argon2HashService,
            repo=UserSqlAlchemyRepository(db))

        async with nats_connection() as nc:
            await nc.publish("user.created", json.dumps({"id": created_user.id, "email": created_user.email}).encode())
        
        return user_dto.User(id=created_user.id, full_name=created_user.full_name, email=created_user.email)
    except EmailNotUniqueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.as_dict())


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token
)
async def login(user: user_dto.UserCredentials, db: Session = Depends(get_db)):
    try:
        return services.login_user(
            email=user.email,
            password=user.password,
            hash_service=Argon2HashService,
            jwt_service=JWTService,
            repo=UserSqlAlchemyRepository(db))
    except (PasswordValidationError, UserNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.as_dict())
