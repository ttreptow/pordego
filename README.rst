pordego
=======

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
    $ pip install pordego-dependency

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
The pordego tool accepts a single configuration file in yml format.
The configuration file has top level configuration parameters called "analysis" and "output" for configuring the analysis and output plugins respectivly.
The values of "analysis" and "output" are lists of plugin specific configuration. The results of all the confiugured analyses are passed to all the output plugins.

The plugin specific configuration must contain a parameter called "plugin_name" which must match the name of one of the instlalled plugins of the section type.
Plugin configurations can optionally specify a parameter called "name" that is passed to the output instead of the plugin name.
This is useful for distinguishing analyses when the sam analysis plugin is run with multiple configurations.

Plugins are exectued in the order they are specified in the file (excpet that analyses are always executed before output regardless of the position of the analysis and output configs), and the same plugin can be executed multiple times with different configuration


Example
^^^^^^^
In this example, one plugin called "myplugin" will be run twice with different configs. The output is sent to stdout. The plugin takes two parameters, one of which is a list.

.. code-block:: yaml

    ---
    analysis:
      - plugin_name: myplugin
        name: Check config 1
        myplugin_param_1: config val
        myplugin_param_2:
          - list item 1
          - list item 2
      - plugin_name: myplugin
        name: Check config 2
        myplugin_param_1: some other val
        myplugin_param_2:
          - list item 7
    output:
      - plugin_name: stdout

The "myplugin" entry point (see below) will be passed a dictionary containing (note that the "plugin_name" parameter is stripped out):

.. code-block:: python

    {
    "name": "Check config 1"
    "myplugin_param_1": "config val",
    "myplugin_param_2": ["list item 1", "list item 2"]
    }

And then it will be executed again with

.. code-block:: python

    {
    "name": "Check config 2"
    "myplugin_param_1": "some other val",
    "myplugin_param_2": ["list item 7"]
    }

It is also possible to include plugin configurations. For example, in the main config file:

.. code-block:: yaml

    ---
    analysis:
      - include: myplugin_config.yml

The contents of myplugin_config.yml are:

.. code-block:: yaml

    ---
    - plugin_name: myplugin
      name: Check config 1
      myplugin_param_1: config val
      myplugin_param_2:
        - list item 1
        - list item 2

Note that the included file only has a list of plugins, not the "analysis" tag.
It is possible to recursively include files in included files as well as to have plugin configurations and include statements in the same file.


Plugins
-------

Known Analysis Plugins
######################

===========  ===========  =======================================================  ========
Plugin Name  Maintainer   Description                                              Python Package Name
===========  ===========  =======================================================  ========
complexity   Tim Treptow  Uses the Radon package to check code complexity          `pordego-complexity <https://github.com/ttreptow/pordego-complexity>`_
dependency   Tim Treptow  Uses the snakefood package to test package dependencies  `pordego-dependency <https://github.com/ttreptow/pordego-dependency>`_
===========  ===========  =======================================================  ========

Known Output Plugins
####################

===========  ===========  =====================================================  ========
Plugin Name  Maintainer   Description                                            Python Package Name
===========  ===========  =====================================================  ========
stdout       Tim Treptow  Dumps results to stdout                                pordego (builtin)
junit        Tim Treptow  Dumps results to a junit file                          pordego (builtin)
===========  ===========  =====================================================  ========

Analysis Plugin Development
###########################
Pordego uses package entry points to discover analysis plugins. Plugins packages must export an entrypont called "pordego.analysis".

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

Output Plugin Development
#########################

Output plugins are specified with the "pordego.output" entry point. The entry point function must take two parameters.

The first parameter is a list of plugin outputs.
Each list item is a tuple containing:

0. the analysis name as specified by the "name" parameter in the analysis plugin config, or the plugin name if "name" does not exist.
1. The second parameter is a string containing a failure message or None if the plugin did not fail.
2. The third parameter is a tuple containing exception info (as returned by sys.exc_info()) if there was an error with the test, or None if there was no error

The second parameter to the output plugin entry point is the plugin configuration as specified in the configuration file