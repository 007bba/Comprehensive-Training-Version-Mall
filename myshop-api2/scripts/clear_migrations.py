import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parents[0] / '..' / 'db.sqlite3'
db = str(db)
print('DB path:', db)
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='django_migrations'")
if cur.fetchone()[0] == 0:
    print('django_migrations table not found')
else:
    cur.execute('DELETE FROM django_migrations')
    conn.commit()
    print('Cleared django_migrations')
conn.close()
