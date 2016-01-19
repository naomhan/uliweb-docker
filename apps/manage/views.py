# coding=utf-8
from uliweb import expose, functions, settings, json, request
from apps.manage import getClient

@expose("/")
class Docker:
    @expose("")
    def index(self):
        return {
            "version":getClient().version(),
            "images":len(getClient().images()),
            "containers":len(getClient().containers(all=True))
        }
