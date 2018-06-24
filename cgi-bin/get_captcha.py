#!/usr/bin/python3
import cgitb
import os
import random
from http import cookies

from geetest import GeetestLib

# 获取极验验证 id 和 key，同时生成一个随机用户 id，防止缓存
captcha_id = os.getenv('GEETEST_ID')
private_key = os.getenv('GEETEST_KEY')
user_id = random.randint(1, 1000)

if __name__ == '__main__':
    # 启用 cgi 的错误提示机制，更容易排错
    cgitb.enable()

    # 用户 id 生成，利用随机数防止缓存
    user_id = random.randint(1, 1000)

    # 从 SDK 中获取相关数据
    gt = GeetestLib(captcha_id, private_key)

    # 使用 http.cookies 模块装填 cookies，简单小巧好用
    c = cookies.SimpleCookie()
    c[gt.GT_STATUS_SESSION_KEY] = gt.pre_process(user_id)
    c['user_id'] = user_id

    # 以 json 类型返回，同时加上 cookies
    print(c.output())
    print('Content-type:application/json\n\n')

    # 其他验证数据返回
    print(gt.get_response_str())
