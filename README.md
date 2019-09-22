pire
====

Python Interactive Regular Expression

Installation
------------

From the project root directory::

    $ python setup.py install

Or through PyPI:

    $ pip install pire

CLI Usage
---------

Use --help/-h to view info on the arguments::

    $ pire --help

Run pire against a text file::

    $ pire application.log

Regexes used will be cached to a file in the present directory named `regex.pire`.

Pass a custom newline-delimited file with regexes::

    $ pire -r app.pire application.log

Pass multiple files::

    $ pire -r app.pire application.log application.log.1 application.log.2

Or::

    $ pire -r app.pire application.log*

Releases
--------

| Version | Notes           |
| ------- | --------------- |
|  0.0.1  | Project created |
