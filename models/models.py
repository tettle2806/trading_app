import datetime

from sqlalchemy import MetaData, Column, Table, Integer, String, TIMESTAMP, ForeignKey, JSON


metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permission", JSON),
)


user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.datetime.utcnow),
    Column("role_id", Integer, ForeignKey("roles.id")),
)



