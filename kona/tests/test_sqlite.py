import sqlite3

def test_sqlite():
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    sql = """
            CREATE TABLE IF NOT EXISTS zx_bank_account(id INTEGER PRIMARY KEY autoincrement
          ,deal_time TEXT,deal_type TEXT,deal_money REAL)"""

    cur.execute(sql)