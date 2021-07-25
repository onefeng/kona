import sqlite3

db = sqlite3.connect("release.db")
cur = db.cursor()
sql = """
            CREATE TABLE IF NOT EXISTS zx_bank_account(id INTEGER PRIMARY KEY autoincrement
          ,deal_time TEXT,deal_type TEXT,deal_money REAL)"""

cur.execute(sql)
