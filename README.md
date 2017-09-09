# 17.8.27
前端markdown渲染,修改成后端markdown.使用github的css
# 17.7.31
> vuln下的desc描述文件,也可以使用jinjia模板啦.

# 部署
>[nginx+uwsgi] http://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/WSGIquickstart.html#web

> ## uwsgi安装

> `pip install uwsgi`

> ubuntu

> `apt-get install uwsgi-plugin-python`

> `uwsgi_python --socket 127.0.0.1:3031 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 &`

> 替换掉nginx默认配置

> 需要一个redis服务,密码是test@test123,在本地监听

>

> pkill -f u

> ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9

> 安装docker服务

> 一些漏洞环境用到数据库的 `docker run -p 3306:3306 -d -e MYSQL_DATABASE=test -e MYSQL_USER=fscan -e MYSQL_PASSWORD=fscan123 -e MYSQL_ROOT_PASSWORD=fscan123 mysql`


额外的
> highlight.js  语法高亮 http://www.gonjay.com/blog/2014/07/11/markdownde-chun-qian-duan-jie-jue-fang-an/

