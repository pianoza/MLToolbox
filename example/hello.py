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
import sys

"""
Example tool application that performs:
    - Open the file hello.txt
    - Replace string username of hello.txt with input string
    - Add and save new content to file goodbye.txt
"""

input_file = open(sys.argv[1], "r")
data = input_file.read().replace("username", sys.argv[2])
output_file = open("goodbye.txt", "w")
output_file.write(data + "\nGoodbye, " + sys.argv[2] + ".")
