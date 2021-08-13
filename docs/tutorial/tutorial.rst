.. currentmodule:: tool.VRE_Tool


Creating a tool
---------------

Before you start creating your tool, the basic entity `Tool` of the `basic_modules` from the openvre-tool-api_ library
is imported.

.. _openvre-tool-api: https://github.com/inab/openvre-tool-api

::

    from basic_modules.tool import Tool

The `Tool` entity is the top-level wrapper for tools within the VRE, that for each tool define the input and output
formats and specify its requirements on the execution environment.

Your first `myTool`
~~~~~~~~~~~~~~~~~~~~~

`myTool` is a class that you define and the wrapper uses to run your application. You must define the location of your
application to run, e.g. ``/example/hello.py``.

You can see the first lines of `myTool` class saved in a file named ``VRE_tool.py`` under the ``tool/`` directory from
the project’s top level directory. In this class, we define the application we want to run using the wrapper. The
application can be implemented in different programming languages, such as Python or R, taking into account how to
execute it. To see how to execute your application see `Command line tool`_ section.

::

    class myTool(Tool):
        """
        This class define <myTool> Tool.
        """
        DEFAULT_KEYS = ['execution', 'project', 'description']
        """config.json default keys"""
        PYTHON_SCRIPT_PATH = "/example/hello.py"
        """<myApplication>"""

    ... (omitted for brevity)

`myTool` class defines two attributes and some methods. Specifically:

* :attr:`~tool.VRE_Tool.myTool.DEFAULT_KEYS`: identifies default arguments from openVRE configuration file (``config.json``).

* :attr:`~tool.VRE_Tool.myTool.PYTHON_SCRIPT_PATH`: location of your application that you wanna run with the wrapper.
    You can use a relative or absolute path.

* :meth:`~tool.VRE_Tool.myTool.run()`: `TO BE DOCUMENTED` ...

* :meth:`~tool.VRE_Tool.myTool.toolExecution()`: `TO BE DOCUMENTED` ...


Adding input files
~~~~~~~~~~~~~~~~~~

If your application expects one or more input files, you must add them as follows in the method
:meth:`~tool.VRE_Tool.myTool.toolExecution()`:

::

    input_file_1 = input_files.get('hello_file')
    if not os.path.isabs(input_file_1):
        input_file_1 = os.path.normpath(os.path.join(self.parent_dir, input_file_1))

For each input file, you must add a new variable. The VRE works with absolute paths and as you can see, it is
preferable to check if the directory is absolute or not; which in case it is not, becomes absolute.

Adding arguments
~~~~~~~~~~~~~~~~

If your application expects one or more arguments, you must add them as follows in the method
:meth:`~tool.VRE_Tool.myTool.toolExecution()`:

::

    argument_1 = self.arguments.get('username')
    if argument_1 is None:
        errstr = "argument_1 must be defined."
        logger.fatal(errstr)
        raise Exception(errstr)

For each argument, you must add a new variable and validate their import from the configuration file (``config.json``)
to ensure execution.

Adding output files
~~~~~~~~~~~~~~~~~~~

If your application expects one or more output files, you must add them as follows in the method
:meth:`~tool.VRE_Tool.myTool.toolExecution()`:

::

    output_id = output_metadata[0]['name']
    output_type = output_metadata[0]['file']['file_type'].lower()
    output_file_path = glob(self.execution_path + "/*." + output_type)[0]
    if os.path.isfile(output_file_path):
        output_files[output_id] = [(output_file_path, "file")]


Command line tool
~~~~~~~~~~~~~~~~~

::

    cmd = [
        'python',
        self.parent_dir + self.PYTHON_SCRIPT_PATH,  # hello.py
        input_file_1,  # hello.txt
        argument_1,  # username
    ]


.. currentmodule:: VRE_RUNNER


Reference tool into the wrapper
-------------------------------

`TO BE DOCUMENTED` ...

::

    from tool.VRE_Tool import myTool


In method run()...

::

    tt_handle = myTool(self.configuration)


Adding software dependencies
----------------------------

If you need some software requirements to run your application, you must add them to the file VRE_RUNNER_, in the
project's top level directory.

.. _VRE_RUNNER: https://github.com/inab/vre_template_tool/blob/master/VRE_RUNNER

::

    DEPENDENCIES=("Rscript", "docker")


Running the tool
----------------

To put the tool to work, go to the project's top level directory and run:

::

    ./VRE_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_RUNNER.log

This command runs the tool that we've just created and you will get an output similar to this:

::

    2021-08-06 13:08:34 | INFO: 0) Unpack information from JSON
    2021-08-06 13:08:34 | INFO: 1) Instantiate and Configure Tool
    2021-08-06 13:08:34 | INFO: 2) Run Tool
    2021-08-06 13:08:34 | PROGRESS: <myApplication> execution finished successfully - FINISHED
    2021-08-06 13:08:34 | INFO: 3) Create information
    2021-08-06 13:08:34 | INFO: 4) Pack information to JSON
    2021-08-06 13:08:34 | PROGRESS: <myTool> tool successfully executed;

Now, check the files in the ``run000`` directory. You should notice that a new file has been created: ``output_metadata.json``,
with the content for the respective results, as the `run` method instructs.

.. note:: If you are wondering about the ``run000`` directory, you can see an example in the :doc:`Examples Section</examples>`.

What just happened under the execution?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`TO BE DOCUMENTED` ...