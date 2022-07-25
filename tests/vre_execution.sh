#!/bin/bash

###
### Testing in a local installation
### the VRE server CMD
###
### * Automatically created by VRE *
###


# Local installation - EDIT IF REQUIRED
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TEST_DATA_DIR=$CWD
WORKING_DIR=$TEST_DATA_DIR/run000
TOOL_EXECUTABLE=$TEST_DATA_DIR/../VRE_RUNNER

# Running segmentation tool

if [ -d  $WORKING_DIR ]; then rm -r $WORKING_DIR/; mkdir -p $WORKING_DIR; else mkdir -p $WORKING_DIR; fi
cd $WORKING_DIR

echo "--- Test execution: $WORKING_DIR"
echo "--- Start time: `date`"
echo $TOOL_EXECUTABLE --config $TEST_DATA_DIR/config.json --in_metadata $TEST_DATA_DIR/in_metadata.json --out_metadata $TEST_DATA_DIR/out_metadata_sample.json  --log_file $WORKING_DIR/tool.log

# time $TOOL_EXECUTABLE --config $TEST_DATA_DIR/config.json --in_metadata $TEST_DATA_DIR/in_metadata.json --out_metadata $TEST_DATA_DIR/out_metadata_sample.json  --log_file $WORKING_DIR/tool.log
