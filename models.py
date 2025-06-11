import sqlite3
from utils import convert_ist_to_timezone

DB = 'fitness.db'

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            datetime TEXT,
            instructor TEXT,
            available_slots INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            client_name TEXT,
            client_email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_classes(target_timezone):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT * FROM classes')
    rows = cur.fetchall()
    conn.close()
    
    classes = []
    for row in rows:
        class_datetime = convert_ist_to_timezone(row[2], target_timezone)
        classes.append({
            'id': row[0],
            'name': row[1],
            'datetime': class_datetime,
            'instructor': row[3],
            'available_slots': row[4]
        })
    return classes

def create_booking(class_id, name, email):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT available_slots FROM classes WHERE id=?', (class_id,))
    result = cur.fetchone()
    
    if not result:
        return {'success': False, 'error': 'Class not found'}
    if result[0] <= 0:
        return {'success': False, 'error': 'No available slots'}

    cur.execute('INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)',
                (class_id, name, email))
    cur.execute('UPDATE classes SET available_slots = available_slots - 1 WHERE id=?', (class_id,))
    conn.commit()
    conn.close()
    return {'success': True}

def get_bookings_by_email(email):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
        SELECT classes.name, classes.datetime, classes.instructor
        FROM bookings
        JOIN classes ON bookings.class_id = classes.id
        WHERE bookings.client_email = ?
    ''', (email,))
    rows = cur.fetchall()
    conn.close()
    
    return [{
        'class_name': row[0],
        'datetime': row[1],
        'instructor': row[2]
    } for row in rows]
