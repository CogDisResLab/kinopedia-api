import sqlite3

conn = sqlite3.connect('kinopedia.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM kinases")
count = cursor.fetchone()[0]
print(f"Database connected! Found {count} kinases")

cursor.execute("SELECT hgnc_symbol FROM kinases")
kinases = cursor.fetchall()
print(f"Kinases: {', '.join([k[0] for k in kinases])}")

conn.close()