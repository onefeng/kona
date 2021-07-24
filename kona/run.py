import itchat
from itchat.content import *
import xml.etree.ElementTree as ElementTree
import re
import datetime
import sqlite3

from kona.config.settings import SQLITE_URL, key_word, send_id
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
    # 提取字段
    deal_time = re.search(r'交易时间：(.*?)\n', data).group(1)  # 交易时间
    item['deal_type'] = re.search(r'交易类型：(.*?)\n', data).group(1)  # 交易类型
    deal_money = re.search(r'交易金额：(.*?)\n', data).group(1)  # 交易金额
    now_time = datetime.datetime.now().year
    item['deal_time'] = str(now_time) + '年' + deal_time
    item['deal_money'] = float(re.search(r'人民币(.*?)元', deal_money).group(1))
    return item, data


def send_message(content):
    """发送消息"""
    itchat.send(content, send_id)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    """处理消息"""
    # 监听指定微信公众号推送的文章信息
    if itchat.search_mps(name='中信银行')[0]['NickName'] == "中信银行":
        item, data = parse_data(msg['Content'])
        # 存入数据库
        db.insert('zx_bank_account', item)
        # 发送消息
        send_message(data)


@itchat.msg_register([TEXT])
def message_reply(msg):
    """回复"""
    text = msg['Text']
    if text == key_word:
        itchat.send('hhh', 'gs199534')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    # 绑定消息响应事件后，让itchat运行起来，监听消息
    itchat.run()
