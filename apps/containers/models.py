#coding = utf-8

from uliweb.orm import *


class Container(Model):
    containerid = Field(str)
    name = Field(str, max_length=50)
    ip = Field(str)
