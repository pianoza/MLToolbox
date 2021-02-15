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

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool
from utils import logger


class myTool(Tool):
    """
    Class to define a Tool
    """

    def __init__(self, configuration=None):
        """
        Init function

        :param configuration: a dictionary containing parameters that define how the operation should be carried out,
        which are specific to each Tool.
        :type configuration: dict
        """
        Tool.__init__(self)
        # logger.debug("Initialized the tool {} with its configuration.".format(self.__class__.__name__))

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        # Class variables initialization
        self.execution_path = os.path.abspath(self.configuration.get('execution', '.'))
        self.arguments = self.configuration

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
        # Set and validate execution directory. If not exists the execution directory will be created.
        if not os.path.isdir(self.execution_path):
            os.makedirs(self.execution_path)

        execution_parent_dir = os.path.dirname(self.execution_path)
        if not os.path.isdir(execution_parent_dir):
            os.makedirs(execution_parent_dir)

        os.chdir(self.execution_path)

        # Call application command to execute
        retVal = self.myToolExecution(input_files)  # TODO adapt this method to your application

        # Save and validate the output files of execution
        if len(output_files) != 0:
            for key in output_files.keys():
                if output_files[key] is not None:
                    output_path = os.path.abspath(output_files[key])
                    output_files[key] = output_path
                else:
                    errstr = "The output_file[{}] can not be located. Please specify its expected path.".format(key)
                    logger.error(errstr)
                    raise Exception(errstr)

        # Create output metadata from execution
        output_metadata = self.create_output_metadata(input_metadata, output_metadata)

        if retVal != 0:
            errstr = "Tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

        return output_files, {}

    def myToolExecution(self, input_files):
        """
        The main function to run the tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :return: # TODO
        :rtype: int
        """
        # Get input files # TODO add input files to use, if it is necessary for you
        input_file_1 = input_files.get("hello_file")

        # Get arguments # TODO add arguments to use, if it is necessary for you
        argument_1 = self.arguments.get("username")

        cmd = [
            '''
            cat {0}
            echo "Goodbye {1}!" >> results.txt
            cat results.txt
            '''.format(input_file_1, argument_1)
        ]  # TODO change command line to run your application

        # Tool execution
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # Sending the stdout to the log file
        for line in iter(process.stdout.readline, b''):
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

        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_metadata: # TODO add
        :type output_metadata: list
        :return: List of matching metadata for the returned files (result).
        :rtype: dict
        """
        try:
            result = dict()
            for output_file in output_metadata:
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

            return result

        except:
            errstr = "Output metadata not created. See logs"
            logger.error(errstr)
            raise Exception(errstr)
