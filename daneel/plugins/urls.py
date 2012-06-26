#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Urls plugin."""

from daneel import utils

def shorten_urls(context):
    msg = context.args
    if msg.startswith("."): return
    urls = utils.find_urls(msg.args)
    if not urls: return
shorten_urls.events = ["PRIVMSG"]

def summarize(context):
    msg = context.args
    if msg.startswith("."): return
    urls = utils.find_urls(msg)
    if not urls: return
    summaries = [utils.get_summary(url) for url in urls]
    return "\n".join(summaries)
summarize.events = ["PRIVMSG"]

def shorten(context):
    pass
shorten.commands = ['shorten']
