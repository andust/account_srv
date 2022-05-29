from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

from src.authentication.domain import model

metadata = MetaData()

users = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("full_name", String(128)),
    Column("email", String(128), unique=True, nullable=False),
    Column("password", String(128), nullable=False),
)


def start_mappers():
    mapper(model.User, users)
