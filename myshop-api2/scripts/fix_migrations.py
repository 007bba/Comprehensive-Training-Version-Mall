import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parents[0] / '..' / 'db.sqlite3'
db = str(db)
print('DB path:', db)
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
rows = cur.fetchall()
print('migrations before:', rows[:20])
# Remove admin entries to allow users migration to apply first
cur.execute("DELETE FROM django_migrations WHERE app='admin'")
conn.commit()
cur.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
rows2 = cur.fetchall()
print('migrations after:', rows2[:20])
conn.close()
