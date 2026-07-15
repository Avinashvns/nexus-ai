from sqlalchemy import text

from database.base import SessionLocal
from database.init_db import init_database


def main():
    init_database()

    database = SessionLocal()

    try:
        result = database.execute(
            text("SELECT 1")
        )

        value = result.scalar()

        assert value == 1

        print(
            "Database connection successful"
        )

    finally:
        database.close()

    print(
        "\nDatabase Test Passed"
    )


if __name__ == "__main__":
    main()