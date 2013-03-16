#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Daneel bot."""

from daneel import girc, utils
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)


def printer(context):
    print context

def summarize(context):
    msg = context.msg
    if msg.startswith("."):
        return
    urls = utils.find_urls(msg)
    if not urls:
        return
    summaries = map(utils.get_summary, urls)
    if context.channel:
        for summary in summaries:
            logger.info(summary)
            context.channel.say(summary)

def esper():
    user = girc.User("daneel_mk2", "R. Daneel Olivaw")
    server = girc.Server("irc.esper.net")
    channels = {
        "#stevens": girc.Channel("#stevens"),
        "#daneeltest": girc.Channel("#daneeltest"),
    }
    for channel in channels.values():
        channel.add_handler(summarize)
    return server, user, channels.values()

def rizon():
    user = girc.User("daneel", "R. Daneel Olivaw", password=open("daneel.pwd").read().strip())
    server = girc.Server("irc.rizon.net")
    channels = {
        "#danger-fourpence": girc.Channel("#danger-fourpence"),
    }
    channels["#danger-fourpence"].add_handler(summarize)
    return server, user, channels.values()

bots = [girc.Bot(*esper()), girc.Bot(*rizon())]
try:
    for bot in bots:
        bot.start()

    for bot in bots:
        bot.wait()
except KeyboardInterrupt:
    pass

