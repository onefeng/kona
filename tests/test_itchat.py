import itchat


def test_itchat():
    import itchat
    # 登录（只需要扫码一次，第二次运行手机微信会弹出确认框）
    itchat.auto_login(hotReload=True)
    # 登录（每次登录都要扫二维码）
    # itchat.login()

    mpsList = itchat.get_mps(update=True)[1:]

    assert True


def test_send():
    s = '🐰 '
    itchat.auto_login(hotReload=True)
    name = itchat.search_friends(name=s)
    user_name = name[0]["UserName"]
    assert True


def test_send_file():
    path = "E:\pro_code\kona\kona\scrips\zx_bank_account1627309223.xlsx"
    itchat.auto_login(hotReload=True)
    itchat.send_file(path, 'filehelper')
