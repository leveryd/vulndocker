{
    "desc":"心脏出血(heartbleed)",
    "image":"vuln/heartbleed",
    "type":"信息泄露",
    "level":"高",
    "volumes":{"#CURRENT_DIR#/www":{"bind": "/var/www/html", "mode": "rw"},"#CURRENT_DIR#/conf":{"bind":"/etc/nginx","mode":"rw"}},
    "ports":{"80/tcp":"","443/tcp":""},
}