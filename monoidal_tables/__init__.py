# -*- coding: utf-8 -*-

from __future__ import print_function

from . import constants
from . import renderers
from . import types


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
    return types.Table(columns=(types.Column(header, getter), ))


def stringable(header, getter):
    """
    Create a table consisting of a single column. The getter must return a
    value that can be converted to string with the ``str()``
    """
    def wrapped_getter(x):
        return str(getter(x))
    return column(header, wrapped_getter)


def integer(header, getter):
    """
    This function behaves just like ``stringable``, except it sets right
    alignment on textual output by default.
    """
    return align_right(stringable(header, getter))


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


def align_left(table):
    """
    Creates a new table with the same columns as the given table. All columns
    in new table are left aligned. This attribute is only applicable to textual
    output.
    """
    return types.set_attr(table, constants.ALIGN_KEY, constants.ALIGN_LEFT)


def align_right(table):
    """
    Creates a new table with the same columns as the given table. All columns
    in new table are right aligned. This attribute is only applicable to
    textual output.
    """
    return types.set_attr(table, constants.ALIGN_KEY, constants.ALIGN_RIGHT)


def align_center(table):
    """
    Creates a new table with the same columns as the given table. All columns
    in new table are center aligned. This attribute is only applicable to
    textual output.
    """
    return types.set_attr(table, constants.ALIGN_KEY, constants.ALIGN_CENTER)


def set_class(table, cls):
    """
    Creates a new table with the same columns as the given table. All columns
    in new table will have given HTML classes. This class will be added to
    table cells, both ``th`` and ``td`.

    This only works for HTML output.

    :param cls: the classes you want to set, you can specify multiple classes
                separated by spaces
    :paramtype cls: string
    """
    return types.set_attr(table, constants.HTML_CLASS_KEY, cls)


def render(renderer, table, data):
    """
    Render the table with the renderer and return the string representation.
    """
    r = renderer(table)
    r.render(data)
    return str(r)


def render_text(table, data):
    """
    This function renders the table as bordered ASCII table and immediately
    prints it to standard output. If you actually need to do something with the
    text, use the ``render`` function.
    """
    print(render(renderers.FancyRenderer, table, data))


def render_html(table, data):
    """
    This function renders the table into HTML and returns the string containing
    the markup.
    """
    return render(renderers.HtmlRenderer, table, data)
