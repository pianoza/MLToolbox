from pathlib import Path
import shutil

from_dir = Path("/home/kaisar/EuCanImage/Coding/VRE/T5.3/Data/stwstrategyhn1")
csv_file = Path("/home/kaisar/EuCanImage/Coding/VRE/T5.3/Data/Examplefiles/pinfo_HN.csv")
to_dir = Path("/home/kaisar/EuCanImage/Coding/VRE/T5.3/Data/stwstrategyhn2")
image_name = "image.nii.gz"
mask_name = "mask.nii.gz"

# list all folders in from_dir
folders = [f for f in from_dir.iterdir() if f.is_dir()]

for f in folders:
    pid = f.name
    new_img_name = pid + "_image_0.nii.gz"
    new_msk_name = pid + "_mask_0.nii.gz"
    shutil.copyfile(str(f / image_name), str(to_dir / new_img_name))
    shutil.copyfile(str(f / mask_name), str(to_dir / new_msk_name))
