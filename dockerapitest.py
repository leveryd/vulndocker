import docker
import os
client = docker.from_env()
def getimagelist():
	print client.images.list()
def getvulclist():
	ret = []
	for i in os.listdir("vuln"):
		try:
			with open("vuln/"+i+"/README.md","r") as f:
				title = f.readlines()[0]
				ret.insert(0,title)
		except Exception,e:
			print e
	return ret
def startimage():
	container = client.containers.run("vuln/shiro:latest", detach=True)
	print container.id
def execcontainer(containerid,cmd):
	content = ""
	a = client.api.exec_create("fc4560a9b6dd","ls /tmp")
	for i in client.api.exec_start(a,stream=True):
		content = content + str(i)
	return content
print execcontainer()