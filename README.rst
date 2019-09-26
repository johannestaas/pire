pire
====

Python Interactive Regular Expression
-------------------------------------

PIRE is an interactive command-line interface allowing you to edit regexes live and see how your
changes match against the input you specify.

.. image:: https://github.com/johannestaas/pire/blob/master/screenshot.png
   :scale: 75%
   :alt: example usage
   :align: center

Installation
------------

Through PyPI::

    $ pip install pire

Or from the project root directory::

    $ python setup.py install

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

Hotkeys
-------

.. image:: https://github.com/johannestaas/pire/blob/master/help.png
   :scale: 75%
   :alt: hotkeys
   :align: center

Releases
--------

:0.2.0:
    - added several hotkeys for navigation
    - improved performance
:0.1.1:
    - fixed bug with missing regex.pire file and output display
:0.1.0:
    - curses interface implemented
:0.0.1:
    - Project created
