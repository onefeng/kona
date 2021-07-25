import time

import pandas.io.sql as sql

from kona.config.settings import SQLITE_URL, FILE_PATH
from kona.data_source.sqlite_client import SqliteClient


def test_write():
    con = SqliteClient(SQLITE_URL).get_conn()
    model = sql.read_sql('select * from zx_bank_account', con)
    now_time = str(int(time.time()))
    model.to_excel(FILE_PATH+'zx_bank_account{}.xlsx'.format(now_time),engine='openpyxl',encoding='utf8')
    assert True