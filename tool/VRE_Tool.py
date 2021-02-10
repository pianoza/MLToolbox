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
import time

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool
from utils import logger


class myTool(Tool):
    """
    Class to define a Tool
    """
    MASKED_KEYS = {'execution', 'project', 'description'}   # default keys of arguments from config.json

    def __init__(self, configuration=None):
        """
        Init function
        """
        logger.debug("Set up {}".format(Tool.__name__))
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        # Arrays are serialized
        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        self.populable_outputs = {}

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the compute_metrics tool.

        :param input_files: List of input files - In this case there are no input files required.
        :type input_files: dict
        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param output_files: List of the output files that are to be generated.
        :type output_files: dict
        :param output_metadata: List of matching metadata for the output files
        :type output_metadata: list
        :return: List of files with a single entry (output_files), List of matching metadata for the returned files
        (output_metadata).
        :rtype: dict, dict
        """
        try:
            # Set and validate execution directory. If not exists the directory will be created.
            execution_path = os.path.abspath(self.configuration.get('execution', '.'))
            if not os.path.isdir(execution_path):
                os.makedirs(execution_path)

            execution_parent_dir = os.path.dirname(execution_path)

            if not os.path.isdir(execution_parent_dir):
                os.makedirs(execution_parent_dir)

            # Update working directory to execution path
            os.chdir(execution_path)
            logger.debug("Execution path: {}".format(execution_path))

            logger.debug("Init execution of the Template Workflow")
            self.execute_workflow(input_metadata, self.configuration, execution_path)

            # Save and validate the output files list
            for key in output_files.keys():
                if output_files[key] is not None:
                    pop_output_path = os.path.abspath(output_files[key])
                    self.populable_outputs[key] = pop_output_path
                    output_files[key] = pop_output_path
                else:
                    errstr = "The output_file[{}] can not be located. Please specify its expected path.".format(key)
                    logger.error(errstr)
                    raise Exception(errstr)

            # Create output metadata
            output_metadata = self.create_output_metadata(input_metadata, output_metadata)

            return output_files, output_metadata

        except:
            errstr = "VRE Template RUNNER pipeline failed. See logs"
            logger.fatal(errstr)
            raise Exception(errstr)

    def execute_workflow(self, input_metadata, arguments, working_directory):  # pylint: disable=no-self-use
        """
        The main function to run the remote Template workflow

        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param arguments: dict containing tool arguments
        :type arguments: dict
        :param working_directory: Execution working path directory
        :type working_directory: str
        """
        try:
            logger.debug("Getting the Template workflow file")
            wf_url = self.configuration.get('wf_url')

            if wf_url is None:
                errstr = "wf_url parameter must be defined"
                logger.fatal(errstr)
                raise Exception(errstr)

            logger.debug("Adding parameters which are not input or output files are in the configuration")
            variable_params = []
            for conf_key in self.configuration.keys():
                if conf_key not in self.MASKED_KEYS:
                    variable_params.append((conf_key, self.configuration[conf_key]))

            logger.info("3) Pack information to YAML")
            wf_input_yml_path = working_directory + "/inputs.yml"
            Template.create_input_yml(input_metadata, arguments, wf_input_yml_path)

            # Template execution
            process = Template.execute_tool(wf_input_yml_path, wf_url)

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
                logger.progress("tool execution finished successfully", status="FINISHED")

        except:
            errstr = "The Template execution failed. See logs"
            logger.error(errstr)
            raise Exception(errstr)

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
