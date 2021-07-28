import time
import itchat
from itchat.content import *
import xml.etree.ElementTree as ElementTree
import re
import datetime
import sqlite3

from pandas.io import sql

from kona.config.settings import SQLITE_URL, key_word, wechat_name, FILE_PATH
from kona.data_source.sqlite_client import SqliteClient

db = SqliteClient(SQLITE_URL)


def parse_data(text):
    """
    解析xml数据
    :param text:
    :return:
    """
    item = dict()
    rgx = re.compile(r"\<des\>\<\!\[CDATA\[(.*?)\]\]\>", re.S)
    m = rgx.search(text)
    data = m.group(1)
    # 收入关键词
    income_words = ['转入', '存入']
    # 支出关键词
    expand_words = ['转出', '收费']
    # 提取字段
    deal_time = re.search(r'交易时间：(.*?)\n', data).group(1)  # 交易时间

    item['abstract_txt'] = re.search(r'交易类型：(.*?)\n', data).group(1)  # 摘要
    item['deal_type'] = re.search(r'交易类型：(.*?)\n', data).group(1)  # 交易类型
    is_income = any(e in item['abstract_txt'] for e in income_words)
    is_expand = any(e in item['abstract_txt'] for e in expand_words)
    item['deal_type'] = '未知'
    a = 1
    if is_income:
        item['deal_type'] = '收入'
    if is_expand:
        item['deal_type'] = '支出'
        a = -1

    deal_money = re.search(r'交易金额：(.*?)\n', data).group(1)  # 交易金额
    now_time = datetime.datetime.now().year
    item['deal_time'] = str(now_time) + '年' + deal_time
    item['deal_money'] = a * float(re.search(r'人民币(.*?)元', deal_money).group(1))
    return item, data


def send_message(content):
    """发送消息"""
    name = itchat.search_friends(name=wechat_name)
    user_name = name[0]["UserName"]
    itchat.send(content, user_name)


def to_file():
    con = db.get_conn()
    model = sql.read_sql('select * from zx_bank_account', con)
    now_time = str(int(time.time()))
    file_path = FILE_PATH + 'zx_bank_account{}.xlsx'.format(now_time)
    model.to_excel(file_path, engine='openpyxl', encoding='utf8')
    return file_path


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    """处理消息"""
    # 监听指定微信公众号推送的文章信息
    nick_name = msg['User']['NickName']  # 获取微信公众号名
    if nick_name == "中信银行":
        item, data = parse_data(msg['Content'])
        # 存入数据库
        db.insert('zx_bank_account', item)
        # 发送消息
        send_message(data)


@itchat.msg_register([TEXT])
def message_reply(msg):
    """回复"""
    text = msg['Text']
    remark_name = msg['User']['RemarkName']
    to_user_name = msg['ToUserName']
    if text == key_word and remark_name == wechat_name:
        file_path = to_file()
        itchat.send_file(file_path, to_user_name)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()