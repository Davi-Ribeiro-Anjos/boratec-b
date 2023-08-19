import os
import cx_Oracle
from dotenv import load_dotenv

load_dotenv()


def dict_fetchall(cursor):
    columns = [col[0].lower() for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def connect_db():
    try:
        conn = cx_Oracle.connect(
            os.environ.get("ORACLE_USER"),
            os.environ.get("ORACLE_PASSWORD"),
            cx_Oracle.makedsn(
                os.environ.get("ORACLE_HOST"),
                os.environ.get("ORACLE_PORT"),
                None,
                os.environ.get("ORACLE_XE"),
            ),
        )
    except Exception as e:
        print("error  to the db")
        raise e
    else:
        return conn
