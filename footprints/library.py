import json
import warnings

import numpy as np

from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from astropy import units as u
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table, join, hstack, vstack
from astropy.time import Time
from astropy.nddata.utils import Cutout2D
from astropy.coordinates import SkyCoord, ICRS, EarthLocation
from astropy.nddata import NoOverlapError
from astropy.stats import SigmaClip
from astropy.utils.exceptions import AstropyUserWarning

from erfa import ErfaWarning
from earthshadow import get_shadow_center, get_shadow_radius, dist_from_shadow_center

from photutils.background import Background2D, MedianBackground, ModeEstimatorBackground
from photutils.profiles import RadialProfile
from photutils.psf import fit_2dgaussian

from settings import fname


'''
Library with functions or classes that are (or were) either:

 - used more than in one script;
 - used by parallelization code (to avoid namespace conflicts)
'''

def is_in_jupyter():
    '''
    Finds if the code is running in a jupyter notebook
    '''
    try:
        from IPython import get_ipython
        # Check if the function exists and if a config object is present
        if get_ipython() is not None and 'IPKernelApp' in get_ipython().config:
            return True
        else:
            return False
    except NameError:
        return False
    except ImportError:
        return False
    
    
def update_dataset(key):
    '''
    Update the 'dataset.json' file with the name of the dataset to
    be used next as a dict key by the pipeline code
    '''

    dataset_dict = {"current_dataset": key}

    try:
        json_file = open('dataset.json', 'w')
        json.dump(dataset_dict, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")


def fit_fwhm(data, *, xypos=None, fwhm=None, fit_shape=None, mask=None, error=None):
    '''
    Overrides library function in order to return the complete PSFPhotometry object
    '''
    with warnings.catch_warnings(record=True) as fit_warnings:
        phot = fit_2dgaussian(data, xypos=xypos, fwhm=fwhm, fix_fwhm=False,
                              fit_shape=fit_shape, mask=mask, error=error)

    if len(fit_warnings) > 0:
        warnings.warn('One or more fit(s) may not have converged. Please '
                      'carefully check your results. You may need to change '
                      'the input "xypos" and "fit_shape" parameters.',
                      AstropyUserWarning)

    return np.array(phot.results['fwhm_fit']), phot   # returning an extra object


def get_cutouts(file1, file2, target_coords, size):
    '''
    Extract cutouts from two images, at the same coordinates.

    Parameters:

    file1         - image file for the first image 
    file2         - image file for the second image, or None
    target_coords - the SkyCoord instance with the center coordinates of the cutouts
    size          - size of the (square) cutout size, in degrees
    '''
    def _get_cutout(file_name, target_coords, size):
        f = fits.open(file_name)

        w = WCS(f[0].header)
        data = f[0].data

        try:
            cutout = Cutout2D(data, position=target_coords, size=size, wcs=w)
        except NoOverlapError as e:
            print(e)
            return None, None
        return cutout
                    
    cutout1 = _get_cutout(file1, target_coords, size)

    cutout2 = None
    if file2 is not None:
        cutout2 = _get_cutout(file2, target_coords, size) 
        
    return cutout1, cutout2


def make_sky_coords(table, wcs):
    '''
    Converts x,y pixel positions to a SkyCoord object, using
    the provided WCS instance.
    '''
    x_pos = list(table['x_source'])
    y_pos = list(table['y_source'])
    
    world_coords = wcs.pixel_to_world(x_pos, y_pos)
    
    ras = np.array(world_coords.ra) * u.deg
    decs = np.array(world_coords.dec) * u.deg

    result = SkyCoord(ra=ras, dec=decs, frame='icrs')

    return result


def remove_outsiders(image, wcs, table, wcs_table=None, debug=False):
    '''
    Checks a set of coordinates against an image file to see if any
    coordinates fall outside the image's footprint.
    
    There are generally two WCS instances, one to convert from table
    x,y positions to sky, the other to convert from image x,y positions
    to sky. The particular case happens when both WCSs are the same.
    We have the weird function interface just for backwards compatibility.
    '''
    wcs_t = wcs
    if wcs_table is not None:
        wcs_t = wcs_table

    coords = make_sky_coords(table, wcs_t)
        
    mask = coords.contained_by(wcs, image=image)

    if debug:
        print(len(coords))
        print(coords)
        print(mask)
        print(np.any(mask))
        print(wcs)
        print(image.shape)

    
    return table[mask]


def plot_images(file1, file2, target_coords, size, title, invert_color=False, 
                figsize=(10, 5), invert_north=[False,False], invert_east=[False,False]):
    '''
    Function that plots side-by-side image cutouts coming from two files. 
    The cutouts are aligned via celestial coordinates.

    Parameters:

    file1         - image file for the image ploted at the left position on screen
    file2         - image file for the image ploted at the righ position on screen, or None
    target_coords - the SkyCoord instance with the center coordinates of the cutouts
    size          - size of the (square) cutout size, in degrees
    title         - the plot title, or None
    invert_color  - use inverted color scale?
    figsize       - plot size
    invert_north  - True if the plot should be flipped N-S
    invert_east   - True if the plot should be flipped E-W
    '''    
    cutout1, cutout2 = get_cutouts(file1, file2, target_coords, size)

    fig1, ax1, ax2 = plot_cutouts(cutout1, cutout2, target_coords, title, marker_right='rx',
                                  invert_color=invert_color, figsize=figsize, 
                                  invert_north=invert_north, invert_east=invert_east)
    
        
def plot_cutouts(cutout1, cutout2, target_coords, title, invert_color=False,
                 figsize=(10, 5), marker_left="None", marker_right="None",
                 invert_north=[False, False], invert_east=[False, False]):
    '''
    Function that plots side-by-side image cutouts. The cutouts are aligned
    via celestial coordinates.

    Parameters:

    cutout1       - image cutout
    cutout2       - image cutout, or None
    target_coords - the SkyCoord instance with positions to mark
    title         - the plot title, or None
    invert_color  - use inverted color scale?
    figsize       - plot size
    invert_north  - True if the plot should be flipped N-S
    invert_east   - True if the plot should be flipped E-W
    marker_left   - marker to be used on the left plot
    marker_right  - marker to be used on the right plot
    
    Return:
    
    fig_1         - Figure where the plots were drawn
    ax_1, ax_2    - Axis objects for each one of the plots (ax_2 can be None) 
    '''    
    def _plot(figure, index, cutout, target_coords, title, invert_color, 
              invert_north, invert_east, marker="None"):

        cw = cutout.wcs
        pixdata = cutout.data
        print("cutout shape:", cutout.data.shape, "px")

        color_map = cm.gray
        if invert_color:
            color_map = cm.gray_r

        ax = figure.add_subplot(1,2, index, projection=cw)

        image = ax.imshow(pixdata, origin='lower', cmap=color_map)

        if invert_north[0]:
            ax.invert_yaxis()
        if invert_east[0]:
            ax.invert_xaxis()
        if invert_north[1]:
            ax.invert_yaxis()
        if invert_east[1]:
            ax.invert_xaxis()

        ax.plot(target_coords.ra.deg, target_coords.dec.deg, marker, transform=ax.get_transform('world'))

        ax.grid(color='white', ls='solid')
        
        return ax
    

    fig_1 = plt.figure(figsize=figsize)

    ax_1 = _plot(fig_1, 1, cutout1, target_coords, title, invert_color, invert_north, invert_east, marker=marker_left)
    
    ax_2 = None
    if cutout2 is not None:
        ax_2 = _plot(fig_1, 2, cutout2, target_coords, title, invert_color, invert_north, invert_east, marker=marker_right)
    
    if title is not None:
        fig_1.suptitle(str(title), horizontalalignment='left', x=0.05)
    
    plt.tight_layout()
    
    return fig_1, ax_1, ax_2
    
    
def plot_profile(ax, profile, positions, sid, source_id, label_flag, title):
    '''
    Code that is common to both plot types
    '''
    # normalize
    pr_max = np.max(profile)
    pr_min = np.min(profile)
    profile = (profile - pr_min) / (pr_max - pr_min)

    label, color, linewidth, label_flag = make_labels(sid, source_id, label_flag)

    ax.plot(positions, profile, label=label, color=color, linewidth=linewidth)

    ax.set_xlabel("Position (pix)")
    ax.set_ylabel("Profile")
    ax.set_title(title)
    ax.legend()
    
    return label_flag


def get_pixel_coords(table, source_id, cutout, wcs_original):
    '''
    Gets pixel coordinates for a source on a cutout.
    
    Parameters:

    table        - table with source data
    source_id    - the source ID that identifies the table row
    cutout       - image cutout
    wcs_original - the WCS of the original image where the cutout was taken from
    
    Returns:
    
    x,y coordinates in pixels
    '''
    # get 1-row table with desired source
    mask = table['source_id'] == source_id
    t1 = table[mask]

    # compute pixel coords in cutout 
    sky_coord = make_sky_coords(t1, wcs_original)
    cutout_coords = cutout.wcs.world_to_pixel(sky_coord)

    return cutout_coords[0][0], cutout_coords[1][0]


def make_radial_profile(table, source_id, cutout, wcs_original, edge_radii):
    '''
    Makes a radial profile around position in image.
    
    Parameters:

    table        - table with X,Y pixel coordinates of object
    source_id    - the source ID that identifies the table row
    cutout       - image cutout
    wcs_original - the WCS of the original image where the cutout was taken from
    edge_radii   - array of radii defining the edges of the radial bins
    
    Returns:
    
    RadialProfile instance
    '''
    x, y = get_pixel_coords(table, source_id, cutout, wcs_original)
    
    rp = RadialProfile(cutout.data, [x, y], edge_radii)
    
    return rp


def make_labels(sid, source_id, label_flag):
    '''
    Encapsulates logic for handling plot labels and colors in profile plots
    '''
    color = 'blue'
    linewidth = 0.5
    if label_flag:
        label = 'field stars'
        label_flag = False
    else:
        label = None

    if sid == source_id:
        color = 'red'
        label = 'target object'
        linewidth = 1.0
        
    return label, color, linewidth, label_flag

    
def plot_radial_profiles(ax, table, source_id, cutout, wcs_original, edge_radii, title):
    '''
    Plots radial profiles for all rows in a table.
    
    Parameters:

    ax           - the axis where to plot
    table        - table with X,Y pixel coordinates of object
    source_id    - the source ID that identifies the table row
    cutout       - image cutout
    wcs_original - the WCS of the original image where the cutout was taken from
    edge_radii   - array of radii defining the edges of the radial bins
    title        - plot title
    '''
    label_flag = True
    
    for row in range(len(table)):
        sid = table['source_id'][row]
        rp = make_radial_profile(table, sid, cutout, wcs_original, edge_radii)
        
        positions = rp.radius
        profile = rp.profile
        
        label_flag = plot_profile(ax, profile, positions, sid, source_id, label_flag, title)

    plt.tight_layout()


def clean_bad_fits(table, par):
    '''
    Remove rows based on criteria produced by the fit_fwhm function.
    '''
    table_1 = table.copy()
    
    # we don't want any flagged fits
    mask = table_1['flags'] == 0
    table_1 = table_1[mask]

    # quality of fit: zero means a perfectly fitted Gaussian
    mask = table_1['qfit'] < par['qfit_max']
    table_1 = table_1[mask]

    # sharpness
    mask = table_1['cfit'] < par['cfit_max']
    table_1 = table_1[mask]
    mask = table_1['cfit'] > -par['cfit_max']
    table_1 = table_1[mask]
    
    return table_1


def plot_analysis_results(table, table_matched, index, par, flux_range, edge_radii):
    '''
    Builds 4-pane plot with final analsyis results.
    
    Parameters:
    
    table         - table with non-matched objects, with their PSFs already fitted
    table_matched - table with matched objects, with no PSF fitted
    index         - index in non-matched table where the target object lives
    par           - parameter dict
    flux_range    - range of peak flux where to accept stars for profile analysis
    edge_radii    - radii used to build radial profiles
    '''
    # pick up one row in the non-matched table; extract info
    plate_id = table['plate_id_1'][index]
    source_id = table['source_id'][index]
    ra  = table['ra_icrs'][index]
    dec = table['dec_icrs'][index]
    annular_bin = table['annular_bin_1'][index]
    target_flux_max = table['flux_max'][index] 
    
    # mid-exposure time and WCS from image header
    header_1 = fits.getheader(fname(par['image1']))
    header_2 = fits.getheader(fname(par['image2']))

    wcs_1 = WCS(header_1)
    
    time_stamp_1 = header_1['DATE-AVG']
    time_event_1 = Time(time_stamp_1)
    time_stamp_2 = header_2['DATE-AVG']
    
    # Earth's shadow
    es_1 = get_earth_shadow(ra, dec, time_event_1)
    formatted_es_1 = "{:.1f}".format(es_1[0])
    
    # we need the plate ID of the second plate, to display it in the title string
    table_2_name = par['table2']
    plate_id_2 = table_2_name.split('_')[1].split('.')[0]

    # title
    title = "Plate ID: " + str(plate_id) + "   "
    title = title + "DATE-AVG: " + str(time_stamp_1) + "    " 
    title = title + "Source ID: " + str(source_id) + "    " 
    title = title + "Annular Bin: " + str(annular_bin) + "    " + "\n"
    title = title + "Plate ID: " + str(plate_id_2) + "   "
    title = title + "DATE-AVG: " + str(time_stamp_2) + "    " 
    title = title + "Earth's shadow: " + formatted_es_1 + " deg." 
    
    # Cutout around target is small so we can see the target structure.
    # Neighborhood cutout picks up more stars for radial profile comparison
    target_cutout_size = float(par['display_cutout_size']) / 60. * u.deg    
    neighborhood_cutout_size = float(par['neighborhood_cutout_size']) / 60. * u.deg

    # sky coords for the target object
    target_coords = SkyCoord(ra=ra, dec=dec, unit='deg')

    # plot cutouts around target, for both images
    plot_images(fname(par['image1']), fname(par['image2']), target_coords, target_cutout_size, title, 
                invert_east=par['invert_east'], invert_north=par['invert_north'])
    
    # cutout for neighborhood needs to be explicitly handled here
    cutout_1, no_need = get_cutouts(fname(par['image1']), fname(par['image2']), 
                                    target_coords, neighborhood_cutout_size)
    

    # on the matched table, filter out rows that fall outside the neighborhood cutout footprint
    table_neighborhood = remove_outsiders(cutout_1.data, cutout_1.wcs, table_matched, wcs_table=wcs_1)
    
    # now, filter out rows that have peak flux off by more than a given limit
    mask = table_neighborhood['flux_max'] < (target_flux_max * (1. + flux_range))
    table_neighborhood = table_neighborhood[mask]
    mask = table_neighborhood['flux_max'] > (target_flux_max * (1. - flux_range))
    table_neighborhood = table_neighborhood[mask]

    # skip profile plot if neighborhood is empty of stars with same flux
    if len(table_neighborhood) < 1:
        return
        
    # arrays with celestial coordinates for displaying on the image
    coords = make_sky_coords(table_neighborhood, wcs_1)

    fig_1, ax_1, ax_2 = plot_cutouts(cutout_1, None, coords, None, figsize=(10,5), marker_left='rx',
                                     invert_east=par['invert_east'], invert_north=par['invert_north'])
    
    # to generate radial profiles, the pixel data must be inverted,
    # and background must be subtracted
    cutout_1.data = 65535. - cutout_1.data

    sigma_clip = SigmaClip(sigma=3.)
    bkg_estimator = MedianBackground()
    bkg_1 = Background2D(cutout_1.data, 40, filter_size=3, exclude_percentile=20.0, 
                         sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)

    cutout_1.data = cutout_1.data - bkg_1.background  

    # fit PSFs to the selected neighborhood stars. Convert from px in the image to px in the cutout
    fwhm_init = par['fwhm_init']
    fit_shape = par['fit_shape']
    cutout_coords = cutout_1.wcs.world_to_pixel(coords)
    xypos = list(zip(cutout_coords[0], cutout_coords[1]))
    fwhm_values_nomatch, phot_neighborhood = fit_fwhm(cutout_1.data, xypos=xypos, fwhm=fwhm_init, fit_shape=fit_shape)
    table_neighborhood_psf = hstack([table_neighborhood, phot_neighborhood.results])
    
    table_neighborhood_psf = clean_bad_fits(table_neighborhood_psf, par)

    # add target object to stars table. The radial profile plot routine requires that.
    table_all_neighborhood = vstack([table_neighborhood_psf, table[index]])
    
    ax = fig_1.add_subplot(122)

    plot_radial_profiles(ax, table_all_neighborhood, source_id, cutout_1, wcs_1, edge_radii, 'Radial profile and stats')

    text = build_stats_text(table[index], table_neighborhood_psf)
    
    props = dict(boxstyle='square', facecolor='white', alpha=0.3)
    ax.text(0.74, 0.60, text, multialignment='left', transform=ax.transAxes, fontsize=10,
            verticalalignment='center', horizontalalignment='center', bbox=props)
    
    plt.show()
    plt.close()
    

stat_pars = {'fwhm':     {'name': 'FWHM               ', 'column': 'fwhm_fit',     'flags': True},
             'fwhmerr':  {'name': 'FWHM error      ',    'column': 'fwhm_err',     'flags': True},
             'elong':    {'name': 'Elongation        ',  'column': 'elongation',   'flags': False},
             'profdiff': {'name': 'RMS profile diff   ', 'column': 'profile_diff', 'flags': False},
            }

def build_stats_text(table_object, table_stars):
    '''
    Builds multi-line text to populate the profile plot widget. 
    
    The stat_params data structure controls the text contents.
    
    Parameters:
    
    table_object  -  1-row table with the object
    table_stars   -  table with stars in the neighborhood
    '''
    flags = table_object['flags']

    text = "Target object\n"

    try:
        for key in list(stat_pars.keys()):
            name = stat_pars[key]['name']

            mark = " "
            if flags > 0 and stat_pars[key]['flags']:
                mark = "*"

            value_object = table_object[stat_pars[key]['column']]
            value_object_string = f"{value_object:5.2f}" + " " + mark
            
            text = text + name + " " + value_object_string + "\n"
    except KeyError:
        pass

    text = text + "\nField stars   (avg - stdev)\n"

    try:
        for key in list(stat_pars.keys()):

            name = stat_pars[key]['name']
            value_stars_av = np.mean(table_stars[stat_pars[key]['column']])
            value_stars_st = np.std(table_stars[stat_pars[key]['column']])

            value_stars_av_string = f"{value_stars_av:5.2f}"
            value_stars_st_string = f"{value_stars_st:5.2f}"
            
            text = text + name + " " + value_stars_av_string + " - " +  value_stars_st_string  + "\n"
    except KeyError:
        pass

    return text


def get_earth_shadow(ra, dec, time_event):
    '''
    Get angular distance from point on the sky, and center of Earth's shadow.
    
    Computed at GEO altitude
    
    Parameters:
    
    ra   -  coordinates
    dec  -
    time -  time
    
    Return:
    
    - distance in degrees
    - boolean: True - is in shadow; False - is not in shadow
    '''
    longitude = 10.242    # TODO: take this from main csv input file instead
    latitude  = 53.482

    location = EarthLocation.from_geodetic(longitude, latitude, 0.0)
    es_radius = get_shadow_radius(orbit='GEO', geocentric_angle=False)
    
    dist = dist_from_shadow_center(ra, dec, time=time_event, obs=location, orbit='GEO')
    for i, d in enumerate(dist):
        if d < es_radius - 2*u.deg:
            in_shadow = "in"
        else:
            in_shadow = "not"
            
    return dist.to_value(u.deg)[0], in_shadow

    
class Worker:
    '''
    Class with callable instances that execute the double loop in script
    find_mismatches.ipynb. The loop scans both tables, looking for coordinate
    matches between entries in each one. 

    It provides the callable for the `Pool.apply_async` function, and also
    holds all parameters necessary to perform the search.
    '''
    def __init__(self, name, table1, table2, index_init, index_end, tolerance=5./3600.):
        '''
        Parameters:

        name       - id string for this worker
        table1     - sources table for the first plate
        table2     - sources table for the second plate
        index_init - initial value for the index at the outermost loop (i1)
        index_end  - final value for the index at the outermost loop (i1)
        tolerance  - half-size of search box, in degrees. Default is 5 arcsec.

        Returns:

        list with indices in the first plate table for sources that have a 
        match in the second plate.
        '''
        self.name = name
        self.table1 = table1
        self.table2 = table2
        
        self.x_label = 'ra_icrs'
        self.y_label = 'dec_icrs'
        
        self.index_init = index_init
        self.index_end  = index_end
        self.tolerance = tolerance
                
        # results go in this list
        self.matched_rows = []
        
        # must be True in order to compare a table with itself
        self.skip_self = False
        
        # to help reporting percentage already executed
        self.ncount = 0
        self.nrange = index_end - index_init
        
        print("Worker ", name, " - ", index_init, index_end, flush=True)
        
    def __call__(self):
        
        # External loop scans the older plate.

        for i1 in range(self.index_init, self.index_end):
            
            self.ncount += 1
                
            # Internal loop scans the newer plate. 
            # We scan the entire table for every entry in the first 
            # table. Not the most efficient code by far; we keep
            # it here because the vectorized approach, which avoids
            # the internal loop in i2, is still being evaluated.
            
#             for i2 in range(len(self.table2)):
#                 if self.matched(i1, i2):
#                     self.matched_rows.append(i1)
#                     break

            # use vectorized matching code
            if self.matched_vectorized(i1):
                self.matched_rows.append(i1)

        return self.matched_rows
    
    def matched_vectorized(self, i1):
        
        # when running under a multiprocessing environment, error messages tend
        # to disappear with no trace. The trick to debug is to capture anything
        # with a try-except block and forcibly generate an output. Just the error
        # message is usually enough to tell what went wrong.
        try:
            # reference element from 1st table, row i1
            x_ref_elem = abs(self.table1[self.x_label][i1])
            y_ref_elem = abs(self.table1[self.y_label][i1])
            
            # values to be compared with are in 2nd table
            x_values = abs(self.table2[self.x_label])
            y_values = abs(self.table2[self.y_label])

            # when comparing a table with itself, use just rows forward of row i1
            if self.skip_self and i1 < len(self.table2)-1:
                x_values = abs(self.table2[self.x_label])[i1+1:]
                y_values = abs(self.table2[self.y_label])[i1+1:]

            # flag points outside the tolerance interval in X
            new_x_values   = np.where(x_values     > abs(x_ref_elem + self.tolerance), 0.0, x_values)
            new_x_values_2 = np.where(new_x_values < abs(x_ref_elem - self.tolerance), 0.0, new_x_values)

            # ditto in Y            
            new_y_values   = np.where(y_values     > abs(y_ref_elem + self.tolerance), 0.0, y_values)
            new_y_values_2 = np.where(new_y_values < abs(y_ref_elem - self.tolerance), 0.0, new_y_values)

            # anything that survived the above filtering in both X and Y will show as a 
            # non-zero value in the product.
            prod = new_x_values_2 * new_y_values_2            

            if not np.any(prod):
                # only zeros; no match
                return False

        except Exception as e:
            print("ERROR in vectorized matching code:  ", str(e), flush=True)

        # found a match

        percent = int((float(self.ncount) / float(self.nrange)) * 100.) 
        if not i1 % 2000:
            print(self.name, " - ", str(percent)+'%', ". ", i1, self.table1['source_id'][i1], flush=True)

            
        return True
    
    def matched(self, i1, i2):
        ### No longer used, but we keep it in here to provide a reference
        ### to the old code's results.

        # look for matching coordinates
        dx = abs(self.table1[self.x_label][i1] - self.table2[self.x_label][i2])

        # X coordinate differ by a tolerance
        if dx > self.tolerance:
            return False

        # same for Y coordinate
        dy = abs(self.table1[self.y_label][i1] - self.table2[self.y_label][i2])

        if dy > self.tolerance:
            return False

        # found a match

        percent = int((float(self.ncount) / float(self.nrange)) * 100.) 

        if not i1 % 500:
            print(self.name, " - ", str(percent)+'%', ". ", i1, i2, self.table1['source_id'][i1], "   ", self.table2['source_id'][i2], "  ", dx*3600, dy*3600, flush=True)
            
        return True

    
class Worker2(Worker):
    '''
    Subclass that looks for duplications in a single table.
    '''
    def __init__(self, name, table1, index_init, index_end, tolerance=5./3600.):
        '''
        Parameters:

        name       - id string for this worker
        table1     - sources table where to look for duplications
        index_init - initial value for the index at the outermost loop (i1)
        index_end  - final value for the index at the outermost loop (i1)
        tolerance  - half-size of search box, in degrees. Default is 5 arcsec.

        Returns:

        list with indices in the table that have duplications.
        '''        
        super().__init__(name, table1, table1, index_init, index_end)
        
        self.skip_self = True
                        
    def __call__(self):
        
        # External loop scans the entire table.

        for i1 in range(self.index_init, self.index_end):
            
            self.ncount += 1
                
            # Internal loop scans only what wasn't scanned yet.
            # No lunger used; kept in here for reference only.

#             for i2 in range(i1+1, len(self.table2)):
#                 if self.matched(i1, i2):
#                     self.matched_rows.append(i1)
#                     break

            # vectorized
            if self.matched_vectorized(i1):
                self.matched_rows.append(i1)

        return self.matched_rows


class FitWorker:
    '''
    Class with callable instances that uses fit_fwhm to fit Gaussians over a 
    list of x,y positions on an image.  

    It provides the callable for the `Pool.apply_async` function, and also
    holds all parameters necessary to perform the fits.
    '''
    def __init__(self, name, data, table, index_init, index_end, par):
        '''
        Parameters:

        name       - id string for this worker
        data       - numpy array with image
        table      - sources table with x,y positions to be fitted (px)
        index_init - initial value for the table index handled by this worker
        index_end  - final value for the table index handled by this worker
        par        - parameter dict from settings.py

        Returns:

        table that results from the hstack operation over the input table,
        and the table in the PSFPhotometry ".results" field
        '''
        self.name = name
        self.data = data
        
        self.index_init = index_init
        self.index_end  = index_end
        
        self.table = table[index_init:index_end]

        self.fwhm = par['fwhm_init']
        self.fit_shape = par['fit_shape']
        
        # build list with x,y positions to fit
        x_pos = list(self.table['x_source'])
        y_pos = list(self.table['y_source'])
        
        self.xypos = list(zip(x_pos, y_pos))
        
        print("Worker ", name, " - ", index_init, index_end, flush=True)
        
    def __call__(self):

        # this print is redundant with the supercalss' constructor print, but necessary
        # when running the pipeline (the superclass' print doesn't output under the pipeline)
#         print("Worker ", self.name, " - started. From row ", self.index_init, "to row", self.index_end, flush=True)

        # this is basically overriding the warnings setup in function fit_fwhm. We leave the warning
        # in the function for compatibility with the code it overrides.
        warnings.filterwarnings('ignore', category=AstropyUserWarning, message=".*One or more fit.*")

        # this function seems to not work efficiently under a parallelized environment. Perhaps it
        # puts a global lock on the data, somehow. 
        fwhm_values, phot = fit_fwhm(self.data, xypos=self.xypos, fwhm=self.fwhm, fit_shape=self.fit_shape)
        
        result = hstack([self.table, phot.results])

        print("Worker ", self.name, " - ended.", flush=True)

        return result



    

