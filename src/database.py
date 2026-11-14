import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text as sql_text

load_dotenv()

required = ["DB_USER", "DB_PASSWORD", "DB_NAME"]
missing = [name for name in required if not os.getenv(name)]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

engine = create_engine(url, pool_pre_ping=True)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(sql_text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
   if test_connection():
       print("Database connection successful.")