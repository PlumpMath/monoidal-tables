Basic Usage
===========

The general patter when using *Monoidal Tables* is that first you define what
columns your table should contain. Then you feed the table with data and obtain
properly formatted output.

The table as abstracted by this library is actually more of a blueprint for
constructing the actual table.

A table is created by concatenating other tables. To have something to start
with, there are a couple functions for creating elementary single column
tables.

The concatenating happens column-wise. This is because it is the best way to do
it and because at this stage there is no data, so it's also the only way to do
it.

When you finally want to use the table blueprint to format data, you have an
option to select which renderer you want to use. The default is to format into
text, but you can also go for HTML.

If you want to customize the output, there are functions that set attributes on
the tables such as column alignment. Please note though that not all attributes
make sense for all renderers. Extra attributes are ignores.

It is perfectly ok to reuse the same table blueprint multiple times with
different data sets.
