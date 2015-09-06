# -*- coding: utf-8 -*-


class Table(object):
    def __init__(self, columns=()):
        self.columns = columns

    def __add__(self, other):
        return Table(self.columns[:] + other.columns[:])


class Column(object):
    def __init__(self, header, cell):
        self.header = header
        self.cell = cell
        self.attrs = {}

    def max_width(self, data):
        data_max = 0
        if data:
            data_max = max([len(self.cell(item)) for item in data])
        return max(data_max, len(self.header))


def set_attr(table, key, value):
    """
    Set an attribute on all columns of a table.

    :param key: name of the attribute
    :param value: value of the attribute
    :returns: new table
    """
    def worker(c, k, v):
        c.attrs[k] = v
        return c
    return Table(tuple(worker(col, key, value) for col in table.columns[:]))
