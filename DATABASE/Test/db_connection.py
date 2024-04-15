import psycopg2

from db_config import get_db_info

local_db_name='db_info.ini'
section='cardReaderDB'
db_info = get_db_info(local_db_name, section)

aws_db_name='aws_db_info.ini'
aws_db_info = get_db_info(aws_db_name, section)

def get_db_connection():
    return psycopg2.connect(**db_info)

def get_aws_db_connection():
    return psycopg2.connect(**aws_db_info)