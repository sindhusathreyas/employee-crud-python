import os
import mysql.connector
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    # Render PostgreSQL
    if os.getenv("DATABASE_URL"):
        return psycopg2.connect(
            os.getenv("DATABASE_URL")
        )

    # Local MySQL
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sindhu@2003",
        database="employee_management"
    )


def get_dict_cursor(connection):
    # PostgreSQL
    if os.getenv("DATABASE_URL"):
        return connection.cursor(cursor_factory=RealDictCursor)

    # MySQL
    return connection.cursor(dictionary=True)

def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()

    if os.getenv("DATABASE_URL"):
        # PostgreSQL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL,
                phone VARCHAR(20),
                department VARCHAR(100) NOT NULL,
                designation VARCHAR(100) NOT NULL,
                salary NUMERIC(12, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        # MySQL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL,
                phone VARCHAR(20),
                department VARCHAR(100) NOT NULL,
                designation VARCHAR(100) NOT NULL,
                salary DECIMAL(12, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    connection.commit()
    cursor.close()
    connection.close()