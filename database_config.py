import databases
import sqlalchemy


# DATABASE_URL = "postgresql+asyncpg://admin:password123456@postgres_db:5432/anti_tik-tok_db"
DATABASE_URL = "sqlite:///anti_tik-tok.db"
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)
