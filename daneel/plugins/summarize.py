#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Summarize plugin.  Listens for URLs and prints a summary."""

from daneel.plugins import weblib

import logging
logger = logging.getLogger(__name__)

def summarize(context):
    msg = context.msg
    # skip command-ish things
    if msg.startswith("."):
        return
    urls = weblib.find_urls(msg)
    if not urls:
        return
    summaries = map(weblib.get_summary, urls)
    if context.channel:
        for summary in summaries:
            context.channel.say(summary)

