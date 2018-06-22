# 自动 Issues 转发系统

### 为什么我做了这个？
因为 GitHub 是目前最好用的的问题反馈系统，然而让玩家直接通过 GitHub 反馈问题违背了 KISS 原则。相信我，这样能够获得更多的正面反馈。  
基于 Python3 cgi 构建的后端；前端采用了 Bootstrap，font-awesome， showdown 框架和工具，在此表示感谢。

### 需要修改哪些内容，如何运行？
- 自动推送机器使用了 PyGithub 模块，需要进行安装；
- 需要添加一个 `GITHUB_TOKEN` 的环境变量，用来存储 GitHub 的 Token；
- 需要修改 `cgi-bin` 下的 `main.py` 的这一处：
    ```python
    repo = g.get_organization("CFPAOrg").get_repo("cfpaorg.github.io")
    ```
- 最后执行 `./run.sh`，里面的端口也需要修改（那个 `8000` 就是端口）。
