import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

DB_NAME = "ALX_prodev"

TABLES = {
    "user_data": (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "  user_id VARCHAR(36) PRIMARY KEY, "
        "  name VARCHAR(255) NOT NULL, "
        "  email VARCHAR(255) NOT NULL, "
        "  age DECIMAL(3, 0) NOT NULL, "
        "  INDEX(user_id)"
        ") ENGINE=InnoDB"
    )
}


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="*******"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print("Database created or already exists")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password_here",
            database=DB_NAME,
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(TABLES["user_data"])
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    cursor = connection.cursor()
    try:
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(float(row["age"]))

                # Check if email already exists to avoid duplicates
                cursor.execute("SELECT email FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue  # Skip existing entry

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age),
                )
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
