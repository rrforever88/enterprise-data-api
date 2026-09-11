from app.db.connection import get_connection

def seed_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO companies (name, industry)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
                """,
                ("Acme", "Manufacturing"),
            )

            company = cursor.fetchone()

            if company is None:
                cursor.execute(
                    """
                    SELECT id
                    FROM companies
                    WHERE name = %s
                    """,
                    ("Acme",),
                )
                company = cursor.fetchone()

            company_id = company[0]

            cursor.execute(
                """
                INSERT INTO contacts (company_id, name, email)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                """,
                (
                    company_id,
                    "Jane Smith",
                    "jane@example.com",
                ),
            )

if __name__ == "__main__":
    seed_database()