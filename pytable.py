# -*- coding: utf-8 -*-

from __future__ import print_function

from operator import itemgetter

import monoidal_tables as mt
from monoidal_tables import renderers


if __name__ == '__main__':
    table = (mt.integer('X', itemgetter('x')) +
             mt.set_class(mt.integer('Y', itemgetter('y')), 'col-y') +
             mt.align_center(mt.column('Name', itemgetter('name'))))
    data = [
        {'x': 0, 'y': 0, 'name': 'Origin'},
        {'x': 5, 'y': 5, 'name': 'Diagonal'},
        {'x': 12, 'y': 8, 'name': 'Up'},
    ]
    print(table.render(data))
