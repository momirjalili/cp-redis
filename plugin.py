from cherrypy.process import plugins

import cherrypy
import redis

class RedisPlugin(plugins.SimplePlugin):
    def __init__(self, bus, host, port, db):
        """
        This plugin is used to bind a redis connection pool to requests.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.connection_pool = None
        self.rdb
        self.host = host
        self.port = port
        self.db = db
        self.bus = bus

    def start(self):
        self.bus.subscribe("redis.bind", self.bind)
        self.bus.subscribe("redis.release", self.bind)

    def stop(self):
        self.bus.unsubscribe("redis.bind")
        self.bus.unsubscribe("redis.release")
        self.connection_pool.disconnect()

    def bind(self):
        self.connection_pool = redis.ConnectionPool(
                    host=self.host,
                    port=self.port,
                    db=self.db
        )
        self.rdb = redis.Redis(connection_pool=self.connection_pool)
        return rdb

    def release(self):
        self.connection_pool.release(self.rdb)
