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
import shutil

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool
from utils import logger


class myTool(Tool):
    """
    Class to define a Tool
    """
    # default keys of arguments from config.json
    DEFAULT_ARGUMENTS = {'execution', 'project', 'description'}

    def __init__(self):
        """
        Init function
        """
        logger.debug("Initialise the tool {} with its configuration.".format(Tool.__name__))
        Tool.__init__(self)

        # Variables initialization
        self.execution_path = os.path.abspath(self.configuration.get('execution', '.'))
        self.outputs = {}
        self.arguments = []
        for conf_key in self.configuration.keys():
            if conf_key not in self.DEFAULT_ARGUMENTS:
                self.arguments.append((conf_key, self.configuration[conf_key]))

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_files: Dictionary of output files locations expected to be generated.
        :type output_files: dict
        :param output_metadata: # TODO add
        :type output_metadata: list
        :return: Locations for the output txt (output_files), Matching metadata for each of the files (output_metadata). # TODO change
        :rtype: dict, dict
        """
        try:
            # Set and validate execution directory. If not exists the execution directory will be created.
            if not os.path.isdir(self.execution_path):
                os.makedirs(self.execution_path)

            execution_parent_dir = os.path.dirname(self.execution_path)
            if not os.path.isdir(execution_parent_dir):
                os.makedirs(execution_parent_dir)

            os.chdir(self.execution_path)

            # Call application command to execute
            logger.debug("Launch application")
            retVal = self.myToolExecution(input_metadata, self.execution_path)   # TODO adapt this method to your application

            # Save and validate the output files of execution
            for key in output_files.keys():
                if output_files[key] is not None:
                    output_path = os.path.abspath(output_files[key])
                    self.outputs[key] = output_path
                    output_files[key] = output_path
                else:
                    errstr = "The output_file[{}] can not be located. Please specify its expected path.".format(key)
                    logger.error(errstr)
                    raise Exception(errstr)

            # Create output metadata from execution
            output_metadata = self.create_output_metadata(input_metadata, output_metadata)

            # Clean tmp files
            shutil.rmtree(self.execution_path + "/intermediate.txt") # TODO

            if retVal != 0:
                raise Exception("")

            return output_files, output_metadata

        except:
            errstr = "Tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def myToolExecution(self, input_metadata, execution_path):
        """
        The main function to run the tool.

        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param execution_path: Execution working directory
        :type execution_path: str
        """
        # TODO put command line to run your application
        cmd = [
            'echo Hello VRE developer! Change this method, to call your application.',
            'echo This dummy application creates {}'.format(self.execution_path + "/intermediate.txt"),
            'touch intermediate.txt',
            'echo This dummy application creates {}'.format(self.execution_path + "/results.txt"),
            'touch results.txt'
        ]

        # Tool execution
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Sending the stdout to the log file
        for line in iter(process.stderr.readline, b''):
            print(line.rstrip().decode("utf-8").replace("", " "))

        rc = process.poll()
        while rc is None:
            rc = process.poll()
            time.sleep(0.1)

        if rc is not None and rc != 0:
            logger.progress("Something went wrong inside the tool execution. See logs", status="WARNING")
        else:
            logger.progress("Tool execution finished successfully", status="FINISHED")

        return process.returncode

    @staticmethod
    def create_output_metadata(input_metadata, output_metadata):
        """
        Create returned output metadata from input metadata and output metadata from output files.

        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param output_metadata: List of matching metadata for the output files
        :type output_metadata: list
        :return: List of matching metadata for the returned files (result).
        :rtype: dict
        """
        try:
            result = dict()
            for output_file in output_metadata:  # for each output file
                output_filename = output_file["name"]
                meta = Metadata()

                # Set file_path for output files
                meta.file_path = output_file["file"].get("file_path", None)

                # Set data and file types of output_file
                meta.data_type = output_file["file"].get("data_type", None)
                meta.file_type = output_file["file"].get("file_type", None)

                # Set sources for output file from input_metadata
                meta_sources_list = list()
                for input_name in input_metadata.keys():
                    meta_sources_list.append(input_metadata[input_name][1].file_path)

                meta.sources = meta_sources_list

                # Set output file metadata
                meta.meta_data = output_file["file"].get("meta_data", None)

                # Add new element in output_metadata
                result.update({output_filename: meta})

            logger.debug("Output metadata created.")
            return result

        except:
            errstr = "Output metadata not created. See logs"
            logger.error(errstr)
            raise Exception(errstr)
