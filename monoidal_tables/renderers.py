# -*- coding: utf-8 -*-

from . import constants


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
        map(self.print_cell, self.table.columns, values, self.widths)
        self.print_delimiter()

    def print_cell(self, column, value, width):
        align = column.attrs.get(constants.ALIGN_KEY, constants.ALIGN_LEFT)
        self.p('| {:{align}{w}} '.format(value, w=width - 1, align=align))

    def print_delimiter(self):
        self.p('|\n')

    def _print_divider(self):
        for w in self.widths:
            self.p('+' + '-' * (w + 1))
        self.p('+\n')


class HtmlRenderer(BaseRenderer):
    def tag(self, elem, cls=None):
        class TagWrapper(object):
            def __enter__(_):
                attr = ' class="{}"'.format(cls) if cls else ''
                self.p('<{}{}>'.format(elem, attr))

            def __exit__(_, type, value, traceback):
                self.p('</{}>'.format(elem))

        return TagWrapper()

    def render(self, data):
        cols = self.table.columns
        attrs = [c.attrs.get(constants.HTML_CLASS_KEY) for c in cols]
        with self.tag('table'):
            with self.tag('thead'):
                self.print_row([c.header for c in cols],
                               attrs, tag='th')
            with self.tag('tbody'):
                for row in data:
                    self.print_row([c.cell(row) for c in cols], attrs)

    def print_row(self, values, attrs, tag='td'):
        with self.tag('tr'):
            for (val, cls) in zip(values, attrs):
                self.print_cell(val, tag=tag, cls=cls)

    def print_cell(self, value, tag, cls=None):
        with self.tag(tag, cls=cls):
            self.p(value)
