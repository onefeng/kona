import sqlite3
import logging

import pandas as pd
from DBUtils.PersistentDB import PersistentDB


class SqliteClient(object):
    def __init__(self, db_path):
        self._pool = PersistentDB(sqlite3, maxusage=None, threadlocal=None, closeable=False, database=db_path)

    def get_conn(self):
        return self._pool.connection()

    def query(self, sql):
        results = ()
        try:
            db = self.get_conn()
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            logging.exception(e)
        finally:
            return results

    def noquery(self, sql):
        flag = False
        try:
            db = self.get_conn()
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            logging.exception(e)
        finally:
            return flag

    def insert(self, table, datas={}):
        flag = False
        try:
            db = self.get_conn()
            cursor = db.cursor()
            keys = ','.join(datas.keys())
            values = ','.join(['?'] * len(datas))
            sql = "insert into {table}({keys}) values {values}".format(table=table, keys=keys, values=tuple(datas.values()))
            # print(sql)
            cursor.execute(sql, tuple(datas.values()))
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            db.rollback()
            logging.exception(e)
        finally:
            return flag


class SqliteFrame(object):
    """pandas handler sqlite database"""

    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def get_conn(self):
        return self.con

    def sqlite_to_df(self, sql):
        """read sqlite to DataFrame"""
        con = self.get_conn()
        cursor = con.cursor()
        values = cursor.execute(sql)
        df = pd.DataFrame(data=values)
        cursor.close()
        con.close()
        return df

    def df_to_sqlite(self, name, df):
        """write DataFrame to sqlite"""
        con = self.get_conn()
        df.to_sql(name, con, if_exists='replace')
        con.close()
        return name
