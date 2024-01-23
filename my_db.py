import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='tts_db'
)

def get_all_texts():
    cusor = conn.cursor()
    sql = "SELECT * FROM texts"
    cusor.execute(sql)
    result = cusor.fetchall()
    cusor.close()
    return result

def insert(text):
    cusor = conn.cursor()
    sql = "INSERT INTO texts (text, status) VALUES (%s, 'free')"
    cusor.execute(sql, text)
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

def update_status(id, new_status):
    cusor = conn.cursor()
    sql = "UPDATE texts SET status = %s WHERE id = %s"
    cusor.execute(sql, (new_status, id))
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