# monoidal-tables

Table generator and formatter.

This package provides a module for easy generating of pretty tables. It
features a couple renderers for textual output as well as for HTML.

Unlike other libraries for generating pretty tables, this module makes sure
that it is impossible to mix up header names and actual values.

The table itself does not contain any data. It is merely a blueprint for
turning a collection of data into an actual table. You create the blueprint
by combining multiple columns.

It is heavily inspired (a knock off, actually) by yesod-tables, a brilliant
Haskell library. Unlike its inspiration, it does not have various columns
for different types, as that is pointless in Python. It does have better
support for customization, though.


## Why the name

A monoid is a set with binary associative operation with neutral element.
Tables as presented here exactly satisfy this condition. The empty table
(with no columns) takes on the role of neutral element and concatenating is
the desired operation.

## Example

```python
from operator import itemgetter
table = (integer('X', itemgetter('x')) +
         integer('Y', itemgetter('y')) +
         string('Name', itemgetter('name')))
data = [
    {'x': 0, 'y': 0, 'name': 'Origin'},
    {'x': 5, 'y': 5, 'name': 'Diagonal'},
    {'x': 2, 'y': 8, 'name': 'Up'},
]
table.render(data, renderer=FancyRenderer)
```
