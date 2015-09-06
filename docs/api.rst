API Documentation
=================

There are functions to help you build atomic tables of single column. These
tables can then be added together using the addition operator ``+``.

All table creating functions have the same two arguments. The ``header``
argument should be a string containing the column name. It will be used in
table header.

The ``getter`` argument should be a function that takes a single argument
representing a row in input data, and returns the value of that particular
column.

.. autofunction:: monoidal_tables.column

.. autofunction:: monoidal_tables.stringable

.. autofunction:: monoidal_tables.integer

.. autofunction:: monoidal_tables.boolean


Rendering Tables
----------------

To render the prepared table, you only need to have data for the table. The
input data should be a list of values. The actual type of values in the list is
completely arbitrary. It can be a list, a tuple, a dict or an instance of your
own class. The only requirement is that your table defines column getter that
can extract values from this.

Please note that the list may need to be traversed multiple times depending on
the renderer you choose.


.. automethod:: monoidal_tables.types.Table.render


Setting Attributes
------------------

To set attributes for the tables, use the following function. These functions
are only applicable to certain outputs. However, all the renderers can ignore
attributes they do not understand, so you can create the table using
appropriate attributes for both outputs.

These functions modify attributes for textual output. If you want to achieve
the same effect in HTML output, define a suitable class for it in CSS and use
that.

.. autofunction:: monoidal_tables.align_left

.. autofunction:: monoidal_tables.align_right

.. autofunction:: monoidal_tables.align_center


There is a single function for modifying attributes for HTML output.

.. autofunction:: monoidal_tables.set_class
