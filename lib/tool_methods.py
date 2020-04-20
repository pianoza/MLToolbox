#!/usr/bin/env python

"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import subprocess

from ruamel import yaml
from utils import logger

import tool.VRE_Tool


class Template:
    """
    This is a class for Template workflow module.
    """

    @staticmethod
    def create_input_yml(input_metadata, arguments, filename_path):
        """
        Create a YAML file containing the information of inputs from Template workflow

        :param input_metadata: Matching metadata for each of the files, plus any additional data.
        :type input_metadata: dict
        :param arguments: dict containing tool arguments
        :type arguments: dict
        :param filename_path: Working YAML file path directory
        :type filename_path: str
        """
        try:
            input = {}
            for key, value in input_metadata.items():  # add metadata inputs
                data_type = value[0]
                if data_type == "file":  # mapping
                    data_type = data_type.replace("f", "F")

                file_path = str(value[1].file_path)
                input.update({key: {"class": data_type, "location": file_path}})

            for key, value in arguments.items():  # add arguments
                if key not in tool.VRE_Tool.WF_RUNNER.MASKED_KEYS:
                    input[str(key)] = str(value)

            with open(filename_path, 'w+') as f:
                yaml.dump(input, f, allow_unicode=True, default_flow_style=False)

        except:
            errstr = "The YAML file creation failed. See logs"
            logger.error(errstr)
            raise Exception(errstr)

    @staticmethod
    def execute_tool(wf_input_yml_path, wf_url):
        """
        Template execution process with the workflow specified by wf_url and YAML file path wf_input_yml_path
        specified by wf_input_yml_path, created from config.json and input_metadata.json

        :param wf_input_yml_path: Template workflow in YAML format
        :type wf_input_yml_path: str
        :param wf_url: URL for the location of the workflow
        :type wf_url: str
        """
        logger.debug("Starting tool execution")
        process = subprocess.Popen(["cwltool", wf_url, wf_input_yml_path], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)  # TODO change for your execution tool
        return process
