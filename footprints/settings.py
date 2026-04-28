import os
import json


# uncomment the imports appropriate for the telescope to be analysed

# # Grosser Schmidt-Spiegel datasets
# from import_GS import sequences as sequences
# from import_GS import parameters as parameters
# tel_suffix = "GS"

# # Great Schmidt Camera  datasets
# from import_GSC import sequences as sequences
# from import_GSC import parameters as parameters
# tel_suffix = "GSC"

# Doppel-Reflektor datasets
from import_DR import sequences as sequences
from import_DR import parameters as parameters
tel_suffix = "DR"

# # 1m-Spiegelteleskop datasets
# from import_ST import sequences as sequences
# from import_ST import parameters as parameters
# tel_suffix = "ST"

telescope_names = {
    'GS':  'Grosser Schmidt-Spiegel',       # 0.91 arcsec/px
    'GSC': 'Great Schmidt Camera',          # 1.29
    'ST':  '1m-Spiegelteleskop',
    'DR':  'Doppel-Reflektor',              # 0.73
}

DATAPATH = '/Users/busko/Projects/VASCO_data/footprints'
# DATAPATH = '/Volumes/backup/plateanalysis_data/footprints'

CATALOG = 'footprints_8.csv'
# CATALOG = 'footprints_1958.csv'
RESULTS = "./results/"


# To support pipleine mode, the current data set and sequence names
# are kept in a json file. To run scripts manually, edit this file 
# to point to the desired plate pair (careful with editing, JSON 
# files have finicky syntax). The pipeline overwrites this file.

dataset_json = 'dataset.json'    
try:
    with open(dataset_json, 'r', encoding='utf-8-sig') as json_file:
        dataset_dict = json.load(json_file)
        current_dataset  = dataset_dict['current_dataset']
        current_sequence = dataset_dict['current_sequence']
except FileNotFoundError:
    print(f"Error: File {dataset_json} was not found.")
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    

# Image names are kept in a json file so the download
# code can update it with new image names as soon as
# images are downloaded.
images_json = 'images.json'
try:
    json_file = open(images_json, 'r')
    images = json.load(json_file)
except FileNotFoundError:
    print(f"Error: File {images_json} was not found.")
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")

    
# these functions replace a (much simpler) dict with static parameters,
# and are used for keeping backwards compatibility throughout the code.

def fname(name, datapath=DATAPATH):
    return os.path.join(datapath, name)

def get_table_sources(plate1, calib=False):
    prefix = 'sources_'
    if calib:
        prefix = prefix + 'calib_'
    return prefix + str(plate1) + '.csv'

def get_table_psf_nomatch(plate1, plate2):
    return 'table_psf_nomatch_' + str(plate1) + '_' + str(plate2) + '.fits'

def get_parameters(key):
    par = parameters['default']
    if key in parameters:
        par = par | parameters[key]
    
    plate1 = key.split(',')[0]
    plate2 = key.split(',')[1]

    par['table1'] = get_table_sources(plate1)
    par['table2'] = get_table_sources(plate2)
    par['table1_calib'] = get_table_sources(plate1, calib=True)
    par['table2_calib'] = get_table_sources(plate2, calib=True)
    par['table_matched'] = 'table_match_' + plate1 + '_' + plate2 + '.fits'
    par['table_psf_matched'] = 'table_psf_match_' + plate1 + '_' + plate2 + '.fits'
    par['table_non_matched'] = 'table_nomatch_' + plate1 + '_' + plate2 + '.fits'
    par['table_psf_nonmatched'] = get_table_psf_nomatch(plate1, plate2)
    par['table_candidates'] = 'table_candidates_' + plate1 + '_' + plate2 + '.fits'
    
    par['image1'] = images[plate1]
    par['image2'] = images[plate2]
    
    return par


