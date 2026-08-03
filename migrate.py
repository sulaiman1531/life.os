import sqlite3
try:
    conn = sqlite3.connect('lifeos.db')
    conn.execute('ALTER TABLE tasks ADD COLUMN project_id VARCHAR')
    conn.commit()
    conn.close()
    print("Migration successful")
except Exception as e:
    print(e)
