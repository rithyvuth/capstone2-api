import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST", 'localhost')
db_user = os.getenv("DB_USER", 'root')
db_password = os.getenv("DB_PASSWORD", 'root')
db_database = os.getenv("DB_DATABASE", 'tts_db')
conn = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database,
)

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
    sql = "SELECT id, text, status FROM texts WHERE status = 'free' ORDER BY id ASC LIMIT 1"
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
