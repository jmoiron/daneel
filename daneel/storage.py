#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" """

import json

class Storage(object):
    def __init__(self, path):
        self.data = {}
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def sync(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.data))

    # reads
    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()

    # writes
    def __delitem__(self, key):
        del self.data[key]
        self.sync()

    def __setitem__(self, key, value):
        self.data[key] = value
        self.sync()

    def has_key(self, key):
         return key in self.data

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key):
        return key in self.data

    def iteritems(self):
        return self.data.iteritems()

    def iterkeys(self):
        return self.__iter__()

    def itervalues(self):
        for _, v in self.iteritems():
            yield v

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def clear(self):
        self.data.clear()
        self.sync()

    def setdefault(self, key, default):
        return self.data.setdefault(key, default)

    def popitem(self):
        ret = self.data.popitem()
        self.sync()
        return ret

    def update(self, other):
        for key in other.keys():
            self[key] = other[key]
        self.sync()

    def get(self, key, default):
        if key in self:
            return self[key]
        return default

    def __repr__(self):
        return repr(dict(self.items()))

