import os
from pathlib import Path
import json
import uuid
from time import time

from_dir = Path("/home/kaisar/EuCanImage/Coding/VRE/T5.3/Data/stwstrategyhn1")
csv_file = Path("/home/kaisar/EuCanImage/Coding/VRE/T5.3/Data/Examplefiles/pinfo_HN.csv")
execution_dir = Path("/home/kaisar/EuCanImage/Coding/VRE/MLToolbox/tests/run000")
image_name = "image.nii.gz"
mask_name = "mask.nii.gz"
max_load = 10

# list all folders in from_dir
folders = [f for f in from_dir.iterdir() if f.is_dir()]
in_metadata = []
config = {}

csv_id = str(uuid.uuid4())
# add csv_file to config
config["output_files"] = [
        {
            "file": {
                "file_type": "zip",
                "file_path": str(execution_dir / "outputs" / "run000.zip"),
                "meta_data": {},
                "data_type": "sample_information_file"
            },
            "required": True,
            "allow_multiple": False,
            "name": "outputs"
        }
]
config["arguments"] = [
    {
        "value": str(execution_dir),
        "name": "execution"
    },
    {
        "value": "my_project_id",
        "name": "project"
    },
    {
        "value": "ml_toolbox",
        "name": "description"
    }
]
config["input_files"] = [{
    "value": csv_id,
    "required": True,
    "allow_multiple": False,
    "name": "label_file"
}]

# add csv_file to in_metadata
in_metadata.append({
    "_id": csv_id,
    "file_path": str(csv_file),
    "file_type": "CSV",
    "data_type": "sample_information_file",
    "compressed": 0,
    "user_id": "user_id",
    "creation_time": {
        "sec": int(time()),
        "usec": 0
    },
    "meta_data": {
        "type": "dir",
        "size": 0,
        "project": "my_project_id",
        "atime": {
            "sec": int(time()),
            "usec": 0
        },
        "parentDir": "unique_file_id_5e14abe0a37742.64003100",  # don't know what this is
        "lastAccess": {
            "sec": int(time()),
            "usec": 0
        }
    },
    "sources": []
})


for folder in folders[:max_load]:
    img_id = str(uuid.uuid4())
    mask_id = str(uuid.uuid4())
    config_item_images = {
        "value": img_id,
        "required": True,
        "allow_multiple": True,
        "name": "images"
    }
    config_item_segmentations = {
        "value": mask_id,
        "required": True,
        "allow_multiple": True,
        "name": "segmentations"
    }

    config["input_files"].append(config_item_images)
    config["input_files"].append(config_item_segmentations)

    image_item = {
        "_id": img_id,
        "file_path": str(folder/image_name),
        "file_type": "NIFTI",
        "data_type": "bioimage",
        "compressed": "GZ",
        "user_id": "user_id",
        "creation_time": {
            "sec": int(time()),
            "usec": 0
        },
        "meta_data": {
            "type": "file",
            "size": 0,
            "project": "my_project_id",
            "atime": {
                "sec": int(time()),
                "usec": 0
            },
            "parentDir": "unique_file_id_5e14abe0a37742.64003100",  # don't know what this is
            "lastAccess": {
                "sec": int(time()),
                "usec": 0
            }
        },
        "sources": []
    }
    mask_item = {
        "_id": mask_id,
        "file_path": str(folder/mask_name),
        "file_type": "NIFTI",
        "data_type": "bioimage",
        "compressed": "GZ",
        "user_id": "user_id",
        "creation_time": {
            "sec": int(time()),
            "usec": 0
        },
        "meta_data": {
            "type": "file",
            "size": 0,
            "project": "my_project_id",
            "atime": {
                "sec": int(time()),
                "usec": 0
            },
            "parentDir": "unique_file_id_5e14abe0a37742.64003100",  # don't know what this is
            "lastAccess": {
                "sec": int(time()),
                "usec": 0
            }
        },
        "sources": []
    }

    in_metadata.append(image_item)
    in_metadata.append(mask_item)

# save config to json
with open("config.json", "w") as f:
    json.dump(config, f, indent=4)

# save in_metadata to json
with open("in_metadata.json", "w") as f:
    json.dump(in_metadata, f, indent=4)
