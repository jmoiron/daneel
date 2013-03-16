#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Daneel bot."""

from daneel import girc, utils
import logging

from daneel.plugins.summarize import summarize
from daneel.plugins.shorten import Shorten

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)


def esper():
    user = girc.User("daneel", "R. Daneel Olivaw")
    server = girc.Server("irc.esper.net")
    channels = {
        "#stevens": girc.Channel("#stevens"),
        #"#daneeltest": girc.Channel("#daneeltest"),
    }
    for channel in channels.values():
        channel.add_handler(summarize)
        channel.add_handler(Shorten())
    return server, user, channels.values()

def rizon():
    user = girc.User("daneel", "R. Daneel Olivaw", password=open("daneel.pwd").read().strip())
    server = girc.Server("irc.rizon.net")
    channels = {
        "#danger-fourpence": girc.Channel("#danger-fourpence"),
    }
    channels["#danger-fourpence"].add_handler(summarize)
    channels["#danger-fourpence"].add_handler(Shorten())
    return server, user, channels.values()

bots = [girc.Bot(*esper()), girc.Bot(*rizon())]
try:
    for bot in bots:
        bot.start()

    for bot in bots:
        bot.wait()
except KeyboardInterrupt:
    pass

