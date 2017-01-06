import cherrypy
from libs.cherrypy.plugin.rdb import RedisPlugin
from libs.cherrypy.tool.rdb import RedisTool


class Root(object):
    @cherrypy.expose
    def index(self, k):
        # print all the recorded messages so far
        v = cherrypy.request.rdb.get(k)
        cherrypy.response.headers['content-type'] = 'text/plain'
        return "Retrieved: %s in %s" % (v, k)

    @cherrypy.expose
    def record(self, k, v):
        # go to /record?msg=hello world to record a "hello world" message
        cherrypy.request.rdb.set(k, v)
        cherrypy.response.headers['content-type'] = 'text/plain'
        return "Recorded: %s in %s" % (v, k)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8090,
                            'server.socket_host': "0.0.0.0"})
    RedisPlugin(cherrypy.engine, 'redis', 6379, 0).subscribe()
    cherrypy.tools.rdb = RedisTool()
    cherrypy.tree.mount(Root(), '/', {'/': {'tools.rdb.on': True}})
    cherrypy.engine.start()
    cherrypy.engine.block()
