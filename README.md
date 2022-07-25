# EuCanImage - VRE Machine Learning Toolbox 

<!-- [![Documentation Status](https://readthedocs.org/projects/vre-template-tool/badge/?version=latest)](https://vre-template-tool.readthedocs.io/en/latest/?badge=latest) -->

### &#128679; Under development (ETA: September 30, 2022)

This repository hosts the source code for the Machine Learning Toolbox of the EuCanImage project funded by Horizon-2020

## Requirements

- Python 3.6 or later
- [Git](https://git-scm.com/downloads)
- WORC

```bash
sudo apt update
sudo apt install python3
sudo apt install git
```

In order to install the Python dependencies you need `pip` and `venv` modules.

```bash
sudo apt install python3-pip python3-venv
```

## Installation

Directly from GitHub:

```bash
cd $HOME
git clone https://github.com/inab/vre_template_tool.git
cd vre_template_tool
```

Create the Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade wheel
pip install -r requirements.txt
```

## Run the Wrapper

```bash
./VRE_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_RUNNER.log
```

Look for the results in `tests/basic/run000/`.

## License
* © 2020-2021 Barcelona Supercomputing Center (BSC), ES

Licensed under the Apache License [Version 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file `LICENSE` for details.
