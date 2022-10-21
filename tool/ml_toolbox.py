# Welcome to the tutorial of WORC: a Workflow for Optimal Radiomics
# Classification! It will provide you with basis knowledge and practical
# skills on how to run the WORC. For advanced topics and WORCflows, please see
# the other notebooks provided with this tutorial. For installation details,
# see the ReadMe.md provided with this tutorial.

# This tutorial interacts with WORC through SimpleWORC and is especially
# suitable for first time usage.

# import neccesary packages
import os
import shutil
from WORC import BasicWORC
from pathlib import Path
from load_vre_configs import load_default_configs, parse_user_arguments, update_overrides
# These packages are only used in analysing the results
import pandas as pd
import json
import fastr
import glob

# TODO: remove these inputs, should be provided by the user
# overridestest = {'modus': 'binary_classification', 'coarse': True, 'experiment_name': 'run000', 'image_types': 'CT', 'Labels': {'label_names': 'imaginary_label_1'}}
# overridestest = {'modus': 'binary_classification', 'coarse': False, 'experiment_name': 'run000', 'image_types': 'CT', 'Labels': {'label_names': 'imaginary_label_1'}}

# DONE image_types: drop-down menu with the following options:
# quantitative_modalities = ['CT', 'PET', 'Thermography', 'ADC', 'MG']
# qualitative_modalities = ['MRI', 'MR', 'DWI', 'US']

def run_ml_toolbox(overrides, images, segmentations, label_file, out_dir, arguments):
    """Execute WORC Tutorial experiment."""
    print(f"Running in folder: {out_dir}.")
    print("ARGUMENTS\n", arguments)
    user_arguments = parse_user_arguments(arguments)
    overrides = load_default_configs('./configs_default.ini')
    overrides = update_overrides(user_arguments)
    print('Parsed arguments', overrides)
    # ---------------------------------------------------------------------------
    # Input
    # ---------------------------------------------------------------------------
    # The minimal inputs to WORC are:
    #   - Images
    #   - Segmentations
    #   - Labels
    #
    # In SimpleWORC, we assume you have a folder "datadir", in which there is a
    # folder for each patient, where in each folder there is a image.nii.gz and a mask.nii.gz:
    #           Datadir
    #               Patient_001
    #                   image.nii.gz
    #                   mask.nii.gz
    #               Patient_002
    #                   image.nii.gz
    #                   mask.nii.gz
    #               ...
    #
    #
    # You can skip this part if you use your own data.
    # In the example, We will use open source data from the online XNAT platform
    # at https://xnat.bmia.nl/data/archive/projects/stwstrategyhn1. This dataset
    # consists of CT scans of patients with Head and Neck tumors. We will download
    # a subset of 20 patients in this folder. You can change this settings if you
    # like

    # Name of the label you want to predict
    modus = overrides['modus']
    overrides.pop('modus')
    # label_names = ['imaginary_label_1']  # they're going to be named as label1, label2, ... and it's mandatory
    # TODO auto label_name for binary or multiclass

    # Determine whether we want to do a coarse quick experiment, or a full lengthy
    # one. Again, change this accordingly if you use your own data.
    coarse = overrides['coarse']  # Note: KEEP COARSE ONLY FOR DEBUGGING
    overrides.pop('coarse')

    # Give your experiment a name
    experiment_name = overrides['experiment_name']
    overrides.pop('experiment_name')

    # Instead of the default tempdir, let's put the temporary output in a subfolder
    # in the same folder as this script
    tmpdir = os.path.join(out_dir, 'tmp')
    print(f"Temporary folder: {tmpdir}.")

    # ---------------------------------------------------------------------------
    # The actual experiment
    # ---------------------------------------------------------------------------

    # Create a Simple WORC object
    experiment = BasicWORC(experiment_name)
    # print([{Path(im).name.split("_")[0]: im for im in images}])
    # print([{Path(seg).name.split("_")[0]: seg for seg in segmentations}])
    # Set the input data according to the variables we defined earlier
    experiment.images_train = [{Path(im).name.split("_")[0]: im for im in images}]
    experiment.segmentations_train = [{Path(seg).name.split("_")[0]: seg for seg in segmentations}]
    experiment.labels_file_train = label_file
    # experiment.labels_name_train = overrides['label_names']  # list
    # # Tried both, setting label_names of the experiment like this:
    # experiment.label_names = overrides['label_names']
    # # And also like this:
    # experiment.predict_labels(['imaginary_label_1'])  # Also tried ['imaginary_label1'] and 'imaginary_label1'
    experiment.predict_labels(overrides['Labels']['label_names'])  # Also tried ['imaginary_label1'] and 'imaginary_label1'
    # overrides.pop('label_names')
    # experiment.segmentations_from_this_directory(segmentations,
                                                #  segmentation_file_name=segmentation_file_name)
    # experiment.labels_from_this_file(label_file)
    # experiment.predict_labels(label_name)

    # Set the types of images WORC has to process. Used in fingerprinting
    # Valid quantitative types are ['CT', 'PET', 'Thermography', 'ADC']
    # Valid qualitative types are ['MRI', 'DWI', 'US']
    image_types = [overrides['image_types']]  # list
    overrides.pop('image_types')
    experiment.set_image_types(image_types)

    # Use the standard workflow for your specific modus
    if modus == 'binary_classification':
        experiment.binary_classification(coarse=coarse)
    # elif modus == 'regression':  # TODO remove it for this version because not all of the classifiers are regressors
    #     experiment.regression(coarse=coarse)
    elif modus == 'multiclass_classification':
        experiment.multiclass_classification(coarse=coarse)

    # overrides = {
    #         'Labels': {
    #             'modus': 'multilabel',
    #         },
    #         'Featsel': {
    #             # Other estimators do not support multiclass
    #             'SelectFromModel_estimator': 'RF'
    #         }
    #         'Classification': {
                    # 'classifiers': 'SVM, RF, LR, LDA, QDA, GaussianNB, AdaBoostClassifier, XGBClassifier'
    #           }
    #     }
    print('ADDING CONFIG OVERRIDES')
    print(overrides)
    experiment.add_config_overrides(overrides)

    # Set the temporary directory
    experiment.set_tmpdir(tmpdir)

    # TODO add an option in UI to run evaluations
    # experiment.add_evaluation()

    experiment.set_multicore_execution()
    # Run the experiment!
    experiment.execute()

    # NOTE:  Precomputed features can be used instead of images and masks
    # by instead using ``experiment.features_from_this_directory(featuresdatadir)`` in a similar fashion.

    # ---------------------------------------------------------------------------
    # Analysis of results
    # ---------------------------------------------------------------------------

    # There are two main outputs: the features for each patient/object, and the overall
    # performance. These are stored as .hdf5 and .json files, respectively. By
    # default, they are saved in the so-called "fastr output mount", in a subfolder
    # named after your experiment name.

    # Locate output folder
    outputfolder = out_dir + '/outputs/' + experiment_name
    zip_file = out_dir + '/results'
    # outputfolder = out_dir + '/outputs/results'
    # zip the folder in outputfloder
    shutil.make_archive(zip_file, 'zip', os.path.split(outputfolder)[0])
    outfile = zip_file + '.zip'
    print(f"Your output is stored in {outfile}.")

    metadata = {
        'file_format': 'zip',
        'output_path': outfile,
    }
    outputs = [(outfile, metadata)]
    return outputs

    # NOTE: the performance is probably horrible, which is expected as we ran
    # the experiment on coarse settings. These settings are recommended to only
    # use for testing: see also below.

    # ---------------------------------------------------------------------------
    # Tips and Tricks
    # ---------------------------------------------------------------------------

    # For tips and tricks on running a full experiment instead of this simple
    # example, adding more evaluation options, debugging a crashed network etcetera,
    # please go to https://worc.readthedocs.io/en/latest/static/user_manual.html.
    # We advice you to look at the docstrings of the SimpleWORC functions
    # introduced in this tutorial, and explore the other SimpleWORC functions,
    # as SimpleWORC offers much more functionality than presented here.

    # Some things we would advice to always do:
    #   - Run actual experiments on the full settings (coarse=False):
    #       coarse = False
    #       experiment.binary_classification(coarse=coarse)
    #   Note: this will result in more computation time. We therefore recommmend
    #   to run this script on either a cluster or high performance PC. If so,
    #   you may change the execution to use multiple cores to speed up computation
    #   just before before experiment.execute():
    #       experiment.set_multicore_execution()
    #
    #   - Add extensive evaluation: experiment.add_evaluation() before experiment.execute():
    #       experiment.add_evaluation()


if __name__ == '__main__':
    run_ml_toolbox()
