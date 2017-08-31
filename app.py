#-*- coding: UTF-8 -*-
from flask import Flask,render_template,session,redirect,url_for,flash,request,abort,Response
from flask.ext.session import Session
import socket
import fcntl
import struct
import os,commands
import docker
import redis
import random
from jinja2 import Template

ip = "10.0.44.141"
webport = 8888
ttyport = 9999
app = Flask(__name__)
app.debug = 1
app.config['SECRET_KEY'] = 'hard to guess string'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config.from_object(__name__)
Session(app)


client = docker.from_env()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
#预处理
@app.before_request
def pre_handle():
	global remoteip
	if 'name' not in session.keys():
		session['name'] = "vulntag" + str(random.randrange(1, 999999))
	remoteip = request.remote_addr
#路由
@app.route('/',methods=['GET','POST'])
def index():
	ret = []
	for i in os.listdir("vuln"):
		try:
			with open("vuln/" + i + "/README.md", "r") as f:
				temp = eval(f.read())
				temp = {"name":temp['desc'],"level":temp['level'],"dirname":i}
				ret.insert(0, temp)
		except Exception as e:
			import traceback
			traceback.print_exc()
	return render_template("index.html",data=ret,webport=webport,ip=ip)

#执行命令,返回命令结果
def execcontainer(containerid,cmd):
	content = ""
	a = client.api.exec_create(containerid,cmd)
	for i in client.api.exec_start(a,stream=True):
		content = content + str(i)
	return content

def getport(containerid):
	containerinfo = client.api.inspect_container(containerid)
	ports = containerinfo['NetworkSettings']['Ports']
	port = []
	print(ports)
	for key in ports.keys():
		value = ports[key]
		port.insert(0, value[0]['HostPort'].encode("utf-8"))
	#通过docker没有找到开放的端口信息,可能是用了host模式,此时用代码写到的/temp/status文件读端口信息
	#比如rmi服务中
	if len(ports) == 0:
		content = execcontainer(containerid,"cat /tmp/port")
		port.insert(0,content.strip())
	return port
@app.route('/start',methods=['GET','POST'])
def start():
	args = {}
	try:
		q = request.args.get('q', None)
		with open("vuln/" + q + "/desc.md", "r") as f:
			desc = f.read()
		redis_conn = redis.Redis(host="127.0.0.1", port=6379)
		containerid = redis_conn.get(session['name'] + q)
		container_remaintime = redis_conn.pttl(session['name'] + q)
		if containerid:
			container_remaintime = container_remaintime/60/1000
		else:
			with open("vuln/" + q + "/README.md", "r") as f:
				temp = eval(f.read())
				if 'network_mode' not in temp.keys():
					temp['network_mode'] = 'bridge'
				container = client.containers.run(temp['cmd'],detach=True, ports = temp['ports'],network_mode=temp['network_mode'])
				redis_conn = redis.Redis(host="127.0.0.1", port=6379)
				redis_conn.psetex(session['name'] + q,1000*60*60,container.id)
				container_remaintime = 60
				containerid = container.id
		port = getport(containerid)
		args['ttyport'] = ttyport
		args["port"] = port
		args["ip"] = ip
		args["remoteip"] = remoteip
		args["webport"] = webport
		args["vulndir"] = q
		args["containerid"] = containerid
		args["container_remaintime"] = container_remaintime
		template = Template(desc.decode("utf-8"))
		desc = template.render(**args)
		args["desc"] = desc
		return render_template("run.html",**args)
	except Exception as e:
		import traceback
		traceback.print_exc()
@app.route('/shutdown',methods=['GET','POST'])
def shutdown():
	try:
		q = request.args.get('q', None)
		redis_conn = redis.Redis(host="127.0.0.1", port=6379)
		containerid = redis_conn.get(session['name'] + q)
		if containerid:
			client.api.stop(containerid)
			client.api.remove_container(containerid)
			redis_conn = redis.Redis(host="127.0.0.1", port=6379)
			redis_conn.delete(session['name'] + q)
		return redirect('/')
	except Exception as e:
		import traceback
		traceback.print_exc()
@app.route('/remaintime')
def remaintime():
	q = request.args.get('vulndir', None)
	redis_conn = redis.Redis(host="127.0.0.1", port=6379)
	container_remaintime = redis_conn.pttl(session['name'] + q)
	return str(container_remaintime/60/1000)
@app.route('/vuln/<path:filename>')
def custom_static(filename):
	with open("vuln/"+filename,'rb') as f:
		content = f.read()
	resp = Response(content)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['content-type'] = 'application/octet-stream'
	return resp
#404页面的路由
@app.errorhandler(404)
def page_not_found(e):
	return "404",404

#404页面的路由
@app.errorhandler(500)
def page_not_found(e):
	return "500",500

@app.route('/about')
def about():
	return render_template("about.html",ip = ip,webport = webport)
@app.route('/test')
def test():
	q = request.args.get('q', None)
	with open("vuln/" + q + "/desc.md", "r") as f:
		desc = f.read()
	return markdown(desc.decode("utf-8"))

if __name__ == '__main__':
	app.run('0.0.0.0',webport)

