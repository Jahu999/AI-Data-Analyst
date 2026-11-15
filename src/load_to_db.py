from src.database import engine
from src.data_loader import load_data
from src.data_cleaning import clean_data
from sqlalchemy import text

def main():
    df = clean_data(load_data())

    df.to_sql(
        name="sales",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi"
    )

    print(f"Zapisano {len(df)} wierszy do PostgreSQL.")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM sales"))

    db_count = result.scalar_one()

    print(f"DataFrame rows: {len(df)}")
    print(f"Database rows: {db_count}")

    if len(df) == db_count:
        print("Data validation: PASSED")
    else:
        print("Data validation: FAILED")

if __name__ == "__main__":
    main()