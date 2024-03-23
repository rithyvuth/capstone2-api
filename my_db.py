import pymysql
import os
from dotenv import load_dotenv
from dbutils.pooled_db import PooledDB

load_dotenv()

db_host = os.getenv("DB_HOST", 'localhost')
db_user = os.getenv("DB_USER", 'root')
db_password = os.getenv("DB_PASSWORD", 'root')
db_database = os.getenv("DB_DATABASE", 'tts_db')
# conn = pymysql.connect(
#     host=db_host,
#     user=db_user,
#     password=db_password,
#     database=db_database,
# )
db_config = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': db_database,
    'autocommit': True
}

connection_pool = PooledDB(creator=pymysql, mincached=0, maxcached=0, **db_config)
conn = connection_pool.connection()

def get_all_texts():
    cusor = conn.cursor()
    sql = "SELECT * FROM texts"
    cusor.execute(sql)
    result = cusor.fetchall()
    cusor.close()
    return result

def findText(text):# return true or false
    cusor = conn.cursor()
    sql = "SELECT * FROM texts WHERE text = %s"
    cusor.execute(sql, (text))
    result = cusor.fetchone()
    cusor.close()
    
    if result is None:
        return False
    return True

def insert(text, filename=None):
    if text == '' or findText(text):
        return None
    cusor = conn.cursor()
    sql = "INSERT INTO texts (text, status, from_file) VALUES (%s, 'free', %s)"
    cusor.execute(sql, (text, filename))
    conn.commit()
    cusor.close()
    
    return cusor.lastrowid

def get_text():
    cusor = conn.cursor()
    sql = "SELECT id, text, status FROM texts WHERE status = 'free' AND user_id IS NULL ORDER BY id ASC LIMIT 1"
    cusor.execute(sql)
    result = cusor.fetchone()
    cusor.close()
    if result is None:
        return [None, None, None]
    
    update_status(result[0], 'busy')
    
    return result

def update_status(id, new_status, filename = None):
    cusor = conn.cursor()
    sql = "UPDATE texts SET status = %s, wav_name = %s WHERE id = %s"
    cusor.execute(sql, (new_status, filename, id))
    conn.commit()
    cusor.close()
    return cusor.lastrowid

def status_to_free():
    cusor = conn.cursor()
    sql = "UPDATE texts SET status = 'free' WHERE status = 'busy'"
    cusor.execute(sql)
    conn.commit()
    cusor.close()
    
    return cusor.lastrowid

def test_get_text():
    cusor = conn.cursor()
    sql = "SELECT id, text, status FROM texts ORDER BY id ASC LIMIT 1"
    cusor.execute(sql)
    result = cusor.fetchone()
    
    cusor.close()
    
    return result


def get_users():
    cusor = conn.cursor()
    sql = "SELECT * FROM users"
    cusor.execute(sql)
    result = cusor.fetchall()
    cusor.close()
    
    return result

def get_texts_by_user_id(id):
    cusor = conn.cursor()
    sql = "SELECT id, text FROM texts WHERE user_id = %s and status = 'free'"
    cusor.execute(sql, (id))
    result = cusor.fetchall()
    cusor.close()
    if result is None:
        return []
    
    return result

def get_text_by_user_id(id):
    cusor = conn.cursor()
    sql = "SELECT id, text FROM texts WHERE user_id = %s and status = 'free' ORDER BY id ASC LIMIT 1"
    cusor.execute(sql, (id))
    result = cusor.fetchone()
    cusor.close()
    if result is None:
        return [None, None, None]
    id = result[0]
    update_status(id, 'busy')
    
    return result

# get id of the first 200 free status texts
def get_free_texts_id(n_text = 220):
    cusor = conn.cursor()
    sql = "SELECT id FROM texts WHERE status = 'free' and user_id IS NULL ORDER BY id ASC LIMIT %s"
    cusor.execute(sql, (n_text))
    result = cusor.fetchall()
    cusor.close()
    
    # return as list of ids 1, 2, 3, 4, ...
    return [x[0] for x in result]

def assign_text_to_user(user_id):
    cusor = conn.cursor()
    count_user_text_left = len(get_texts_by_user_id(user_id))
    if 220 - count_user_text_left <= 0:
        conn.commit()
        cusor.close()
        return None
    free_text = get_free_texts_id(220 - count_user_text_left)
    if len(free_text) == 0:
        conn.commit()
        cusor.close()
        return None
    sql = "UPDATE texts SET user_id = %s WHERE id = %s"
    for id in free_text:
        cusor.execute(sql, (user_id, id))
    conn.commit()
    cusor.close()
    
    return cusor.lastrowid

def add_user(name):
    cusor = conn.cursor()
    sql = "INSERT INTO users (name) VALUES (%s)"
    cusor.execute(sql, (name))
    conn.commit()
    cusor.close()
    
    return cusor.lastrowid

def update_text(id, newText):
    cusor = conn.cursor()
    sql = "UPDATE texts SET text = %s WHERE id = %s"
    cusor.execute(sql, (newText, id))
    conn.commit()
    cusor.close()
    
    return cusor.lastrowid
from text_normalization import text_normalize
def normalize_text():
    cusor = conn.cursor()
    sql = "SELECT id, text FROM texts WHERE status = 'free'"
    cusor.execute(sql)
    result = cusor.fetchall()
    for id, text in result:
        normalized_text = text_normalize(text, text_token_by_space=True)
        update_text(id, normalized_text)
    cusor.close()
    
    return cusor.lastrowid

#normalize_text()