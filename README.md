# VRE Sample Tool

A simple example tool that is ready to run a workflow

## Requirements
- Python 3.6.9+
- Python3-dev and Python3-venv
- Python Modules:
  - pylint
  - pytest
  - mg-tool-api: https://github.com/Multiscale-Genomics/mg-tool-api.git
  - cwltool: https://github.com/common-workflow-language/cwltool.git

Installation
------------

Directly from GitHub:

```
cd ${HOME}/user

git clone https://github.com/inab/vre_cwl_executor.git

cd vre_cwl_executor
```

Create the Python environment

```
python3 -m venv ${HOME}/user/vre_cwl_executor/venv
source venv/bin/activate
pip install -r requirements.txt
```
