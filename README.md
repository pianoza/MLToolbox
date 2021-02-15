# VRE wrapper tool template

This is a simple example of a wrapper tool that can run in the VRE and is written for Python 3.6 or later.

## Requirements

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip python3-dev python3-venv
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

Change the path in `example/config.json`:

```
"arguments": [
  {
      "name": "execution",
      "value": "ADD_YOUR_LOCAL_PATH/example/run000"
  }
]

...

"output_files": [
    {
      "name": "results",
      "required": true,
      "allow_multiple": false,
      "file": {
        "file_path": "ADD_YOUR_LOCAL_PATH/example/run000/results.txt",
...
```

Change the path in `example/in_metadata.json`:
```
[
  {
    "_id": "unique_file_id_5e14abe0a37012.29503907",
    "type": "file",
    "file_path": "ADD_YOUR_LOCAL_PATH/example/data/hello.txt",
...
```

### Usage

```bash
./VRE_RUNNER --config example/config.json --in_metadata example/in_metadata.json --out_metadata out_metadata.json --log_file VRE_RUNNER.log
```
