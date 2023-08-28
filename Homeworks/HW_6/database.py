import databases
import sqlalchemy
from sqlalchemy import ForeignKey
from settings import settings

db = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

products = sqlalchemy.Table("products", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("product_name", sqlalchemy.String(100)),
                            sqlalchemy.Column("description", sqlalchemy.String(1000)),
                            sqlalchemy.Column("price", sqlalchemy.Integer)
                            )


orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
                          sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id")),
                          sqlalchemy.Column("date", sqlalchemy.String),
                          sqlalchemy.Column("status", sqlalchemy.String(20))
                          )

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
