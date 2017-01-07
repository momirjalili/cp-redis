import cherrypy


class RedisTool(cherrypy.Tool):
    """This tool will add rdb to cp request."""

    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_rdb, priority=21)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.release_rdb,
                                      priority=81)

    def bind_rdb(self):
        rdb = cherrypy.engine.publish("redis.bind").pop()
        cherrypy.request.rdb = rdb

    def release_rdb(seld):
        cherrypy.request.rdb = None
