import sqlite3
from datetime import datetime, timedelta

DB = 'fitness.db'

classes = [
    ('Yoga', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 09:00:00'), 'Asha', 10),
    ('Zumba', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 17:00:00'), 'Ravi', 8),
    ('HIIT', (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d 07:00:00'), 'Nina', 5)
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executemany('INSERT INTO classes (name, datetime, instructor, available_slots) VALUES (?, ?, ?, ?)', classes)
conn.commit()
conn.close()
