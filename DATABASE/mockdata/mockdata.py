import random
import secrets

from mockdata.hash import *

account_data = [
    {
        'full_name': 'Samuel Vue',
        'username': 'vuesa01',
        'password': f"{encode_password('password1')}"
    },
    {
        'full_name': 'Reece Flynn',
        'username': 'flynre01',
        'password': f"{encode_password('password2')}"
    },
    {
        'full_name': 'Kevin Tu',
        'username': 'tuph01',
        'password': f"{encode_password('password3')}"
    }
]

building_info_data = [
    {
        'building': 'Farwell'
    },
    {
        'building': 'Olson'
    },
    {
        'building': 'Diseth'
    },
    {
        'building': 'Miller'
    },
    {
        'building': 'Brandt'
    },
    {
        'building': 'Ylvisaker'
    },
    {
        'building': 'Baker Village'
    },
    {
        'building': 'College Apartments'
    },
    {
        'building': 'Larsen'
    },
    {
        'building': 'Prairie Houses'
    },
    {
        'building': 'Sustainability House'
    },
    {
        'building': 'Off-Campus Living'
    },
    {
        'building': 'Roth'
    }
]

account_profile_data = [
    {
        'id_number': '528480',
        'account_id': 1,
        'user_token': 'Mason',
        'housing': 1,
    },
    {
        'id_number': '527836',
        'account_id': 2,
        'user_token': 'Reece',
        'housing': 8,
    },
    {
        'id_number': '529194',
        'account_id': 3,
        'user_token': 'Kevin',
        'housing': 4,
    }
]

meal_plan_data = [
    {
        'account_id': 1,
        'role': 'Student',
        'swipes_remaining': 100,
        'dining_dollars': round(random.uniform(0.00, 250.00), 2), 
        'meal_plan': 'Normal'
    },
    {
        'account_id': 2,
        'role': 'Student',
        'swipes_remaining': 100,
        'dining_dollars': round(random.uniform(0.00, 250.00), 2),
        'meal_plan': 'Normal'
    },
    {
        'account_id': 3,
        'role': 'Student',
        'swipes_remaining': 100,
        'dining_dollars': round(random.uniform(0.00, 250.00), 2),
        'meal_plan': 'Normal'
    }
]

def create_account_data(db_connection):
    db_cursor = db_connection.cursor()
    
    insert_query = """INSERT INTO account (fullname, username, password)
                        VALUES (%s, %s, %s)"""
    
    for record in account_data:
        record = (record["full_name"], record["username"], record["password"])
        db_cursor.execute(insert_query, record)

    return db_connection

def create_building_info_data(db_connection):
    db_cursor = db_connection.cursor()

    insert_query = """INSERT INTO building_info (building_name)
                        VALUES (%s)"""
    
    for record in building_info_data:
        record = (record["building"],)
        db_cursor.execute(insert_query, record)

    return db_connection


def generate_random_user_token():
    user_token = secrets.token_bytes(32)
    return user_token

def create_account_profile_data(db_connection):
    db_cursor = db_connection.cursor()

    insert_query = """INSERT INTO account_profile (id_number, account_id, user_token, housing)
                        VALUES (%s, %s, %s, %s)"""
    
    for record in account_profile_data:
        user_token = generate_random_user_token()
        record = (record["id_number"], record["account_id"], user_token, record["housing"])
        db_cursor.execute(insert_query, record)

    return db_connection

def create_meal_balance_data(db_connection):
    db_cursor = db_connection.cursor()

    insert_query = """INSERT INTO meal_balance (account_id, role, swipes_remaining, dining_dollars, meal_plan)
                        VALUES (%s, %s, %s, %s, %s)"""
    
    for record in meal_plan_data:
        record = (record["account_id"], record["role"], record["swipes_remaining"], record["dining_dollars"], record["meal_plan"])
        db_cursor.execute(insert_query, record)
    
    return db_connection
    