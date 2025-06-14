Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-bd3491fs/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/bd3491fs/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_BD3491FS/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_BD3491FS/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython library for the Rohm BD3491FS Audio Processor


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
--------------------
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-bd3491fs/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-bd3491fs

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-bd3491fs

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-bd3491fs

Usage Example
=============

.. code-block:: python

    import board
    import adafruit_bd3491fs
    import busio

    i2c = busio.I2C(board.SCL, board.SDA)
    bd3491fs = adafruit_bd3491fs.BD3491FS(i2c)

    bd3491fs.active_input = adafruit_bd3491fs.Input.A
    bd3491fs.input_gain = adafruit_bd3491fs.Level.LEVEL_20DB
    bd3491fs.channel_1_attenuation = 0
    bd3491fs.channel_2_attenuation = 0

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/bd3491fs/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BD3491FS/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
