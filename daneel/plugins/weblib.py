#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convenience functions for doing web things."""

import re
import requests
import urlparse
import traceback
import json

from lxml.cssselect import CSSSelector as cs
from lxml.html import document_fromstring
from daneel import utils

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"

def text(selector, html):
    res = cs(selector)(html)
    if not res:
        return ""
    if res and len(res) == 1:
        return res[0].text_content().strip()
    res = map(lambda x: x.text_content().strip(), res)
    return "".join(res)

def first(selector, html):
    res = cs(selector)(html)
    if not res or not len(res):
        return None
    return res[0]

def get_summary(url):
    """Get a summary for a url."""
    if "yelp.com" in url:
        return "Yelp is not supported because they IP blocked the server daneel runs on."
    page = requests.get(url, headers={'User-Agent': ua})
    try:
        content = page.text
    except:
        content = page.content
        content = utils.utf8_damnit(content)
    return summarize(content, url)


def summarize(content, url=""):
    """Return a summary for an html document.  If a URL is passed, it may be
    treated specially to give better results, eg. twitter will return the tweet."""
    html = document_fromstring(content)
    if url:
        parsed = urlparse.urlparse(url)
        if parsed.netloc.endswith("twitter.com") and "status" in url:
            tweet = text(".permalink-tweet .tweet-text", html)
            try:
                username = cs(".permalink-tweet")(html)[0].attrib["data-screen-name"]
                return "@%s: %s" % (username, tweet)
            except:
                return tweet
    # try to return opengraph description or title first, then just the <title>
    ogdesc = first("meta[property=\"og:description\"]", html)
    if ogdesc:
        return utils.maxlen(ogdesc.attrib["content"])

    ogtitle = first("meta[property=\"og:title\"]", html)
    if ogtitle:
        return utils.maxlen(ogtitle.attrib["content"])

    return text("title", html)


def shorten_url(url):
    gurl = "https://www.googleapis.com/urlshortener/v1/url"
    data = json.dumps({"longUrl": url})
    resp = requests.post(gurl, data, headers={"Content-Type": "application/json"})
    if resp.json and "id" in resp.json:
        return resp.json["id"]
    return None

url_re = re.compile(r"(https?://[^ ]+)")

def find_urls(message):
    """Finds urls in a message.  Returns a list of URLs, or an empty list
    if none are found.  Only looks for http & https schemes."""
    urls = url_re.findall(message)
    return [url.rstrip(',') for url in urls]

