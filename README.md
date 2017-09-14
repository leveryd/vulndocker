# ubuntu 14.04
## 安装

```
apt-get install uwsgi-plugin-python docker.io nginx-core
pip install -r requirements.txt

[替换掉nginx默认配置](http://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/WSGIquickstart.html#web)
cp nginx.conf /etc/nginx/sites-enabled/default
```

## 运行

```
docker run -d -p 6379:6379 redis:latest

cd vulndocker/
uwsgi_python --socket 127.0.0.1:3031 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 &

添加计划任务
*/2 * * * * python /root/vulndocker/crontab.py
```

## 删除

```
ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
```

# mac
同上