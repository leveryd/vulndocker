{
    "desc":"心脏出血(heartbleed)",
    "image":"vuln/heartbleed",
    "type":"信息泄露",
    "level":"高",
    "volumes":{"/Users/4nim4l/fddproject/vulndocker/vuln/heartbleed/www":{"bind": "/var/www/html", "mode": "rw"},"/Users/4nim4l/fddproject/vulndocker/vuln/heartbleed/conf":{"bind":"/etc/nginx","mode":"rw"}},
    "ports":{"80/tcp":"","443/tcp":""},
}