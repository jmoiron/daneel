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

