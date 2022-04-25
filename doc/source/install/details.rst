Detailed installation instructions
==================================

Pyrocko can be installed under any operating system where its prerequisites are
available. This document describes details about its requirements which are
needed when a standard install is not possible or conflicts arise.

**For standard install instructions, head on over to**

* :doc:`system/index`

Prerequisites
-------------

The following software packages must be installed before Pyrocko can be
installed from source:

* Build requirements
   * C compiler (tested with gcc, clang and MSVC)
   * ``patch`` utility
   * `NumPy <http://numpy.scipy.org/>`_ (>= 1.6, with development headers)

* Try to use normal system packages for these Python modules:
   * `Python <http://www.python.org/>`_ (>= 3.5, with development headers)
   * `NumPy <http://numpy.scipy.org/>`_ (>= 1.6, with development headers)
   * `SciPy <http://scipy.org/>`_
   * `matplotlib <http://matplotlib.sourceforge.net/>`_ (with Qt5 backend)
   * `pyyaml <https://bitbucket.org/xi/pyyaml>`_
   * `PyQt5 <http://www.riverbankcomputing.co.uk/software/pyqt/intro>`_ (only needed for the GUI apps)
   * `requests <http://docs.python-requests.org/en/master/>`_

* Optional Python modules:
   * `progressbar2 <http://pypi.python.org/pypi/progressbar2>`_
   * `Jinja2 <http://jinja.pocoo.org/>`_ (required for the :ref:`fomosto report <fomosto_report>` subcommand)
   * `nosetests <https://pypi.python.org/pypi/nose>`_ (to run the unittests)
   * `coverage <https://pypi.python.org/pypi/coverage>`_ (unittest coverage report)

* Manually install these optional software tools:
   * `GMT <http://gmt.soest.hawaii.edu/>`_ (4 or 5, only required for the :py:mod:`pyrocko.plot.automap` module)
   * `slinktool <http://www.iris.edu/data/dmc-seedlink.htm>`_ (optionally, if you want to use the :py:mod:`pyrocko.streaming.slink` module)
   * `rdseed <http://www.iris.edu/software/downloads/rdseed_request.htm>`_ (optionally, if you want to use the :py:mod:`pyrocko.io.rdseed` module)
   * `QSEIS <https://git.pyrocko.org/pyrocko/fomosto-qseis>`_ (optional, needed for the Fomosto ``qseis.2006a`` backend)
   * `QSSP <https://git.pyrocko.org/pyrocko/fomosto-qssp>`_ (optional, needed for the Fomosto ``qssp.2010`` backend)
   * `PSGRN/PSCMP <https://git.pyrocko.org/pyrocko/fomosto-psgrn-pscmp>`_ (optional, needed for the Fomosto ``psgrn.pscmp`` backend)

Download, compile and install Pyrocko from source
-------------------------------------------------

The following examples will install Pyrocko on Linux or MacOS. For Windows
source installs, please refer to :ref:`Installation on Windows: From source
<windows-install-from-source>`.

.. highlight:: sh

1. Download (clone) the Pyrocko project directory with *git*::

    cd ~/src/   # or wherever you keep your source packages
    git clone https://git.pyrocko.org/pyrocko/pyrocko.git pyrocko

2. Change to the Pyrocko project directory::

   cd ~/src/pyrocko/

3. Install prerequisites using your method of choice::

    # (a) If you manage your installations with the system's package manager:
    python3 ./install_prerequisites.py

    # or (b), if you manage your installations with pip:
    pip3 install -r requirements.txt

    # or (c), if you manage your installations with conda:
    conda install --file requirements.txt

4. Build and install Pyrocko::

    # If you want to install for single user:
    pip3 install --no-deps --no-build-isolation --force-reinstall .

    # or, if you want to install system wide:
    sudo pip3 install --no-deps --no-build-isolation --force-reinstall .

**Note:** If you do not specify `--no-deps`, pip will automatically download
and install missing dependencies. Unless you manage your installations
exclusively with pip, omitting this flag can lead to conficts.

**Note:** The intention of using `--no-build-isolation` is to compile exactly
against the already installed prerequisites. If you omit the flag, pip will
compile against possibly newer versions which it downloads and installs into a
temporary, isolated environment.

**Note:** If you have previously installed Pyrocko using other tools like e.g.
*pip*, or *conda*, you should first remove the old installation. Otherwise you
will end up with two parallel installations which will cause trouble.

Update
------

If you later would like to update Pyrocko, run the following commands (this
assumes that you have used *git* to download Pyrocko).

Change to the Pyrocko project directory (step 2. above), then update it::

    git pull origin master --ff-only

**Then build and reinstall Pyrocko as descibed in step 4.**
