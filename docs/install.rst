Requirements and Installation
=============================

Requirements
------------

Software
^^^^^^^^

- Python 3.6+

Python Modules
^^^^^^^^^^^^^^

- `openvre-tool-api <https://github.com/inab/openvre-tool-api>`_

Installation
------------

Directly from GitHub:

.. code-block:: none
   :linenos:

   git clone https://github.com/inab/vre_template_tool.git

Using pip:

.. code-block:: none
   :linenos:

   pip install git+https://github.com/inab/vre_template_tool.git

Documentation
-------------

To build the documentation:

.. code-block:: none
   :linenos:

   pip install Sphinx
   pip install sphinx-autobuild
   cd docs
   make html
