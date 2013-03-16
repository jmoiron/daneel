#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities."""

import re

white,black,red,green,yellow,blue,purple = range(89,96)
def color(string, color=green, bold=False):
    """Usage: color("foo", red, bold=True)"""
    return '\033[%s%sm' % ('01;' if bold else '', color) + str(string) + '\033[0m'

encodings = "utf-8 L1 L2 shift_jis utf-16 cp1252 cp1251 cp1250".split()
def utf8_damnit(string, encodings=encodings):
    """Try your sunday best to make something a utf-8 encoded string."""
    if isinstance(string, unicode):
        return string.encode("utf-8")
    for encoding in encodings:
        try:
            return string.decode(encoding).encode("utf-8")
        except:
            pass
    return string # pray

def applyable(match):
    """Make a callable filter from match."""
    if not match:
        return lambda x: True
    if callable(match):
        return match
    if isinstance(match, basestring):
        regex = re.compile(match)
        return lambda x: regex.search(x)
    if hasattr(match, "search") and hasattr(match, "match"):
        # assume this is a regex
        return lambda x: match.search(x)
    raise ValueError("Could not make applyable from %r" % match)

def maxjoin(parts, char, length):
    """Join a number of parts such that the result is shorter than length."""
    joined = ""
    for part in parts:
        if len(joined) + len(part) < length:
            joined += "%s%s" % (part, char)
        else:
            return joined.rstrip(char)
    return joined

def maxlen(message, length=400):
    mlen = len(message)
    if mlen < length:
        return message
    sentences = message.split(".")
    if len(sentences) > 1 and len(sentences[0]) < length:
        return maxjoin(sentences, ".", length)
    words = message.split()
    if len(words) > 1 and len(words[0]) < length:
        return maxjoin(words, " ", length)
    return message[:length]

