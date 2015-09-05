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
