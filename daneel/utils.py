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

def get_summary(url):
    page = requests.get(url)
    html = document_fromstring(page.text)
    parsed = urlparse.urlparse(url)
    if parsed.netloc.endswith("twitter.com"):
        tweet = cs("p.tweet-text")(html)
        if tweet: return tweet[0].text_content().replace(u'\xa0', '')
    ogdesc = cs('meta[property="og:description"]')(html)
    if ogdesc:
        return ogdesc[0].attrib["content"]
    ogtitle = cs('meta[property="og:title"]')(html)
    if ogtitle:
        return ogtitle[0].attrib["content"]
    title = cs('title')(html)
    if title:
        return title[0].text_content()
    return ''


