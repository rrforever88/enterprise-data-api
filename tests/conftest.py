import os
import pytest

from app.db.connection import get_connection

os.environ["DATABASE_URL"] = (
    "postgresql://appuser:apppassword@localhost:5432/enterprise_data_test"
)

@pytest.fixture(autouse=True)
def reset_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE contacts, companies
                RESTART IDENTITY CASCADE
                """
            )

            cursor.execute(
                """
                INSERT INTO companies (name, industry)
                VALUES (%s, %s)
                """,
                ("Acme", "Manufacturing"),
            )

    yield