from cherrypy.process import plugins

import redis


class RedisPlugin(plugins.SimplePlugin):
    def __init__(self, bus, host, port, db):
        """
        This plugin is used to bind a redis connection pool to requests.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.rdb = None
        self.host = host
        self.port = port
        self.db = db
        self.bus = bus
        self.connection_pool = redis.ConnectionPool(
                    host=self.host,
                    port=self.port,
                    db=self.db
        )

    def start(self):
        self.bus.subscribe("redis.bind", self.bind)

    def stop(self):
        self.bus.unsubscribe("redis.bind", self.bind)
        self.connection_pool.disconnect()

    def bind(self):
        self.rdb = redis.Redis(connection_pool=self.connection_pool)
        return self.rdb
