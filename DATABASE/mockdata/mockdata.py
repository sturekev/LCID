# for generating random database
# import bcrypt
import hashlib
import random
import secrets
import string

from mockdata.hash import *

account_mockdata = [
    {
        'full_name': 'Samuel Vue',
        'username': 'vuesa01',
        # 'password': "$2b$12$dBkFNwcwUmYbxyYFDbad/OYLhKJvJkupwSr8zF00MbVr8ClK22tWi"
        'password': f"{encodePassword('password1')}"
    },
    {
        'full_name': 'Reece Flynn',
        'username': 'flynre01',
        # 'password': "$2b$12$PynlC8EP2DdQa5qCOmwqNuXEAPfN63YEHMRZ5dek9QMMXVcCOQzRW"
        'password': f"{encodePassword('password2')}"
    },
    {
        'full_name': 'Kevin Tu',
        'username': 'tuph01',
        # 'password': "$2b$12$qkqpaQpL.heDesoTJKRFgOWyacjPhYOq.7t4mwZIGAdfeaUgU7vgy"
        'password': f"{encodePassword('password3')}"
    }
]

building_info_mockdata = [
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

account_profile_mockdata = [
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

meal_plan_mockdata = [
    {
        'account_id': 1,
        'role': 'Student',
        'swipes_remaining': random.randint(0, 19), # assumes a weekly swipe meal plan
        'dining_dollars': round(random.uniform(0.00, 250.00), 2), # assumes a 19 meal week plan
        'meal_plan': 'Normal'   # not sure how we want this fully implemented yet, 
                                # just a placeholder which probably works fine
    },
    {
        'account_id': 2,
        'role': 'Student',
        'swipes_remaining': random.randint(0, 19),
        'dining_dollars': round(random.uniform(0.00, 250.00), 2),
        'meal_plan': 'Normal'
    },
    {
        'account_id': 3,
        'role': 'Student',
        'swipes_remaining': random.randint(0, 19),
        'dining_dollars': round(random.uniform(0.00, 250.00), 2),
        'meal_plan': 'Normal'
    }
]

# def hash_password(password):
#     password_bytes = password.encode('utf-8')
#     hashed_password = hashlib.sha256(password_bytes).digest()
#     return hashed_password


def generate_random_string(length):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_mockdata_account(db_connection):
    db_cursor = db_connection.cursor()
    
    insert_query = """INSERT INTO account (fullname, username, password)
                        VALUES (%s, %s, %s)"""
    
    for aRecord in account_mockdata:
        record = (aRecord["full_name"], aRecord["username"], aRecord["password"])
        db_cursor.execute(insert_query, record)

    return db_connection

def create_mockdata_building_info(db_connection):
    db_cursor = db_connection.cursor()

    insert_query = """INSERT INTO building_info (building_name)
                        VALUES (%s)"""
    
    for aRecord in building_info_mockdata:
        record = (aRecord["building"],)
        db_cursor.execute(insert_query, record)

    return db_connection


def generate_random_user_token():
    user_token = secrets.token_bytes(32)
    return user_token

def create_mockdata_account_profile(db_connection):
    db_cursor = db_connection.cursor()

    insert_query = """INSERT INTO account_profile (id_number, account_id, user_token, housing)
                        VALUES (%s, %s, %s, %s)"""
    
    for aRecord in account_profile_mockdata:
        user_token = generate_random_user_token()
        record = (aRecord["id_number"], aRecord["account_id"], user_token, aRecord["housing"])
        db_cursor.execute(insert_query, record)

    return db_connection

def create_mockdata_meal_balance(db_connection):
    db_cursor = db_connection.cursor()

    insert_query = """INSERT INTO meal_balance (account_id, role, swipes_remaining, dining_dollars, meal_plan)
                        VALUES (%s, %s, %s, %s, %s)"""
    
    for aRecord in meal_plan_mockdata:
        record = (aRecord["account_id"], aRecord["role"], aRecord["swipes_remaining"], aRecord["dining_dollars"], aRecord["meal_plan"])
        db_cursor.execute(insert_query, record)
    
    return db_connection
    