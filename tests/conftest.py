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
            cursor.execute("DELETE FROM contacts")
            cursor.execute("DELETE FROM companies")

            cursor.execute(
                """
                INSERT INTO companies (id, name, industry)
                VALUES (%s, %s, %s)
                """,
                (1, "Acme", "Manufacturing"),
            )

    yield