Installation
============

Requirements
------------

Grove is compatible with Python 2.7.

Install Grove
-------------

The preferred method for installing Grove is easy_install_ or pip_. ::

  easy_install grove

or ::

  pip install grove

Alternatively, you can download_ or clone_ the repository and build from sources. ::

  python setup.py install

.. _download: https://pypi.python.org/pypi/grove/
.. _clone: https://github.com/zivia/grove.git

.. _easy_install: https://pypi.python.org/pypi/setuptools
.. _pip: http://www.pip-installer.org/en/latest/

Grove also optionally uses the ETE Toolkit for graphing parse trees generated during grammatical evolution.
Installation through conda is required to use this feature. ::

  conda install grove
