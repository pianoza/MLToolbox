# VRE Sample Tool

A simple example tool that is ready to run a workflow.

## Requirements

* Install the dependencies used by the Wrapper.

```bash
sudo apt update
sudo apt install git
sudo apt install docker-ce
```

Remember to add your username to the `docker` group.

 ```bash
 sudo usermod -a -G docker $USER
 ```
 
* Install the Wrapper dependencies.

    - Python 3.6 or +
    - Python3.6-pip, Python3.6-dev and Python3.6-venv or +

## Installation

Directly from GitHub:

```bash
cd $HOME

git clone https://github.com/inab/vre_sample_tool.git

cd vre_sample_tool
```

Create the Python environment:

```bash
python3 -m venv $HOME/vre_sample_tool/venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Add your ${USER} in `tests/basic/config.json`:

```json 
"arguments": [
  {
      "name": "execution",
      "value": "/home/${USER}/vre_sample_tool/tests/basic/run000"
  }
],
"output_files": [
  {
      "name": "bam_file",
      "required": true,
      "allow_multiple": false,
      "file": {
          "file_path": "/home/${USER}/vre_sample_tool/tests/basic/run000/A.bam"
      }
   }
]
```
and `tests/basic/in_metadata.json`:

```json 
{
    "_id": "unique_file_id_5e14abe0a37012.29503907",
    "file_path": "/home/${USER}/vre_sample_tool/tests/basic/NA12878.bam"
},
{
    "_id": "unique_file_id_5e14abe0a37012.29503908",
    "file_path": "/home/${USER}/vre_sample_tool/tests/basic/hg38.fa"
{
``` 
and `/test/basic/input_basic_example.yml`:

```yaml 
  input_reads: 
    class: File
    location: /home/${USER}/vre_sample_tool/tests/basic/NA12878.bam
  biospecimen_name: "hg38"
  indexed_reference_fasta:
    class: File 
    location: /home/${USER}/vre_sample_tool/tests/basic/hg38.fa
```
## Run the example
```bash
./VRE_CWL_RUNNER --config tests/basic/config.json --in_metadata tests/basic/in_metadata.json --out_metadata out_metadata.json --log_file VRE_CWL_RUNNER.log
```
