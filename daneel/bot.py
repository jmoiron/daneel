#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Daneel IRC Bot."""

from daneel import plugins
from irctk import Bot

daneel = Bot()

def has(obj, attr):
    return bool(getattr(obj, attr, None))

for plugin in plugins.enabled:
    if has(plugin, "commands"):
        for command in plugin.commands:
            daneel.command(command)(plugin)
    if has(plugin, "events"):
        for event in plugin.events:
            daneel.event(event)(plugin)
    if has(plugin, "regex"):
        for reg in plugin.regex:
            daneel.regex(reg)(plugin)

