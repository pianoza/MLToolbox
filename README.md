# VRE wrapper template

Simple example of a wrapper that can run in the VRE.

## Requirements
This simple example is written for Python 3.6 or later.

- python3-pip, python3-dev and python3-venv
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [docker](https://docs.docker.com/get-docker/)

```bash
sudo apt update
sudo apt install python3.6 
sudo apt install python3-pip python3-dev  python3-venv
sudo apt install git
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

## Example
### Configuration

Change the execution path in `example/config.json`:

```json 
"arguments": [
  {
      "name": "execution",
      "value": "ADD_YOUR_LOCAL_PATH/run000"
  }
]
```

### Usage

```bash
./VRE_RUNNER --config example/config.json --in_metadata example/in_metadata.json --out_metadata example/out_metadata.json --log_file example/example.log
```
