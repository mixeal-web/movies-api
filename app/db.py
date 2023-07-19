# app/extensions/db.py

import os
import mysql.connector


def get_db_connection():
    # Get the database connection details from environment variables
    db_host = os.getenv('MYSQL_HOST')
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_database = os.getenv('MYSQL_DB')

    # Create a MySQL connection
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    return connection
