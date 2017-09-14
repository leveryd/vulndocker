# 漏洞靶场
一个在线的漏洞测试平台,[示例网站](http://139.199.206.110)

```
1.可以快速启动新的漏洞测试环境
2.可以根据文档复现漏洞，掌握漏洞原理
3.每个用户都是独立的漏洞环境，互不影响测试
```

本项目只在mac和ubuntu 14.04测试通过.

# ubuntu 14.04
## 安装

```
cd vulndocker
apt-get install uwsgi-plugin-python docker.io nginx-core
pip install -r requirements.txt
cp nginx.conf /etc/nginx/sites-enabled/default
#编译项目中的所有镜像,耗时会比较长.特别是有些docker镜像访问国外源
setsid python compile.py &
```

参考

[uwsgi](http://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/WSGIquickstart.html#web)

## 运行

```
#平台需要redis服务
docker run -d -p 6379:6379 redis:latest

#启动
cd vulndocker/

#修改app.py中的ip和port
ip = "127.0.0.1"    #本机ip
webport = 8888      #web端口
ttyport = 9999      #在线docker端口

#启动
uwsgi_python --socket 127.0.0.1:3031 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 &

#添加计划任务
*/2 * * * * python /root/vulndocker/crontab.py
```

## 删除

```
ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
```

# mac
同上