import sqlite3
import os

def init_db():
    os.makedirs('database',exist_ok=True)
    conn = sqlite3.connect('database/court_data.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS queries (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       case_type TEXT,
                       case_number TEXT,
                       filling_year TEXT,
                       response TEXT,
                       timestamp DATATIME DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    init_db()
    print('Databse initialize and ready')