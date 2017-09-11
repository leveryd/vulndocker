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

ip = "127.0.0.1"
webport = 8888
ttyport = 9999
CURRENT_DIR = os.getcwd()
app = Flask(__name__)
app.debug = 1
app.config['SECRET_KEY'] = 'hard to guess string'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config.from_object(__name__)
Session(app)

# docker在ubuntu上部署时,没有auto参数,出现client和server版本不一致的问题
client = docker.from_env(version = "auto")

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
		try:
			port.insert(0, value[0]['HostPort'].encode("utf-8"))
		except Exception:
			import traceback
			traceback.print_exc()
	#通过docker没有找到开放的端口信息,可能是用了host模式,此时用代码写到的/temp/status文件读端口信息
	#比如rmi服务中
	if len(ports) == 0:
		content = execcontainer(containerid,"cat /tmp/port")
		port.insert(0,content.strip())
	return port

# 清理没必要的配置选项
# 可变对象,和不可变对象
def cleanconfig(config,q):
	containerargslist = ["image","volumes","detach","ports","depends","network_mode","tty","environment"]
	for key in config.keys():
		if key not in containerargslist:
			config.pop(key)
	if 'detach' not in config.keys():
		config['detach'] = True
	# volumes支持相对路径的写法
	if "volumes" in config.keys():
		temp = {}
		for key in config["volumes"]:
			print config["volumes"]
			newkey = key.replace("#CURRENT_DIR#", CURRENT_DIR + "/vuln/" + q)
			temp[newkey] = config["volumes"][key]
		config.pop("volumes")
		config["volumes"] = temp
	# 容器依赖其他容器时,先启动其他容器,然后link上去
	# 当前目录下应该有依赖容器的启动配置,目前只支持依赖一个容器
	if "depends" in config.keys():
		with open("vuln/" + q + "/" + config['depends'] + "/" + config['depends'] + ".json") as f:
			depends_config = eval(f.read())
			cleanconfig(depends_config,q)
		print depends_config
		container = client.containers.run(**depends_config)
		redis_conn = redis.Redis(host="127.0.0.1", port=6379)
		print container,type(container)
		redis_conn.psetex(session['name'] + q + "depends", 1000 * 61 * 60, container.id)
		config['links'] = {container.name: config['depends']}
		print(config['links'])
		config.pop("depends")
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
				config = eval(f.read())
				cleanconfig(config,q)
				container = client.containers.run(**config)
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
		dependscontainerid = redis_conn.get(session['name'] + q + "depends")
		if containerid:
			client.api.stop(containerid)
			client.api.remove_container(containerid)
			redis_conn = redis.Redis(host="127.0.0.1", port=6379)
			redis_conn.delete(session['name'] + q )
		if dependscontainerid:
			client.api.stop(dependscontainerid)
			client.api.remove_container(dependscontainerid)
			redis_conn = redis.Redis(host="127.0.0.1", port=6379)
			redis_conn.delete(session['name'] + q + "depends")
		return redirect('/')
	except Exception as e:
		import traceback
		traceback.print_exc()
	finally:
		return redirect('/')
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

