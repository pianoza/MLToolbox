********
Examples
********

The best way to learn is with examples, and ``vre_template_tool`` is no exception. For this
reason, there is an example you can test and it is available at `tests/basic/`_ directory.

.. _tests/basic/: https://github.com/inab/vre_template_tool/tree/master/tests/basic/


Default structure
~~~~~~~~~~~~~~~~~

Before delving into the details, let's first understand the directory of a test. Though it
can be modified, all VRE Tool projects have the same file structure by default, similar
to this:

::

    tests/basic/
         config.json
         in_metadata.json
         README.md
         test_VRE_RUNNER.sh


Configuration files
~~~~~~~~~~~~~~~~~~~

``config.json``

.. literalinclude :: ../tests/basic/config.json
   :language: json

``in_metadata.json``

.. literalinclude :: ../tests/basic/in_metadata.json
   :language: json


Running the example
~~~~~~~~~~~~~~~~~~~

Results
=======

This will create a ``run000`` directory with the following contents:

::

    run000/
        goodbye.txt
        out_metadata.json
        tool.log
