# 心脏出血漏洞（CVE-2014-0160）测试环境

编译运行：

```
docker-compose build
docker-compose up -d
```

访问`https://filippo.io/Heartbleed`进行在线检测：

![](vuln/heartbleed/1.png)

下载利用工具

> [ssltest.py](vuln/heartbleed/ssltest.py)

Python2运行脚本拿到敏感数据（Cookie）：

> `python ssltest.py {{ip}} -p {{port[1]}}`
![](vuln/heartbleed/2.png)