# Import file for parameters and sequences of plates for telescope great Schmidt Camera.


# Parameters that may require fine tuning, specific to each dataset.
# The defaults are appropriate for the Grosser Schmidt-Spiegel datasets. 

# scan resolution: 1.29 arcsec / pix

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
        'neighborhood_cutout_size': 12.0,          # full side of square, arcmin
        'elongation_limit': 1.10,
        'profile_diff_threshold': 0.05,           # 0.04 good, checked with false positives
        'circularity_threshold': [70],            # about 28% on a 0-255 scale
        'circularity_low_limit': 0.80, 
        'tiny_cutout_size': 21,                   # for cicularity computation (px)
        'false_positive_threshold': 10.,          # checked with false positives
        # display
        'fwhm_lim': 20., 
        'disp_elong_lim': 1.2,
        'display_cutout_size': 3.0,                # full side of square, arcmin
        'plot_limit': 100,
        'rotate': [False,False],                  # rotate *before* flipping - NOT IMPLEMENTED YET
        'invert_east':  [False,False],
        'invert_north': [False,False],
    },
    '8739,8741': {
        'annular_bin': 4,
    },
}


# Plate IDs in interesting sequences of images. This dict was built 
# by script footprint_analysis.ipynb (it has to be manually copied and
# pasted from the output of that script, in here). 

sequences = {
    # same night
    'seq01': [66586, 66587, 66588],    # 1953 Sep 5
    'seq02': [66600, 66601],           # 1953 Sep 13
    # different nights
#     'seq03': [66586, 66592],           # 1953 Sep 5 and 6
#     'seq04': [66587, 66592],           # 1953 Sep 5 and 6
#     'seq05': [66588, 66592],           # 1953 Sep 5 and 6
#     'seq_special': [66586, 66587, 66588, 66592],      # entire sequence
}





