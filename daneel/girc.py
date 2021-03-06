#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Very simple IRC lib using gevent threads per server."""

import gevent
from gevent import monkey, event
monkey.patch_all()

import socket
import os
import re
import logging
import traceback
import time
from daneel import utils

logger = logging.getLogger(__name__)

def handle_on(function, type=None, sender=None, target=None, msg=None):
    type, sender, target, msg = map(utils.applyable, (type, sender, target, msg))
    def handler(ctx):
        if not ctx.is_valid:
            return
        if type(ctx.type) and sender(ctx.sender) and target(ctx.target) and msg(ctx.msg):
            function(ctx)
    return handler

def privmsg(function):
    return handle_on(function, type=lambda m: m == "PRIVMSG")

class Context(object):
    def __init__(self, line, server):
        self.server = server
        data = line.split(None, 3)
        if len(data) != 4:
            self.is_valid = False
            return
        self.line = line
        self.is_valid = True
        self.sender = data[0][1:]
        self.type = data[1]
        self.target = data[2]
        if self.target in server.channels:
            self.channel = server.channels[self.target]
        self.msg = data[3][1:]

    def __repr__(self):
        ctx = dict(self.__dict__)
        del ctx["is_valid"]
        del ctx["line"]
        return "Context: %s" % ctx

class User(object):
    def __init__(self, nick="robotnik", realname="eggman", password=None):
        self.nick = nick
        self.realname = realname
        self.password = password

    def identify(self, server):
        if self.password:
            server.waitfor("This nickname is registered")
            server.say("nickserv", "identify %s" % self.password)
            server.waitfor("Password accepted")

    def initialize(self, server):
        server.send("NICK %s" % self.nick)
        server.send("USER %s 0 * :%s" % (self.nick, self.realname))

    def __str__(self):
        return "%s%s" % (self.nick, " (w/ password)" if self.password else "")

class Channel(object):
    def __init__(self, name):
        """Channels do not have a server until a server is used to join them."""
        if not name.startswith("#"):
            raise ValueError("Channel names must start with a #")
        self.name = name
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handle_on(handler, target=self.name))

    def say(self, msg):
        self.server.say(self.name, msg)

class Server(object):
    pingre = re.compile(r"PING :(.+)")

    def __init__(self, host, port=6667, ssl=False, timeout=300):
        if isinstance(host, list):
            self.hosts = host
            self.host = self.nexthost()
        else:
            self.host = host
        self.port = port
        self.ssl = ssl
        self.timeout = timeout
        self.connected = False
        self.socket = None
        self.rawhandlers = [self.ping]
        self.handlers = []
        self.channels = {}

    def nexthost(self):
        if not hasattr(self, "current"):
            self.current = 0
        else:
            self.current = (self.current + 1) % len(self.hosts)
        return self.hosts[self.current]

    def connect(self,  user):
        """Connect as a user.  If this server is already connected, noop."""
        if self.connected:
            return
        self.socket = socket.socket()
        self.socket.settimeout(30)
        self.socket.connect((self.host, self.port))
        logger.info("%s connected to %s" % (utils.color("iii", utils.green), self.host))
        self.read_thread = gevent.spawn(self.read)
        user.initialize(self)
        self.waitfor("Found your hostname")
        user.identify(self)
        self.connected = True

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def _log(self, msg, incoming=True):
        status = "<<:" if incoming else ">>:"
        status = utils.color(status, utils.yellow if incoming else utils.green)
        logger.info("%s `%s`" % (status, msg))

    def read(self):
        sockfile = self.socket.makefile()
        while True:
            line = sockfile.readline()
            # if we read nothing, that means we've disconnected
            if not line:
                return
            line = line.strip()
            self._log(line)
            self.handle(line)

    def ping(self, line):
        match = self.pingre.match(line)
        if match:
            self.send("PONG :%s" % match.groups()[0])

    def handle(self, line):
        for handle in self.rawhandlers:
            try:
                handle(line)
            except:
                logger.error(traceback.format_exc())
        context = Context(line, self)
        if context.is_valid:
            for handle in self.handlers:
                handle(context)

    def send(self, msg):
        self._log(msg, False)
        msg = utils.utf8_damnit(msg)
        self.socket.send("%s\r\n" % msg)

    def say(self, to, msg):
        msgs = msg.split("\n")
        # rudimentary flood protection...
        for msg in msgs[:4]:
            self.send("PRIVMSG %s :%s" % (to, msg))

    def waitfor(self, matcher, raw=True):
        if isinstance(matcher, basestring):
            raw = True
        matcher = utils.applyable(matcher)
        result = event.AsyncResult()
        def waiter(line):
            if matcher(line):
                result.set(1)
        handlers = self.rawhandlers if raw else self.handlers
        handlers.append(waiter)
        result.get()
        handlers.remove(waiter)

    def wait(self):
        self.read_thread.join()

    def join(self, channel):
        self.send("JOIN %s" % channel.name)
        self.channels[channel.name] = channel
        # XXX: this makes it unsafe to use the same channel for multiple servers
        # but you probably should not be trying to take that shortcut anyway
        channel.server = self
        self.handlers += channel.handlers

    def __str__(self):
        return "%s:%s" % (self.host, self.port)

class Bot(object):
    def __init__(self, server, user, channels):
        self.server = server
        self.user = user
        self.channels = channels

    def start(self):
        status = utils.color("**:", utils.blue)
        logger.info("%s Connecting to %s as %s" % (status, self.server, self.user))
        self.server.connect(self.user)
        if not self.user.password:
            self.server.waitfor("MODE")
        # join channels
        for channel in self.channels:
            self.server.join(channel)

    def wait(self):
        self.server.wait()

    def forever(self):
        while True:
            self.start()
            self.wait()
            status = utils.color("**:", utils.red)
            logger.info("%s Server %s disconnected.  Reconnecting in 30 seconds..." % (status, self.server))
            try:
                self.server.disconnect()
            except Exception as e:
                logger.error("EE Error: %s", e)
            time.sleep(30)

