{
    "desc":"Nginx 配置错误导致漏洞",
    "image":"vuln/nginx2",
    "type":"配置不当",
    "level":"中",
    "ports":{"8080/tcp":"","8081/tcp":"","8082/tcp":"","80/tcp":""},
    "volumes":{"#CURRENT_DIR#/configuration":{"bind": "/etc/nginx/conf.d", "mode": "rw"},"#CURRENT_DIR#/files/":{"bind":"/home","mode":"rw"},"#CURRENT_DIR#/www/":{"bind":"/usr/share/nginx/html/","mode":"rw"}},
}