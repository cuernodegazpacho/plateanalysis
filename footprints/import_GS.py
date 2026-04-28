# Import file for parameters and sequences of plates for telescope Grosser Schmidt-Spiegel.


# Parameters that may require fine tuning, specific to each dataset.
# The defaults are appropriate for the Grosser Schmidt-Spiegel datasets. 

parameters = {
    'default': {
        'nproc': 8,                                # number of performance processors (Mac M1 16Gb) - average tasks
        'nproc_analysis': 4,                       # number of performance processors (Mac M1 16Gb) - heavy tasks
        # sextractor and catalog criteria
        'use_catalog': True,                      # use Gaia IDs for filtering
        'sextractor_flags': 4,
        'model_prediction': 0.6,
        'elongation': 1.15,                        # less than
        'annular_bin': 8,                          # less or equals
        'flag_rim': 0,
        'max_flux_threshold': 0.1,
        # analysis
        'fwhm_init': 8.,
        'fit_shape': 31,
        'min_acceptable_flux': 500,
        'min_fwhm':  3.,
        'max_fwhm': 15.,
        'qfit_max': 2.5,
        'cfit_max': 0.003,
        'max_fit_flag': 0,
        'neighborhood_cutout_size': 8.0,          # full side of square, arcmin
        'elongation_limit': 1.10,
        'profile_diff_threshold': 0.05,           # 0.04 good, checked with false positives
        'circularity_threshold': [70],            # about 28% on a 0-255 scale
        'circularity_low_limit': 0.80, 
        'tiny_cutout_size': 21,                   # for cicularity computation (px)
        'false_positive_threshold': 10.,          # checked with false positives
        # display
        'fwhm_lim': 20., 
        'disp_elong_lim': 1.2,
        'display_cutout_size': 2.5,                # full side of square, arcmin
        'plot_limit': 100,
        'rotate': [False,False],                  # rotate *before* flipping - NOT IMPLEMENTED YET
        'invert_east':  [False,False],
        'invert_north': [False,False],
    },
    '8739,8741': {
        'annular_bin': 4,
    },
    '9341,9342': {
        'nproc_analysis': 6,
        'max_flux_threshold': 0.03,
        'annular_bin': 5,
    },
    '9342,9343': {
        'nproc_analysis': 6,
        'max_flux_threshold': 0.03,
        'annular_bin': 5,
    },
    '9474,9475': {
        'nproc_analysis': 4,
        'min_fwhm':  5.,
        'max_fwhm': 10.,
        'annular_bin': 5,
    },
    '9039,9040': {
        'rotate': [False,True],            # 2nd plate has to be reprojected for display
    },
    '9039,9012': {
        'neighborhood_cutout_size': 15.0,  
    },
    '9012,9013': {
        'neighborhood_cutout_size': 15.0,  
    },
    '9013,9014': {
        'neighborhood_cutout_size': 15.0,  
        'display_cutout_size': 2.5,  
    },
    '9089,9112': {
        'annular_bin': 6,
        'neighborhood_cutout_size': 18.0,  
    },
    '9112,9099': {
        'annular_bin': 6,
        'neighborhood_cutout_size': 45.0,
    },
    '9095,9096': {
        'annular_bin': 7,                  # 9096 looks underexposed
        'neighborhood_cutout_size': 15.0, 
    },
    '9099,9100': {
        'annular_bin': 7,                 
        'neighborhood_cutout_size': 15.0, 
    },
    '9337,9338': {
        'annular_bin': 6,                  # focus
        'neighborhood_cutout_size': 15.0, 
    },
    '9352,9353': {
        'annular_bin': 6,                  # focus
        'neighborhood_cutout_size': 15.0, 
    },
    '9355,9356': {                         # 9356 partially blocked by shutter
        'annular_bin': 6,                  # focus
        'neighborhood_cutout_size': 15.0, 
    },
    '9307,9311': {                         # guiding
        'elongation': 1.25,
        'elongation_limit': 1.15,
    },
    '9311,9312': {                         # guiding
        'elongation': 1.25,
        'elongation_limit': 1.15,
    },
    '9312,9282': {                         # guiding
        'elongation': 1.25,
        'elongation_limit': 1.15,
    },
    '9282,9285': {                         # guiding
        'elongation': 1.25,
        'elongation_limit': 1.15,
    },
    '8820,8847': {                         # guiding
        'elongation': 1.25,
        'elongation_limit': 1.15,
        'neighborhood_cutout_size': 30.0, 
    },
    '8840,8845': {
        'neighborhood_cutout_size': 15.0,  
    },
    '9011,9043': {
        'neighborhood_cutout_size': 15.0,  
        'display_cutout_size': 2.0,
    },
    '9381,9388': {
        'neighborhood_cutout_size': 20.0,  
    },
}


# Plate IDs in interesting sequences of images. This dict was built 
# by script footprint_analysis.ipynb (it has to be manually copied and
# pasted from the output of that script, in here). 
# 
# This dict includes sequences of two or more plates taken on the same 
# night, and overlapping more than 50% in area.

sequences = {
#     'seq00': [8794, 8795, 8796],                                # out-of-focus (but good for testing)
    'seq01': [9245, 9246, 9247],
    'seq03': [9313, 9315, 9317, 9318, 9319, 9320],      
    'seq04': [9322, 9323, 9324, 9325, 9326, 9327, 9328],
    'seq05': [9344, 9345, 9346, 9347, 9348, 9349, 9350],
    'seq06': [9341, 9342, 9343],
    'seq07': [9473, 9474, 9475],
#     'seq08': [9521, 9522, 9523],                                # comet - trailed
    'seq09': [9533, 9534, 9535],
    'seq10': [9538, 9539, 9540],
    'seq11': [9545, 9546, 9547],
    'seq12': [9550, 9551, 9552],
# two-plate sequences that overlap by more than 50% in area.
    'seq13': [8874, 8875],
#     'seq14': [9039, 9040],    # 9040 is Y only, rotated AND flipped
    'seq15': [9012, 9013],
    'seq16': [9016, 9017],
    'seq17': [9095, 9096],
    'seq18': [9099, 9100],
#     'seq18a': [9100, 9099],          # lots of super-bright objects in 9100 - artifacts mostly
#     'seq19': [9167, 9168, 9169],   # out-of-order
    'seq20': [9168, 9169],
    'seq21': [9174, 9175],
    'seq22': [9176, 9177],
    'seq23': [9228, 9229],
    'seq24': [9233, 9234],
    'seq25': [9305, 9306],
    'seq26': [9285, 9286],
    'seq27': [9337, 9338],
    'seq28': [9352, 9353],
    'seq29': [9355, 9356],
#     'seq30': [9469, 9472],    # comet Arend-Roland   Ha + GG5
#     'seq31': [9482, 9484],    # comet Arend-Roland   Kodak OaO
#     'seq32': [9488, 9489, 9490, 9491],     # comet Arend-Roland   Kodak OaO
#     'seq33': [9525, 9526],     # comet Arend-Roland partial tail
    'seq34': [9528, 9529],
#     'seq35': [9536, 9537],   # comet Arend-Roland   Kodak OaO
#     'seq36': [9543, 9544],   # comet Arend-Roland   Kodak OaO
    'seq37': [9548, 9549],
    'seq38': [9555, 9556],
    'seq39': [9557, 9558],     # coordinates a bit off?
#     'seq40': [9596, 9597],     # comet Mrkos Ha+GG5, OaO (?)
# }
# #
# #
# #
# This dict below is also for telescope Grosser Schmidt-Spiegel. It includes
# two or more plates taken on separate nights, with up to 10 nights difference
# between dates. Plate areas overlapping by more than 50%.
#        
#
# sequences = {
#     'seq41': [9012, 9013, 9014, 9039, 9040],  # 9040 is Y only; 9012-9013 already done; 9039 is first
#     'seq41': [9039, 9012, 9013, 9014],        # 2nd attempt - 9014 underexposed - contamination with weak stars
    'seq42': [9089, 9112, 9099],                # March 28 - Apr 07, 1956
    'seq43': [9307, 9311, 9312, 9282, 9285, 9286],
#     'seq44': [9313, 9315, 9317, 9318, 9319, 9320, 9316, 9322, 9323, 9324, 9325, 9327, 9321], # repeat from seqs 03 and 04
#     'seq45': [9316, 9322, 9323, 9324, 9325, 9327, 9321],                                     # ditto
#     'seq46': [9322, 9323, 9324, 9325, 9321],                                                 # ditto
#     'seq47': [9352, 9353, 9355, 9356],                                                       # seq28 + seq29
#     'seq48': [9486, 9488, 9489, 9493],                                                       # comet 
#     'seq49': [9488, 9489, 9490, 9491, 9492, 9493],                                           # comet
#     'seq50': [9525, 9526, 9531, 9536, 9537, 9543, 9544],                                     # comet
#     'seq51': [9528, 9529, 9553, 9555, 9556],                   # partial with seq 34 and 38
#     'seq51': [9529, 9553, 9555],                               # non-overlapping FOVs: 60+ stars out of frame
#     'seq52': [9531, 9536, 9537, 9543, 9544],                   # comet
#     'seq53': [9533, 9534, 9535, 9545, 9546, 9547],             # seq09 + seq11
#     'seq54': [9536, 9537, 9543, 9544],                         # comet
#     'seq55': [9542, 9548, 9549, 9557, 9558],                   # seq37 + seq39
    'seq55': [9542, 9548],                                       # removed seq37 + seq39
#     'seq56': [9545, 9546, 9547, 9550, 9551, 9552],             # seq11 + seq12
#     'seq57': [9548, 9549, 9557, 9558],                         # seq37 + seq39
# #     # two-plate sequences
#     'seq58': [8739, 8741],                      # Earth shadow 8 deg - plates are too dirty
    'seq59': [8820, 8847],
    'seq60': [8840, 8845],
#     'seq61': [8886, 8893],                      # 8886 has no WCS
#     'seq62': [8910, 8915],                      # 8910 IR emulsion, 8915 blue emulsion, 8915 bad WCS - false positives
    'seq63': [9010, 9042],
    'seq64': [9011, 9043],
#     'seq65': [9012, 9013, 9014],                # partial repeat with seq15 - seq41 9014 underexposed
#     'seq66': [9112, 9099, 9100],                # repeat with seq42
    'seq67': [9182, 9188],
    'seq68': [9185, 9187],
    'seq69': [9248, 9249],
    'seq70': [9381, 9388],
    'seq71': [9388, 9404],
#     'seq72': [9480, 9482, 9484],                # comet
#     'seq73': [9482, 9484, 9485],                # comet
#     'seq74': [9553, 9555, 9556],                # comet Mrkos 
}





