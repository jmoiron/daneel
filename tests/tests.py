#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""daneel tests."""

from unittest import TestCase
from daneel import utils

class DaneelTest(TestCase):
    pass

class UtilsTest(TestCase):
    def test_find_urls(self):
        results = utils.find_urls("Welcome to http://reddit.com, where we https://google.com/#foo")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "http://reddit.com")
        self.assertEqual(results[1], "https://google.com/#foo")

    def test_summarize(self):
        doc = u"""<!doctype html> <html> <head> eta charset="utf-8">
        <title>日本語でOKです。</title> </head> <body> <p>日本語でOKです。
        </p> </body> </html>"""
        self.assertEqual(utils.summarize(doc), u"日本語でOKです。")
