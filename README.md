# 自动 Issues 转发系统

### 为什么我做了这个？
因为 GitHub 是目前最好用的的问题反馈系统，然而让玩家直接通过 GitHub 反馈问题违背了 KISS 原则。相信我，这样能够获得更多的正面反馈。  
基于 Python3 cgi 构建的后端；前端采用了 bootstrap，font-awesome，showdown 框架；后端采用了极验验证，Nginx，uWSGI 等工具，在此表示感谢。

### 需要修改哪些内容，如何运行？
- 自动推送机器使用了 `PyGithub` 模块，需要进行安装；

- 采用了 `SQLite` 数据库，需要自行安装；

- 需要添加一个 `GITHUB_TOKEN` 的环境变量，用来存储 GitHub 的 Token；

- 需要添加 `GEETEST_ID`，`GEETEST_KEY` 环境变量，存储极验验证给的 id 和 key；

- 需要修改 `cgi-bin` 下的 `main.py` 的这一处：
    ```python
    repo = g.get_organization("CFPAOrg").get_repo("cfpaorg.github.io")
    ```

- 数据库被放置在网站上级目录中的 `database` 文件夹中，需要自行创建。这么做是因为可以访问到网站所在目录下文件，放置在上级目录中就无法访问了。

### 如何通过 Nginx 和 uWSGI 运行服务端？

实际上这个服务器后端没有使用任何 Python 框架，只用了原生的 cgi 模块，大部分教程似乎都是基于 Django 或者 Flask 框架的，一到原生脚本就捉急了。好在我多方寻找答案，总算解决了这个问题，现把解决方案总结如下：

首先，在安装好 Nginx 以后，你需要安装 uWSGI 模块，uWSGI 模块有简体中文的官方文档，讲解的很详细。

> 官方文档：<http://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/index.html>

这个模块在官方文档上讲解了多种安装方式。然而源码安装太繁琐，使用 pip 安装后，运行会报错：

```
!!! UNABLE to load uWSGI plugin: ./python_plugin.so: cannot open shared object file: No such file or directory !!!
```

好在 Ubuntu论坛上有人提供了简单的 apt 安装方法，非常好用。

> 解决方案来源：<https://askubuntu.com/questions/227940/uwsgi-cant-find-python-plugin>

```shell
sudo apt-get install uwsgi-plugin-python3
```

安装好以后，直接通过 `uwsgi` 指令就可开启 uwsgi 服务。

任何服务都需要配置文件。我们需要修改 Nginx 的配置，让它连接到 cgi 服务上，同时我们需要给 uwsgi 指定一个配置，让其能够按照要求进行服务的开启。

在任意位置创建一个配置文件，文件名随意，这里我们命名为 `uwsgi_config.ini`，内部写入：

```ini
[uwsgi]
;使用 cgi
plugins=cgi
;将服务开放在 localhost，9000端口上，可自定义
socket=127.0.0.1:9000
;跳转到 cgi-bin 文件夹路径
chdir=/var/www/cgi-bin/
;开始进行 cgi 文件指定
cgi=/cgi-bin=/var/www/cgi-bin/
;使用 python3 进行运行
cgi-helper=.py=python3
```

输入 `uwsgi --ini xxx/uwsgi_config.ini` 就行，最后面的参数指定的是这个配置文件的地址。

然后是修改 Nginx 配置文件，一般为 `etc/nginx/sites-enabled/deafult` 文件，加入这一段：

```javascript
location /cgi-bin {
		# 引入 uwsgi_params 文件
		include uwsgi_params;
		# 对当前 location 的请求进行 cgi 脚本处理
		uwsgi_modifier1 9;
		# TCP 连接方式，要和之前 uwsgi 运行端口一致，才能进行通信
		uwsgi_pass 127.0.0.1:9000;
	}
```

保存后，输入 `nginx -s reload` 重载服务端即可。

感谢 CSDN 上面的博客对搭建的指导

> 来源：<https://blog.csdn.net/xlisper/article/details/36703955>

