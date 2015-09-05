# -*- coding: utf-8 -*-

from __future__ import print_function


class BaseRenderer(object):
    def __init__(self, table):
        self.table = table
        self.output = []

    def p(self, val):
        self.output.append(val)

    def __str__(self):
        return ''.join(self.output)


class FancyRenderer(BaseRenderer):
    def render(self, data):
        self.widths = [col.max_width(data) + 1 for col in self.table.columns]
        self._print_divider()
        self.print_row([c.header for c in self.table.columns])
        self._print_divider()
        for row in data:
            self.print_row([c.cell(row) for c in self.table.columns])
        self._print_divider()

    def print_row(self, values):
        map(self.print_cell, values, self.widths)
        self.print_delimiter()

    def print_cell(self, value, width):
        self.p('| {:<{w}}'.format(value, w=width))

    def print_delimiter(self):
        self.p('|\n')

    def _print_divider(self):
        for w in self.widths:
            self.p('+' + '-' * (w + 1))
        self.p('+\n')


class HtmlRenderer(BaseRenderer):
    def tag(self, elem):
        class TagWrapper(object):
            def __enter__(_):
                self.p('<{}>'.format(elem))

            def __exit__(_, type, value, traceback):
                self.p('</{}>'.format(elem))

        return TagWrapper()

    def render(self, data):
        with self.tag('table'):
            with self.tag('thead'):
                self.print_row([c.header for c in self.table.columns],
                               tag='th')
            with self.tag('tbody'):
                for row in data:
                    self.print_row([c.cell(row) for c in self.table.columns])

    def print_row(self, values, tag='td'):
        with self.tag('tr'):
            map(lambda v: self.print_cell(v, tag=tag), values)

    def print_cell(self, value, tag):
        with self.tag(tag):
            self.p(value)


class Table(object):
    def __init__(self, columns=()):
        self.columns = columns

    def __add__(self, other):
        return Table(self.columns[:] + other.columns[:])

    def render(self, data, renderer=FancyRenderer):
        r = renderer(self)
        r.render(data)
        print(r)


class Column(object):
    def __init__(self, header, cell):
        self.header = header
        self.cell = cell

    def max_width(self, data):
        data_max = 0
        if data:
            data_max = max([len(self.cell(item)) for item in data])
        return max(data_max, len(self.header))


def column(header, getter):
    """
    Create table consisting of a single column. The getter must return a
    string-like value, else TypeError will be raised.
    """
    def better_getter(x):
        value = getter(x)
        if value is None:
            return ''
        if not isinstance(value, basestring):
            raise TypeError(
                'Column {col}: {data} is not a string.'.format(
                    col=header, data=value))
        return value
    return Table(columns=(Column(header, getter), ))


def stringable(header, getter):
    """
    Create a table consisting of a single column. The getter must return a
    value that can be converted to string with the ``str()``
    """
    def wrapped_getter(x):
        return str(getter(x))
    return column(header, wrapped_getter)


def boolean(header, getter, mapping=None):
    """
    Create a table consisting of a single column. The getter must return a
    boolean which is converted to string based on the mapping provided as
    optional argument. The default is simply ``"True"`` and ``"False"``.

    :param mapping: Dict mapping booleans to strings.
    """
    mapping = mapping or {True: 'True', False: 'False'}

    def wrapped_getter(x):
        value = getter(x)
        if not isinstance(value, bool):
            raise TypeError(
                'Column {col}: {data} is not a bool.'.format(
                    col=header, data=value))
        return mapping[x]
    return column(header, wrapped_getter)


if __name__ == '__main__':
    from operator import itemgetter
    table = (stringable('X', itemgetter('x')) +
             stringable('Y', itemgetter('y')) +
             column('Name', itemgetter('name')))
    data = [
        {'x': 0, 'y': 0, 'name': 'Origin'},
        {'x': 5, 'y': 5, 'name': 'Diagonal'},
        {'x': 2, 'y': 8, 'name': 'Up'},
    ]
    table.render(data, renderer=FancyRenderer)
