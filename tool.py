import cherrypy
import redis

class RedisTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_handler',
            self.bind_rdb, priority=20
        )

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.release_rdb,
                                      priority=80)

    def bind_rdb(self):
        rdb = cherrypy.engine.publish("redis.bind").pop()
        import ipdb
        ipdb.set_trace()
        cherrypy.request.rdb = rdb

    def release_rdb(seld):
        cherrypy.request.rdb = None
        cherrypy.engine.publish("redis.release")
