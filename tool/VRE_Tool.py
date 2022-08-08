#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020-2021 Barcelona Supercomputing Center (BSC), Spain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import time
from glob import glob
from pathlib import Path

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool
from tool.ml_toolbox import run_ml_toolbox
from utils import logger

class MLToolboxRunner(Tool):
    """
    Tool for segmenting a file
    """
    MASKED_KEYS = {
        'execution',
        'project',
        'description'
    }  # arguments from config.json

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.info("VRE MLToolbox Workflow runner")
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        # Arrays are serialized
        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        self.populable_outputs = []
    
    def run(self, input_files, input_metadata, output_files):
        """
        The main function to run the compute_metrics tool.

        :param input_files: List of input files - In this case there are no input files required.
        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :param output_files: List of the output files that are to be generated.
        :type input_files: dict
        :type input_metadata: dict
        :type output_files: dict
        :return: List of files with a single entry (output_files), List of matching metadata for the returned files
        (output_metadata).
        :rtype: dict, dict
        """

        # print('INPUT FILES', input_files)
        # print('INPUT METADATA', input_metadata)
        # print('OUTPUT FILES', output_files)

        try:
            # Set and check execution directory. If not exists the directory will be created.
            execution_path = os.path.abspath(self.configuration.get('execution', '.'))
            execution_parent_dir = os.path.dirname(execution_path)
            if not os.path.isdir(execution_parent_dir):
                os.makedirs(execution_parent_dir)

            # Update working directory to execution path
            os.chdir(execution_path)
            logger.debug("Execution path: {}".format(execution_path))

            logger.debug("Init execution of the Segmentation")
            # Prepare file paths
            for key in input_files.keys():
                if key == 'images':
                    images = input_files[key]
                elif key == 'label_file':
                    label_file = input_files[key]
                elif key == 'segmentations':
                    segmentations = input_files[key]
                else:
                    logger.debug('Unrecognized key {}'.format(key))
                    continue
            # Create a custom config file for this execution
            template = get_config_template(input_metadata['output_folder'] + '/outputs')
            config_file_path = Path(input_metadata['output_folder']) / 'config.d' / 'config.py'
            config_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file_path, 'w') as f:
                f.write(template)
            logger.debug("Output metadata file: {}".format(config_file_path))
            
            # Make fastr to look for config file here
            os.environ["FASTRHOME"] = str(config_file_path.parent)

            # Run the MLToolbox
            outputs = run_ml_toolbox(self.configuration, images, segmentations, label_file, input_metadata['output_folder'])

            output_files = []
            out_meta = []
            # TODO parse outputs from run_ml_toolbox
            for _file, _meta in outputs:
                if os.path.isfile(_file):
                    meta = Metadata()
                    meta.file_path = _file  # Set file_path for output files
                    meta.data_type = 'sample_information_file'
                    meta.file_type = 'zip'
                    meta.meta_data = _meta
                    out_meta.append(meta)
                    output_files.append({
                        'name': 'outputs', 'file_path': _file
                    })
                else:
                    logger.warning("Output not found. Path \"{}\" does not exist".format(_file))

            output_metadata = {'output_files': out_meta}
            logger.debug("Output metadata created")

            return output_files, output_metadata

        except Exception:
            errstr = "VRE CWL RUNNER pipeline failed. See logs"
            logger.fatal(errstr)
            raise Exception(errstr)

def get_config_template(output_path):
    template = f"""
# THIS IS AN AUTOMATICALLY GENERATED FILE. ANY CHANGES WILL BE OVERWRITTEN.
import os
import fastr
import pkg_resources
import site
import sys

# Get directory in which packages are installed
working_set = pkg_resources.working_set
requirement_spec = pkg_resources.Requirement.parse('WORC')
egg_info = working_set.find(requirement_spec)
if egg_info is None:  # Backwards compatibility with WORC2
    try:
        packagedir = site.getsitepackages()[0]
    except AttributeError:
        # Inside virtualenvironment, so getsitepackages doesnt work.
        paths = sys.path
        for p in paths:
            if os.path.isdir(p) and os.path.basename(p) == 'site-packages':
                packagedir = p
else:
    packagedir = egg_info.location

# Add the WORC FASTR tools and type paths
tools_path = [os.path.join(packagedir, 'WORC', 'resources', 'fastr_tools')] + tools_path
types_path = [os.path.join(packagedir, 'WORC', 'resources', 'fastr_types')] + types_path

# Mounts accessible to fastr virtual file system
mounts['worc_example_data'] = os.path.join(packagedir, 'WORC', 'exampledata')
mounts['apps'] = os.path.expanduser(os.path.join('~', 'apps'))
mounts['output'] = '{output_path}'
mounts['test'] = os.path.join(packagedir, 'WORC', 'resources', 'fastr_tests')

# First option is to have a single shared folder where all the results from all the users are stored.
# Problem: each user will have their own random uuid directory without access outside this dir.
# Second option is to modify the config file before importing fastr.
# Problem: the user space and the source code is separated, so each user runs the same code. This is dangerous as one user can modify the run of another user.

# The ITKFile type requires a preferred type when no specification is given.
# We will set it to Nifti, but you may change this.
preferred_types += ["NiftiImageFileCompressed"]
    """
    return template
