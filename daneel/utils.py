#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities."""

from lxml.html import document_fromstring, fragment_fromstring
from lxml.cssselect import CSSSelector as cs

import requests

import re
import urlparse

url_re = re.compile(r"(https?://[^ ]+)")

def find_urls(message):
    """Finds urls in a message.  Returns a list of URLs, or an empty list
    if none are found.  Only looks for http & https schemes."""
    urls = url_re.findall(message)
    return [url.rstrip(',') for url in urls]

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

def get_summary(url):
    page = requests.get(url)
    content = page.content
    try:
        content = content.decode("utf-8")
    except:
        pass # sorry, can't be bothered
    return summarize(content, url)

def summarize(content, url=""):
    html = document_fromstring(content)
    if url:
        parsed = urlparse.urlparse(url)
        if parsed.netloc.endswith("twitter.com"):
            tweet = cs("p.tweet-text")(html)
            if tweet: return tweet[0].text_content().replace(u'\xa0', '')
    ogdesc = cs('meta[property="og:description"]')(html)
    if ogdesc:
        return maxlen(ogdesc[0].attrib["content"])
    ogtitle = cs('meta[property="og:title"]')(html)
    if ogtitle:
        return maxlen(ogtitle[0].attrib["content"])
    title = cs('title')(html)
    if title:
        return maxlen(title[0].text_content())
    return ''


