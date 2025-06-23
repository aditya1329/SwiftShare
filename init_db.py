import sqlite3

conn = sqlite3.connect('swiftshare.db')
cursor = conn.cursor()

# ⚠️ Delete old table (if testing)
cursor.execute("DROP TABLE IF EXISTS files")

# ✅ Recreate table with required fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uploader TEXT NOT NULL,
        filename TEXT NOT NULL,
        passcode TEXT NOT NULL,
        timestamp TEXT,
        status TEXT,
        downloaded INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()

print("✅ Recreated 'files' table with downloaded field and no UNIQUE on passcode.")
