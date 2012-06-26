#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""IRC bot for #stevens @ esper."""

from irctk import Bot

class Config(object):
    SERVER = 'irc.esper.net'
    PORT = 6667
    SSL = False
    TIMEOUT = 300
    NICK = "daneel"
    REALNAME = "R. Daneel Olivaw"
    CHANNELS = ["#stevens"]

config = Config()

bot = Bot()
bot.config.from_object(config)

from daneel import plugins

def has(obj, attr):
    return bool(getattr(obj, attr, None))

for plugin in plugins.enabled:
    if has(plugin, "commands"):
        for command in plugin.commands:
            bot.command(command)(plugin)
    if has(plugin, "events"):
        for event in plugin.events:
            bot.event(event)(plugin)
    if has(plugin, "regex"):
        for reg in plugin.regex:
            bot.regex(reg)(plugin)

