from configparser import ConfigParser
from ast import literal_eval
import pprint

from matplotlib.pyplot import isinteractive

def get_default_configs():
    defaults_file = './configs_default.ini'
    config = ConfigParser()
    config.read(defaults_file)
    confdict = {section: dict(config.items(section)) for section in config.sections()}
    return confdict

def load_default_configs(file_path):
    configs = {
        'modus': 'binary_classification',
        'coarse': True,
        'experiment_name': 'run000',
        'image_types': 'CT',
        'General': dict(),
        'Preprocessing': dict(),
        'ImageFeatures': dict(),
        'PyRadiomics': dict(),
        'ComBat': dict(),
        'Featsel': dict(),
        'Labels': dict(),
        'Resampling': dict(),
        'Classification': dict(),
        'CrossValidation': dict(),
        'HyperOptimization': dict(),
    }
    parser = ConfigParser()
    parser.read(file_path)
    configs['General']['Segmentix'] = parser.getboolean('General', 'Segmentix')
    configs['General']['tempsave'] = parser.getboolean('General', 'tempsave')
    configs['General']['AssumeSameImageAndMaskMetadata'] = parser.getboolean('General', 'AssumeSameImageAndMaskMetadata')
    configs['General']['ComBat'] = parser.getboolean('General', 'ComBat')
    configs['Preprocessing']['Normalize'] = parser.getboolean('Preprocessing', 'Normalize')
    configs['Preprocessing']['Clipping'] = parser.getboolean('Preprocessing', 'Clipping')
    configs['Preprocessing']['Clipping_Range'] = parser.get('Preprocessing', 'Clipping_Range')
    configs['Preprocessing']['Method'] = parser.get('Preprocessing', 'Method')
    configs['Preprocessing']['Resampling'] = parser.getboolean('Preprocessing', 'Resampling')
    configs['Preprocessing']['Resampling_spacing'] = parser.get('Preprocessing', 'Resampling_spacing')
    configs['Preprocessing']['BiasCorrection'] = parser.getboolean('Preprocessing', 'BiasCorrection')
    configs['ImageFeatures']['histogram'] = parser.getboolean('ImageFeatures', 'histogram')
    configs['ImageFeatures']['orientation'] = parser.getboolean('ImageFeatures', 'orientation')
    configs['ImageFeatures']['texture_Gabor'] = parser.getboolean('ImageFeatures', 'texture_Gabor')
    configs['ImageFeatures']['texture_LBP'] = parser.getboolean('ImageFeatures', 'texture_LBP')
    configs['ImageFeatures']['texture_GLCM'] = parser.getboolean('ImageFeatures', 'texture_GLCM')
    configs['ImageFeatures']['texture_GLCMMS'] = parser.getboolean('ImageFeatures', 'texture_GLCMMS')
    configs['ImageFeatures']['vessel'] = parser.getboolean('ImageFeatures', 'vessel')
    configs['ImageFeatures']['log'] = parser.getboolean('ImageFeatures', 'log')
    configs['ImageFeatures']['phase'] = parser.getboolean('ImageFeatures', 'phase')
    configs['PyRadiomics']['extract_shape'] = parser.getboolean('PyRadiomics', 'extract_shape')
    configs['PyRadiomics']['texture_GLRLM'] = parser.getboolean('PyRadiomics', 'texture_GLRLM')
    configs['PyRadiomics']['texture_GLSZM'] = parser.getboolean('PyRadiomics', 'texture_GLSZM')
    configs['PyRadiomics']['texture_GLDM'] = parser.getboolean('PyRadiomics', 'texture_GLDM')
    configs['PyRadiomics']['texture_NGTDM'] = parser.getboolean('PyRadiomics', 'texture_NGTDM')
    configs['ComBat']['batch'] = parser.get('ComBat', 'batch')
    configs['Featsel']['Variance'] = parser.getfloat('Featsel', 'Variance')
    configs['Featsel']['SelectFromModel'] = parser.getfloat('Featsel', 'SelectFromModel')
    configs['Featsel']['UsePCA'] = parser.getfloat('Featsel', 'UsePCA')
    configs['Featsel']['StatisticalTestUse'] = parser.getfloat('Featsel', 'StatisticalTestUse')
    configs['Featsel']['ReliefUse'] = parser.getfloat('Featsel', 'ReliefUse')
    configs['Labels']['label_names'] = parser.get('Labels', 'label_names')
    configs['Resampling']['Use'] = parser.getfloat('Resampling', 'Use')
    configs['Classification']['classifiers'] = parser.get('Classification', 'classifiers')
    configs['CrossValidation']['Type'] = parser.get('CrossValidation', 'Type')
    configs['CrossValidation']['N_iterations'] = parser.getint('CrossValidation', 'N_iterations')
    configs['CrossValidation']['test_size'] = parser.getfloat('CrossValidation', 'test_size')
    configs['CrossValidation']['fixed_seed'] = parser.getboolean('CrossValidation', 'fixed_seed')
    configs['HyperOptimization']['test_size'] = parser.getfloat('HyperOptimization', 'test_size')
    configs['HyperOptimization']['n_splits'] = parser.getint('HyperOptimization', 'n_splits')
    configs['HyperOptimization']['N_iterations'] = parser.getint('HyperOptimization', 'N_iterations')
    configs['HyperOptimization']['n_jobspercore'] = parser.getint('HyperOptimization', 'n_jobspercore')

    return configs

def get_typed_val(val):
    # vall is always a string, assign it to bool, tuple, or number
    try: # this takes care of single numbers
        return literal_eval(val)
    except:
        if val == 'on': return True
        else:
            return val

def parse_user_arguments(arguments):
    # remove unwanted fields
    arguments.pop('execution')
    arguments.pop('project')
    arguments.pop('description')
    # iterate over the rest and parse
    configs = {
        'modus': '',
        'coarse': False,
        'experiment_name': 'run000',
        'image_types': 'CT',
        'General': dict(),
        'Preprocessing': dict(),
        'ImageFeatures': dict(),
        'PyRadiomics': dict(),
        'ComBat': dict(),
        'Featsel': dict(),
        'Labels': dict(),
        'Resampling': dict(),
        'Classification': dict(),
        'CrossValidation': dict(),
        'HyperOptimization': dict(),
    }
    classifiers = ''
    comma = ''
    for key, val in arguments.items():
        levels = key.split(':')
        section, item = levels[1], levels[2]
        if section == 'classifiers':
            classifiers = classifiers + comma + item
            comma = ', '
        elif section == 'ML':
            configs['modus'] = val
        else:
            typed_val = get_typed_val(val)
            if isinstance(typed_val, tuple):  # we don't want to change '1, 1, 1' to (1, 1, 1)
                typed_val = val
            configs[section][item] = typed_val
    configs['Classification']['classifiers'] = classifiers
    configs['image_types'] = configs['General']['Imagetype']
    configs['General'].pop('Imagetype')
    return configs

def update_overrides(configs, user_configs):
    '''We can't use dict.update()
    iterate over configs
        if the field exists in user_configs
            update it
        else
            set that field in config to false
    '''
    new_configs = configs
    for section, items in configs.items():
        if isinstance(items, dict):
            for field, val in items.items():
                if field in user_configs[section]:
                    new_configs[section][field] = user_configs[section][field]
                else:
                    if isinstance(val, bool):
                        new_configs[section][field] = False
                    else:
                        new_configs[section][field] = ''
        else:
            new_configs[section] = user_configs[section]
    return new_configs

# ARGUMENTS
vre_args = {
    'execution': '/gpfs/eucanimage.eu/vre/userdata//ECIUSER6059f84f499c8/__PROJ62f62b15eb48c3.57139216/run029',
    'project': '/gpfs/eucanimage.eu/vre/userdata//ECIUSER6059f84f499c8/__PROJ62f62b15eb48c3.57139216/run029',
    'description': None,
    'General:General:Segmentix': 'on',
    'General:General:tempsave': 'on', 
    'General:General:AssumeSameImageAndMaskMetadata': 'on', 
    'General:General:ComBat': 'on', 
    'General:General:Imagetype': 'MRI', 
    'image:Preprocessing:Normalize': 'on', 
    'image:Preprocessing:Method': 'minmed', 
    'image:Preprocessing:Clipping': 'on', 
    'image:Preprocessing:Clipping_Range': '-1000.0, 3001.0', 
    'image:Preprocessing:Resampling': 'on', 
    'image:Preprocessing:Resampling_spacing': '1, 1, 1', 
    'image:Preprocessing:BiasCorrection': 'on', 
    'radiomics:ImageFeatures:histogram': 'on', 
    'radiomics:ImageFeatures:orientation': 'on', 
    'radiomics:ImageFeatures:texture_Gabor': 'on', 
    'radiomics:ImageFeatures:texture_LBP': 'on', 
    'radiomics:ImageFeatures:texture_GLCM': 'on', 
    'radiomics:ImageFeatures:texture_GLCMMS': 'on', 
    'radiomics:ImageFeatures:vessel': 'on', 
    'radiomics:ImageFeatures:log': 'on', 
    'radiomics:ImageFeatures:phase': 'on', 
    'radiomics:PyRadiomics:extract_shape': 'on', 
    'radiomics:PyRadiomics:texture_GLRLM': 'on', 
    'radiomics:PyRadiomics:texture_GLSZM': 'on', 
    'radiomics:PyRadiomics:texture_GLDM': 'on', 
    'radiomics:PyRadiomics:texture_NGTDM': 'on', 
    'selection:ComBat:batch': 'Hospital', 
    'selection:Featsel:Variance': '1.0', 
    'selection:Featsel:SelectFromModel': '0.275', 
    'selection:Featsel:UsePCA': '0.275', 
    'selection:Featsel:StatisticalTestUse': '0.275', 
    'selection:Featsel:ReliefUse': '0.275', 
    'arguments_ML:ML:mode': 'multiclass_classification', 
    'ML:Labels:label_names': 'imaginary_label_1, imaginary_label_2', 
    'ML:Resampling:Use': '0.2', 
    'classifiers:classifiers:SVM': 'on', 
    'classifiers:classifiers:RF': 'on', 
    'classifiers:classifiers:LR': 'on', 
    'classifiers:classifiers:LDA': 'on', 
    'classifiers:classifiers:QDA': 'on', 
    'classifiers:classifiers:GaussianNB': 'on', 
    'classifiers:classifiers:AdaBoostClassifier': 'on', 
    'classifiers:classifiers:XGBClassifier': 'on', 
    'CrossValidation:CrossValidation:test_size': '0.2', 
    'CrossValidation:CrossValidation:N_iterations': '10', 
    'CrossValidation:CrossValidation:Type': 'LOO', 
    'CrossValidation:CrossValidation:fixed_seed': 'on', 
    'HyperOptimization:HyperOptimization:test_size': '0.2', 
    'HyperOptimization:HyperOptimization:n_splits': '4', 
    'HyperOptimization:HyperOptimization:N_iterations': '1000', 
    'HyperOptimization:HyperOptimization:n_jobspercore': '500'
}

if __name__ == '__main__':
    # configs = load_default_configs('./configs_default.ini')
    configs = load_default_configs('/home/kaisar/EuCanImage/Coding/VRE/MLToolbox/tool/configs_default.ini')
    new_configs = parse_user_arguments(vre_args)
    pp = pprint.PrettyPrinter(4)
    print('Default configs')
    pp.pprint(configs)
    print('User configs')
    pp.pprint(new_configs)
    # configs.update(new_configs)
    overrides = update_overrides(configs, new_configs)
    print('Overrides')
    pp.pprint(configs)


# vre_args = {
#     'execution': '/gpfs/eucanimage.eu/vre/userdata//ECIUSER6059f84f499c8/__PROJ62f62b15eb48c3.57139216/run028',
#     'project': '/gpfs/eucanimage.eu/vre/userdata//ECIUSER6059f84f499c8/__PROJ62f62b15eb48c3.57139216/run028',
#     'description': None,
#     'General:General:Segmentix': 'on', 
#     'General:General:tempsave': 'on', 
#     'General:General:AssumeSameImageAndMaskMetadata': 'on',
#     'General:General:ComBat': 'on', 
#     'General:General:Imagetype': 'CT', 
#     'image:Preprocessing:Normalize': 'on', 
#     'image:Preprocessing:Method': 'z_score', 
#     'image:Preprocessing:Clipping': 'on', 
#     'image:Preprocessing:Clipping_Range': '-1000.0, 3000.0', 
#     'image:Preprocessing:Resampling': 'on', 
#     'image:Preprocessing:Resampling_spacing': '1, 1, 1', 
#     'image:Preprocessing:BiasCorrection': 'on', 
#     'radiomics:ImageFeatures:histogram': 'on', 
#     'radiomics:ImageFeatures:orientation': 'on', 
#     'radiomics:ImageFeatures:texture_Gabor': 'on', 
#     'radiomics:ImageFeatures:Orientation': 'on', 
#     'radiomics:ImageFeatures:texture_GLCM': 'on', 
#     'radiomics:ImageFeatures:texture_GLCMMS': 'on', 
#     'radiomics:ImageFeatures:vessel': 'on', 
#     'radiomics:ImageFeatures:log': 'on', 
#     'radiomics:ImageFeatures:phase': 'on', 
#     'radiomics:PyRadiomics:extract_shape': 'on', 
#     'radiomics:PyRadiomics:texture_GLRLM': 'on', 
#     'radiomics:PyRadiomics:texture_GLSZM': 'on', 
#     'radiomics:PyRadiomics:texture_GLDM': 'on', 
#     'radiomics:PyRadiomics:texture_NGTDM': 'on', 
#     'selection:ComBat:batch': 'Hospital', 
#     'selection:Featsel:Variance': '1.0', 
#     'selection:Featsel:SelectFromModel': '0.275', 
#     'selection:Featsel:UsePCA': '0.275', 
#     'selection:Featsel:StatisticalTestUse': '0.275', 
#     'selection:Featsel:ReliefUse': '0.275', 
#     'arguments_ML:ML:ML:mode': 'binary_classification', 
#     'ML:Labels:label_names': 'imaginary_label_1', 
#     'ML:Resampling:Use': '0.2', 
#     'classifiers:classifiers:SVM': 'on', 
#     'classifiers:classifiers:RF': 'on', 
#     'classifiers:classifiers:LR': 'on', 
#     'classifiers:classifiers:LDA': 'on', 
#     'classifiers:classifiers:QDA': 'on', 
#     'classifiers:classifiers:GaussianNB': 'on', 
#     'classifiers:classifiers:AdaBoostClassifier': 'on', 
#     'classifiers:classifiers:XGBClassifier': 'on', 
#     'CrossValidation:CrossValidation:test_size': '0.2', 
#     'CrossValidation:CrossValidation:N_iterations': '10', 
#     'CrossValidation:CrossValidation:Type': 'random_split', 
#     'CrossValidation:CrossValidation:fixed_seed': 'on', 
#     'HyperOptimization:HyperOptimization:test_size': '0.2', 
#     'HyperOptimization:HyperOptimization:n_splits': '5', 
#     'HyperOptimization:HyperOptimization:N_iterations': '1000', 
#     'HyperOptimization:HyperOptimization:n_jobspercore': '500'
#     }