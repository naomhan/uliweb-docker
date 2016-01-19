# coding=utf-8
from uliweb import expose, functions, request, redirect, url_for, json, settings
from apps.manage import getClient
import time, os, commands
from models import Container
@expose('/containers')
class Containers:

    def __init__(self):
        self.client = getClient()

    @expose("")
    def index(self):
        containers = self.client.containers(all=True)
        #print containers
        infos = []

        for container in containers:
            info = {}
            info["id"] = container["Id"]
            info["name"] = str(container["Names"][0])[1:]
            info["image"] = container["Image"]
            info["created"] = time.strftime('%Y-%m-%d',time.localtime(container["Created"]))
            info["status"] = self.client.inspect_container(container["Id"])["State"]["Running"]
            #info["ip"] = self.client.inspect_container(container["Id"])["NetworkSettings"]["IPAddress"]
            #exec_id = self.client.exec_create(container=container["Id"], cmd=settings["DOCKER"]["IP"])["Id"]
            info["ip"] = ""
            tmp = str(commands.getoutput("docker exec "+ container["Id"] +" ifconfig eth1|sed -n 2p|awk  '{ print $2 }'|awk -F : '{ print $2 }'")).lower()
            print tmp
            if tmp.find("error") ==-1:
                info["ip"] = tmp
            infos.append(info)
        #print infos
        return {"containers":infos}

    @expose("detail/<id>")
    def detail(self, id):
        return {}


    @expose("add")
    def add(self):
        if request.method=="GET":
            images = []
            for i in self.client.images():
                images.append(i["RepoTags"][0])
            return {"images":sorted(images)}
        elif request.method=="POST":
            image = request.params["image"]
            name = request.params["name"]
            command = request.params["command"]
            ip = request.params["ip"]
            if len(name) <=1:
                return json({'success':False,'message':'name长度不能小于一个字符'})
            containerId = self.client.create_container(
                image=image,
                name = name,
                command=command,
                stdin_open=True,
                tty=True,
                detach=True
            )["Id"]
            print containerId
            self.client.start(container=containerId)
            cmd = ""
            if self.client.inspect_container(container=containerId)["State"]["Running"] and ip.strip():
                cmd = "pipework "+ settings["DOCKER"]["NETWORK"] + " " +name + " " + ip +"/24"
            else:
                cmd = "pipework "+ settings["DOCKER"]["NETWORK"] + " " +name + " dhcp"
            print cmd
            #print "docker exec "+containerId + """  bash -c "echo 'root:""" + command + """' | chpasswd" """
            print os.system(cmd)
            #ip = str(commands.getoutput("docker exec "+ containerId +" ifconfig eth1|sed -n 2p|awk  '{ print $2 }'|awk -F : '{ print $2 }'")).lower()
            #print ip
            # if ip.find("error") ==-1:
            #     #con = functions.get_model(Container)
            #     c = con(
            #         containerid = containerId,
            #         name = name,
            #         ip = ip
            #     )
            #     c.save()
            print json({'success':True,'container':containerId})
            return json({'success':True,'container':containerId})
        else:
            return redirect(url_for(Containers.add))

    def start(self, id):
        self.client.start(container=id)
        cmd = ""
        if self.client.inspect_container(container=id)["State"]["Running"]:
        #     cmd = "pipework "+ settings["DOCKER"]["NETWORK"] + " " +name + " " + ip +"/24"
        # else:
            cmd = "pipework "+ settings["DOCKER"]["NETWORK"] + " " +self.client.inspect_container(container=id)["Name"][1:] + " dhcp"
        print cmd
        os.system(cmd)
        return redirect(url_for(Containers.index))

    def stop(self, id):
        self.client.stop(container=id)
        return redirect(url_for(Containers.index))

    def restart(self, id):
        self.client.restart(container=id)
        if self.client.inspect_container(container=id)["State"]["Running"]:
        #     cmd = "pipework "+ settings["DOCKER"]["NETWORK"] + " " +name + " " + ip +"/24"
        # else:
            cmd = "pipework "+ settings["DOCKER"]["NETWORK"] + " " +self.client.inspect_container(container=id)["Name"][1:] + " dhcp"
        print cmd
        os.system(cmd)
        return redirect(url_for(Containers.index))

    def delete(self, id):
        try:
            self.client.remove_container(container=id, force=True)
        except Exception as e:
            self.client.stop(container=id)
            self.client.remove_container(container=id)

        return redirect(url_for(Containers.index))
