# coding=utf-8
from uliweb import expose, functions, json
from apps.manage import getClient
import time

@expose("/images")
class Images:

    def __init__(self):
        self.client = getClient()

    @expose("")
    def index(self):
        images = []
        tmps = self.client.images()
        for tmp in tmps:
            image = {}
            image["ID"] = tmp["Id"]
            RepoTags = str(tmp["RepoTags"][0]).split(":")
            image["REPOSITORY"] = RepoTags[0]
            image["TAG"] = RepoTags[1]
            image["CREATED"] = time.strftime('%Y-%m-%d',time.localtime(tmp["Created"]))
            size = float(tmp["VirtualSize"])/1024/1024
            image["VirtualSize"] = float("%.2f" %size)
            images.append(image)
        return {"images":images}
