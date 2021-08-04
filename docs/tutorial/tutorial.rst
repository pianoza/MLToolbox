.. currentmodule:: tool.VRE_Tool


Creating a tool
---------------

::

    from basic_modules.tool import Tool
    from utils import logger


Our first ``myTool``
~~~~~~~~~~~~~~~~~~~~

::

    class myTool(Tool):
        """
        This class define <myTool> Tool.
        """
        DEFAULT_KEYS = ['execution', 'project', 'description']
        """config.json default keys"""
        PYTHON_SCRIPT_PATH = "/example/hello.py"
        """<myApplication>"""


Adding input files
~~~~~~~~~~~~~~~~~~

In method toolExecution()...

::

    input_file_1 = input_files.get('hello_file')
    if not os.path.isabs(input_file_1):
        input_file_1 = os.path.normpath(os.path.join(self.parent_dir, input_file_1))


Adding arguments
~~~~~~~~~~~~~~~~

In method toolExecution()...

::

    argument_1 = self.arguments.get('username')
    if argument_1 is None:
        errstr = "argument_1 must be defined."
        logger.fatal(errstr)
        raise Exception(errstr)


Adding output files
~~~~~~~~~~~~~~~~~~~

In method run()...

::

    output_id = output_metadata[0]['name']
    output_type = output_metadata[0]['file']['file_type'].lower()
    output_file_path = glob(self.execution_path + "/*." + output_type)[0]
    if os.path.isfile(output_file_path):
        output_files[output_id] = [(output_file_path, "file")]


Command line tool
~~~~~~~~~~~~~~~~~

::

    if os.path.isfile(input_file_1):

        cmd = [
            'python',
            self.parent_dir + self.PYTHON_SCRIPT_PATH,  # hello.py
            input_file_1,  # hello.txt
            argument_1,  # username
        ]


.. currentmodule:: VRE_RUNNER


Reference tool into the wrapper
-------------------------------

::

    from tool.VRE_Tool import myTool


In method run()...

::

    tt_handle = myTool(self.configuration)


Adding software dependencies
----------------------------

::

    DEPENDENCIES=("Rscript", "docker")


Running the tool
----------------
