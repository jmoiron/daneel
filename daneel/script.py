#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Actual bot binary script helper."""

import sys
import os
import json
import optparse
import bot

defaults = dict(
    SERVER = 'irc.esper.net',
    PORT = 6667,
    SSL = False,
    TIMEOUT = 300,
    NICK = "daneel2",
    REALNAME = "R. Daneel Olivaw",
    CHANNELS = ["#daneeltest"],
)

def register_plugins():
    from daneel.bot import daneel
    from daneel.plugins import enabled

    for plugin in enabled:
        if hasattr(plugin, "commands"):
            for command in plugin.commands:
                daneel.command(command)(plugin)
        if hasattr(plugin, "events"):
            for event in plugin.events:
                daneel.event(event)(plugin)
        if hasattr(plugin, "regex"):
            for reg in plugin.regex:
                daneel.regex(reg)(plugin)


def parse_args():
    parser = optparse.OptionParser(usage="%prog config")
    opts, args = parser.parse_args()
    if len(args) != 1:
        print "Error: single argument (config file path) required."
        raise SystemExit
    return opts, args

def main():
    register_plugins()
    opts, args = parse_args()
    if not os.path.exists(args[0]):
        print "Error: file %s not found." % args[0]
        raise SystemExit
    with open(args[0], "r") as f:
        conf = json.load(f)
    config = defaults.copy()
    config.update(conf)
    bot.daneel.config.update(config)
    bot.daneel.run()

