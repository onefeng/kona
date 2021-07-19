import itchat
from itchat.content import *
import xml.etree.ElementTree as ElementTree
import re


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
    item['deal_time'] = re.search(r'交易时间：(.*?)\n', data).group(1) #交易时间
    item['deal_type'] = re.search(r'交易类型：(.*?)\n', data).group(1)  # 交易类型
    item['deal_money'] = re.search(r'交易金额：(.*?)\n', data).group(1)  # 交易金额
    return m.group(1)

s="""
'尊敬的用户：
	您尾号4543的中信储蓄卡

交易时间：7月17日 20:23
交易类型：跨行转入存入-郭松
交易金额：人民币 10.00 元
卡内余额：人民币 3,068.23 元
	

★来中信直播间，看精彩直播，还有福利大转盘，等您抽取好礼>>
'"""
def send_message(content):
    """发送消息"""
    pass


def store_data(data):
    """存入数据"""

    pass


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    """处理消息"""
    # 监听指定微信公众号推送的文章信息
    if itchat.search_mps(name='中信银行')[0]['NickName'] == "中信银行":
        item = parse_data(msg['Content'])
        # 存入数据库
        s = 1


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    # 绑定消息响应事件后，让itchat运行起来，监听消息
    itchat.run()
