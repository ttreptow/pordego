pordego
=======
Static analysis tool for Python for integration with CI tools

Summary
-------
Pordego provides a simple, pluggable command line tool for executing various static analyses such as
code complexity, dependency analysis, etc.. The goal is to provide a simple, configurable tool that CI software such as Bamboo can call as a step in the build process.

The pordego package itself only contains the command line tool (also called "pordego") and the configuration parser.
The actual analyses are performed by additional packages (see below for a list of known packages)

"Pordego" means "gate" in Esperanto. The tool acts as a gate for the CI process and keeps crappy code out.

Installation
------------
The easiest way to install is to run

.. code-block:: bash

    $ pip install pordego

This will install the command line tool, which does not do much on it's own. You will want to install one or more plugins, such as:

.. code-block:: bash

    $ pip install pordego-complexity

pordego will automatically detect installed plugins

Usage
-----
Run the analyses:

.. code-block:: bash

    $ pordego run <path to config file>

Show the installed plugins:

.. code-block:: bash

    $ pordego show

Run Configuration File
######################
The pordego tool accepts a single configuration file in yml format. The configuration file has one top level configuration parameter called "plugins". The value of plugins is a list of plugin specific configuration. The plugin specific configuration must contain a parameter called "name" which must match the name of one of the instlalled plugins.

Plugins are exectued in the order they are specified in the file, and the same plugin can be executed multiple times with different configuration


Example
^^^^^^^
In this example, one plugin called "myplugin" will be run. The plugin takes two parameters, one of which is a list.

.. code-block:: yaml

    ---
    plugins:
      - name: myplugin
        myplugin_param_1: config val
        myplugin_param_2:
          - list item 1
          - list item 2

The "myplguin" entry point (see below) will be passed a dictionary containing (note that the "name" parameter is stripped out):

.. code-block:: python

    {
    "myplugin_param_1": "config val",
     "myplugin_param_2": ["list item 1", "list item 2"]
    }


Plugins
-------

Known Plugins
#############

======================================================================  ============  ===========
Python Package Name                                                     Maintainer    Description
======================================================================  ============  ===========
`pordego-complexity <https://github.com/ttreptow/pordego-complexity>`_  Tim Treptow   Uses the Radon package to check code complexity
======================================================================  ============  ===========

Plugin Development
##################
Pordego uses package entry points to discover plugins. Plugins packages must export an entrypont called "pordego.analysis".

Example:
^^^^^^^^
.. code-block:: python

   setup(
   ...
   entry_points={"pordego.analysis": ["myplugin = mypackage.mymodule:some_function"]},
   ...
   )

The function receives a dictionary containing the configuration for the plugin as specified in the file passed to pordego

Returning Errors and Succeess
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For simplicty's sake, the interaction between the pordego tool and the plugins is minimal. There are three states that a plugin can comminucate depending on what exceptions are raised.

* Don't raise an exception- pordego assumes that the plugin has passed
* raise AssertionError- pordego assumes that the condition that the plugin is checking (e.g. code complexity) has failed. Pordego prints out the exception but not a stack trace.
* raise any other exception- pordego assumes that the plugin or configuration is in error so it prints out a stack trace to aid in debugging