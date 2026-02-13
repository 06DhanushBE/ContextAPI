import sqlite3

conn = sqlite3.connect('contextapi.db')
try:
    conn.execute('ALTER TABLE api_keys ADD COLUMN llm_provider TEXT DEFAULT "groq"')
    conn.commit()
    print('Column llm_provider added successfully')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Column llm_provider already exists')
    else:
        print(f'Error: {e}')
finally:
    conn.close()
