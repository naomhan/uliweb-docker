from uliweb import settings
import docker


def getClient():
    return docker.Client(base_url=settings["DOCKER"]["URL"])
