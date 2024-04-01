import psycopg2

from db_config import get_db_info

filename='db_info.ini'
section='cardReaderDB'
db_info = get_db_info(filename, section)

filename2='aws_db_info.ini'
aws_db_info = get_db_info(filename2, section)

def get_db_connection():
    return psycopg2.connect(**db_info)

def get_aws_db_connection():
    return psycopg2.connect(**aws_db_info)