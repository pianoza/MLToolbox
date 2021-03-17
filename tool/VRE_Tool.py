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

from basic_modules.tool import Tool
from utils import logger


class myTool(Tool):
    """
    This class define <myTool> Tool.
    """
    DEFAULT_KEYS = ['execution', 'project', 'description']  # config.json default keys
    PYTHON_SCRIPT_PATH = "/example/hello.py"   # tool application

    def __init__(self, configuration=None):
        """
        Init function

        :param configuration: a dictionary containing parameters that define how the operation should be carried out,
        which are specific to <myTool> tool.
        :type configuration: dict
        """
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        # Init variables
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.parent_dir = os.path.abspath(self.current_dir + "/../")
        self.execution_path = os.path.abspath(self.configuration.get('execution', '.'))
        self.arguments = dict(
            [(key, value) for key, value in self.configuration.items() if key not in self.DEFAULT_KEYS]
        )

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the <myTool> tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_files: Dictionary of the output files locations. expected to be generated.
        :type output_files: dict
        :param output_metadata: # TODO
        :type output_metadata: list
        :return: # TODO
        :rtype: dict, dict
        """
        try:
            # Set and validate execution directory. If not exists the directory will be created.
            if not os.path.isdir(self.execution_path):
                os.mkdir(self.execution_path)

            # Set and validate execution parent directory. If not exists the directory will be created.
            execution_parent_dir = os.path.dirname(self.execution_path)
            if not os.path.isdir(execution_parent_dir):
                os.mkdir(execution_parent_dir)

            # Update working directory to execution path
            os.chdir(self.execution_path)

            # Tool Execution
            self.toolExecution(input_files)

            # Create and validate the output file from tool execution
            output_id = output_metadata[0]["name"]
            output_type = output_metadata[0]["file"]["file_type"].lower()
            output_file_path = "{}/{}.{}".format(self.execution_path, output_id, output_type)
            output_files[output_id] = [(output_file_path, "file")]
            # TODO: add more output files to save, if it is necessary for you
            #  or create a method to manage more than one output file

            return output_files, output_metadata

        except:
            errstr = "VRE <myTool> tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def toolExecution(self, input_files):
        """
        The main function to run the <myTool> tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        """
        try:
            # Get input files
            input_file_1 = input_files.get("hello_file")
            # TODO: add more input files to use, if it is necessary for you

            # Get arguments
            argument_1 = self.arguments.get("username")
            # TODO: add more arguments to use, if it is necessary for you

            # Tool execution
            cmd = [
                'python',
                self.parent_dir + self.PYTHON_SCRIPT_PATH,  # hello.py
                input_file_1,   # hello_file
                argument_1,     # username
            ]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # TODO: change command line to run <myApplication>

            # Sending the stdout to the log file
            for line in iter(process.stderr.readline, b''):
                print(line.rstrip().decode("utf-8").replace("", " "))

            rc = process.poll()
            while rc is None:
                rc = process.poll()
                time.sleep(0.1)

            if rc is not None and rc != 0:
                logger.progress("Something went wrong inside the <myApplication> execution. See logs.", status="WARNING")
            else:
                logger.progress("The <myApplication> execution finished successfully.", status="FINISHED")

        except:
            errstr = "The <myApplication> execution failed. See logs."
            logger.error(errstr)
            raise Exception(errstr)
