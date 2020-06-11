import sqlalchemy

from sqlalchemy.sql import expression
from databases import Database

from config import DB_URL

database = Database(DB_URL)
metadata = sqlalchemy.MetaData(database)


todo = sqlalchemy.Table(
    "todo",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False, index=True),
    sqlalchemy.Column("completed", sqlalchemy.Boolean, server_default=expression.false()),
)

engine = sqlalchemy.create_engine(str(DB_URL), connect_args={"check_same_thread": False})
metadata.create_all(engine)
