# VRE template tool

Simple example tool that is ready to run in the VRE.

## Requirements

- Python 3.6 or +x
- Python3.6-pip, Python3.6-dev and Python3.6-venv or +
- Git

```bash
sudo apt update
sudo apt install python3.6 
sudo apt install python3.6-pip python3.6-dev  python3.6-venv
sudo apt install git
sudo apt install docker-ce
```

Remember to add your username to the `docker` group.

 ```bash
 sudo usermod -a -G docker $USER
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
python3 -m venv $HOME/vre_template_tool/venv
source venv/bin/activate
pip install --upgrade wheel
pip install -r requirements.txt
```

## Configuration

Change user with your username in `tests/basic/config.json`:

```json
"arguments": [
  {
      "name": "execution",
      "value": "/home/user/vre_template_tool/tests/basic/run000"
  }
],
"output_files": [
  {
      "name": "bam_file",
      "required": true,
      "allow_multiple": false,
      "file": {
          "file_path": "/home/user/vre_template_tool/tests/basic/run000/A.bam"
      }
   }
]

```

and `tests/basic/in_metadata.json`:

```json
{
    "_id": "unique_file_id_5e14abe0a37012.29503907",
    "file_path": "/home/user/vre_template_tool/tests/basic/NA12878.bam"
},
{
    "_id": "unique_file_id_5e14abe0a37012.29503908",
    "file_path": "/home/user/vre_template_tool/tests/basic/hg38.fa"
{
```

## Run the example

```bash
./VRE_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_RUNNER.log
```
