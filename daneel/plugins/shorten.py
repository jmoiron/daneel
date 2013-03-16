#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shorten urls automatically which are over a certain threshold."""

from daneel.plugins import weblib
import re

setre = re.compile(r"\.shorten (\d+)$")

class Shorten(object):
    """Shorten urls > length."""
    def __init__(self, maxlen=50):
        self.maxlen = maxlen

    def __call__(self, context):
        msg = context.msg
        if self.commands(context):
            return
        urls = weblib.find_urls(msg)
        shortened = []
        for url in urls:
            if len(url) > self.maxlen:
                shorter = weblib.shorten_url(url)
                if shorter:
                    shortened.append([url, shorter])
        for orig, short in shortened:
            context.channel.say("%s..: %s" % (orig[:30], short))

    def commands(self, context):
        msg = context.msg
        if msg == ".shorten":
            context.channel.say("URLs over %d chars will be shortened.  `.shorten ##` to set." % self.maxlen)
            return True
        isset = setre.match(msg)
        if isset:
            self.maxlen = int(isset.groups()[0])
            context.channel.say("URLs over %d chars will be shortened." % self.maxlen)
            return True

