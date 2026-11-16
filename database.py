import sqlite3

DATABASE_NAME = "alumni.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS ALUMNI (
        alumni_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        graduation_year INTEGER,
        degree TEXT,
        major TEXT
    );

    CREATE TABLE IF NOT EXISTS EMPLOYMENT (
        employment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_id INTEGER NOT NULL,
        company_name TEXT NOT NULL,
        job_title TEXT,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY (alumni_id) REFERENCES ALUMNI(alumni_id)
    );

    CREATE TABLE IF NOT EXISTS PROFESSIONAL_AFFILIATION (
        affiliation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_id INTEGER NOT NULL,
        organization_name TEXT NOT NULL,
        position TEXT,
        FOREIGN KEY (alumni_id) REFERENCES ALUMNI(alumni_id)
    );

    CREATE TABLE IF NOT EXISTS MEMBERSHIP (
        membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_id INTEGER NOT NULL,
        membership_type TEXT,
        start_date TEXT,
        expiration_date TEXT,
        FOREIGN KEY (alumni_id) REFERENCES ALUMNI(alumni_id)
    );

    CREATE TABLE IF NOT EXISTS CONTRIBUTION (
        contribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        contribution_date TEXT,
        payment_method TEXT,
        FOREIGN KEY (alumni_id) REFERENCES ALUMNI(alumni_id)
    );

    CREATE TABLE IF NOT EXISTS EVENTS (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_id INTEGER NOT NULL,
        event_name TEXT NOT NULL,
        event_date TEXT,
        location TEXT,
        FOREIGN KEY (alumni_id) REFERENCES ALUMNI(alumni_id)
    );
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")