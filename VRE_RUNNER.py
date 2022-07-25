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

import argparse
import sys

from utils import logger
from apps.jsonapp import JSONApp
from tool.VRE_Tool import MLToolboxRunner

def main_wrapper(config_path, in_metadata_path, out_metadata_path):
    """
    Main function.

    This function launches the tool using configuration written in two json files: config.json and in_metadata.json.

    :param config_path: Path to a valid VRE JSON file containing information on how the tool should be executed.
    :type config_path: str
    :param in_metadata_path: Path to a valid VRE JSON file containing information on tool inputs.
    :type in_metadata_path: str
    :param out_metadata_path: Path to write the VRE JSON file containing information on tool outputs.
    :type out_metadata_path: str
    :return: If result is True, execution finished successfully. False, otherwise.
    :rtype: bool
    """
    try:
        app = JSONApp()

        result = app.launch(MLToolboxRunner, config_path, in_metadata_path, out_metadata_path)
        logger.progress("<myTool> tool successfully executed; see {}".format(out_metadata_path))
        return result

    except Exception as error:
        errstr = "<myTool> tool wasn't successfully executed. ERROR: {}.".format(error)
        logger.error(errstr)
        raise Exception(errstr)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="VRE <myTool> Tool")
    PARSER.add_argument("--config", help="Location of configuration file", required=True)
    PARSER.add_argument("--in_metadata", help="Location of input metadata file", required=True)
    PARSER.add_argument("--out_metadata", help="Location of output metadata file", required=True)
    PARSER.add_argument("--log_file", help="Location of the log file", required=False)

    ARGS = PARSER.parse_args()

    CONFIG = ARGS.config
    IN_METADATA = ARGS.in_metadata
    OUT_METADATA = ARGS.out_metadata

    if ARGS.log_file:
        sys.stderr = sys.stdout = open(ARGS.log_file, "w")

    RESULTS = main_wrapper(CONFIG, IN_METADATA, OUT_METADATA)
