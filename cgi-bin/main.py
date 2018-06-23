#!/usr/bin/python3
import cgi
import cgitb
import codecs
import os
import sys
import sqlite3
import time
import re

import github

if __name__ == '__main__':
    # 启用 cgi 的错误提示机制，更容易排错
    cgitb.enable()

    # 获取玩家丢来的数据
    form = cgi.FieldStorage()

    # 标题获取
    title = form['title'].value

    # 标签获取，因为可以为空，也可能是数组，判定较为复杂
    tags = []
    try:
        tags = form['inlineCheckbox'].value
    except AttributeError:
        for i in form['inlineCheckbox']:
            tags.append(i.value)
    except KeyError:
        pass

    # 模组信息，可以为空
    mod_info = ''
    try:
        mod_info = form['modinfo'].value
    except KeyError:
        pass

    # 邮箱获取
    email_in = form['email'].value
    # 邮箱后端校验，防止 SQL 注入攻击
    email_match = re.findall(r'^[\w.\-]+@(?:[a-z0-9]+(?:-[a-z0-9]+)*\.)+[a-z]{2,3}$', email_in)
    if len(email_match) > 0:
        email = email_match[0]
    else:
        email = 'null@null.nul'

    # 问题本体
    body = form['body'].value

    # 读取返回的网页文件
    with open('./return.html', 'r', encoding='utf-8') as f:
        html = []
        for i in f.readlines():
            html.append(i)

    # 返回数据头
    header = 'Content-Type: text/html\n\n'

    # 开始登陆 GitHub，使用环境变量中存储的 token
    g = github.Github(os.getenv('GITHUB_TOKEN'))

    # 跳转指定组织，指定仓库
    repo = g.get_organization("CFPAOrg").get_repo("cfpaorg.github.io")

    # label 映射，将玩家反馈数据和 GitHub 的 label 进行联系
    label = repo.get_labels()  # 获取 GitHub 的标签
    issues_label = []  # 存玩家提交的标签
    if 'tags1' in tags:
        issues_label.append(label[2])
    if 'tags2' in tags:
        issues_label.append(label[1])
    if 'tags3' in tags:
        issues_label.append(label[0])

    # mod_info 不为空，组装到 body 里面
    if mod_info:
        body = '```\n{}\n````\n{}'.format(mod_info, body)

    # 发 Issues
    issue = repo.create_issue(title=title, body=body, labels=issues_label)

    # 得到反馈的网址
    html_url = issue.html_url

    # 数据存储，一来对问题进一步回溯，二来防止有人捣乱
    ip = os.getenv('REMOTE_ADDR')
    time_index = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 开始连接数据库，存储位置为上级文件夹，那么外部无法访问到
    conn = sqlite3.connect('../issues.db')

    # 创建游标
    cursor = conn.cursor()

    # 不存在表时，创建表
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS ISSUES '
        '(TIME TEXT PRIMARY KEY NOT NULL, '
        'EMAIL TEXT NOT NULL, '
        'IP TEXT NOT NULL, '
        'URL TEXT NOT NULL);')
    conn.commit()

    # 开始执行数据存储，出现错误则回滚
    try:
        cursor.execute("INSERT INTO ISSUES "
                       "(TIME, EMAIL, IP, URL) "
                       "VALUES ('{}', '{}', '{}', '{}')".format(time_index, email, ip, html_url))
        conn.commit()
    except sqlite3.Error:
        conn.rollback()

    # 关闭数据库
    conn.close()

    # cgi 默认输出似乎是系统编码，这里得强制指定下，虽然最后服务器会在 linux 系统上
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

    # 用户得到的界面
    print(header, ''.join(html).format(html_url, html_url))
