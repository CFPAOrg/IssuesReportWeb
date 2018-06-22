#!/usr/bin/python3
import cgi
import cgitb
import codecs
import os
import sys

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

    # cgi 默认输出似乎是系统编码，这里得强制指定下，虽然最后服务器会在 linux 系统上
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

    # 用户得到的界面
    print(header, ''.join(html).format(html_url, html_url))
