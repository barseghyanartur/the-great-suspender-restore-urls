================================
the-great-suspender-restore-urls
================================

Restore the broken URLs of the Great Suspender browser (Google Chrome, Firefox)
extension.

.. image:: https://img.shields.io/pypi/v/the-great-suspender-restore-urls.svg
   :target: https://pypi.python.org/pypi/the-great-suspender-restore-urls
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/the-great-suspender-restore-urls.svg
    :target: https://pypi.python.org/pypi/the-great-suspender-restore-urls/
    :alt: Supported Python versions

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/barseghyanartur/the-great-suspender-restore-urls/#License
   :alt: MIT

Background
==========

If you used to use The Great Suspender Chrome extension, you would notice (as 
of 2021-02-04) that it has been banned by Google Chrome for being a malware.

The last-known-good-version on GitHub, release `v7.1.6 <https://github.com/greatsuspender/thegreatsuspender/releases/tag/v7.1.6>`__,
works well for me, if installed from source. However, your saved
tabs won't reload as something has changed in between the `good` and the `bad`
releases.

What to do? Would you just loose all precious URLs and saved sessions? If you 
are OK with that, just pass by. Otherwise, read further.

How to fix the broken tabs
==========================

1. Use the `FreshStart - Cross Browser Session Manager <https://chrome.google.com/webstore/detail/freshstart-cross-browser/nmidkjogcjnnlfimjcedenagjfacpobb>`__
   extension to export all your tabs into a JSON and save it into a file (for
   instance, name it ``tabs.json``).

2. Install ``the-great-suspender-restore-urls`` (this) package:

.. code-block:: sh

  pip install the-great-suspender-restore-urls

3. Fix your broken tabs:

.. code-block:: sh

    restore-the-great-suspender-urls --in-file=tabs.json --out-file=tabs-restored.json

4. Use the `FreshStart - Cross Browser Session Manager <https://chrome.google.com/webstore/detail/freshstart-cross-browser/nmidkjogcjnnlfimjcedenagjfacpobb>`__
   to import the tabs back (paste the contents of the ``tabs-restored.json``
   in the import session window).

Usage options
=============

By default, your existing session names will get a " - cleaned" suffix.
In order to tweak that, use the ``--session-name-suffix`` argument.

To have a verbose output, add the ``--verbose`` argument.

.. code-block:: sh

    restore-the-great-suspender-urls \
        --in-file=tabs.json \
        --out-file=tabs-restored.json \
        --session-name-suffix=' - FIXED' \
        --verbose

Prerequisites
=============

- Python 3.6, 3.7, 3.8 or 3.9.

License
=======

MIT

Support
=======

For any issues contact me at the e-mail given in the `Author`_ section.

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
