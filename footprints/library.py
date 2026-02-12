import warnings

import numpy as np

from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from astropy import units as u
from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata.utils import Cutout2D
from astropy.coordinates import SkyCoord, ICRS
from astropy.nddata import NoOverlapError
from astropy.utils.exceptions import AstropyUserWarning


from photutils.psf import fit_2dgaussian


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


def remove_outsiders(image, wcs, table, wcs_table=None):
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

    return table[mask]


def plot_images(file1, file2, target_coords, size, title, invert_color=False, 
                invert_north=[False,False], invert_east=[False,False]):
    '''
    Function that plots side-by-side image cutouts coming from two files. 
    The cutouts are aligned via celestial coordinates.

    Parameters:

    file1         - image file for the image ploted at the left position on screen
    file2         - image file for the image ploted at the righ position on screen, or None
    target_coords - the SkyCoord instance with the center coordinates of the cutouts
    size          - size of the (square) cutout size, in degrees
    title         - the plot title
    invert_color  - use inverted color scale?
    invert_north  - True if the plot should be flipped N-S
    invert_east   - True if the plot should be flipped E-W
    '''    
    cutout1, cutout2 = get_cutouts(file1, file2, target_coords, size)

    plot_cutouts(cutout1, cutout2, target_coords, title, invert_color=invert_color, 
                invert_north=invert_north, invert_east=invert_east)
    
        
def plot_cutouts(cutout1, cutout2, target_coords, title, invert_color=False, 
                invert_north=[False, False], invert_east=[False, False]):
    '''
    Function that plots side-by-side image cutouts. The cutouts are aligned
    via celestial coordinates.

    Parameters:

    cutout1       - image cutout
    cutout2       - image cutout, or None
    target_coords - the SkyCoord instance with positions to mark
    title         - the plot title
    invert_color  - use inverted color scale?
    invert_north  - True if the plot should be flipped N-S
    invert_east   - True if the plot should be flipped E-W
    '''    
    
    def _plot(index, cutout, target_coords, title, invert_color, invert_north, invert_east):

        cw = cutout.wcs
        pixdata = cutout.data
        print(cutout.data.shape)

        color_map = cm.gray
        if invert_color:
            color_map = cm.gray_r

        ax = fig.add_subplot(1,2, index, projection=cw)

        image = ax.imshow(pixdata, origin='lower', cmap=color_map)

        if invert_north[0]:
            ax.invert_yaxis()
        if invert_east[0]:
            ax.invert_xaxis()
        if invert_north[1]:
            ax.invert_yaxis()
        if invert_east[1]:
            ax.invert_xaxis()

        ax.plot(target_coords.ra.deg, target_coords.dec.deg, 'rx', transform=ax.get_transform('world'))

        ax.grid(color='white', ls='solid')
    

    fig = plt.figure(figsize=(10, 5))

    _plot(1, cutout1, target_coords, title, invert_color, invert_north, invert_east)
    
    if cutout2 is not None:
        _plot(2, cutout2, target_coords, title, invert_color, invert_north, invert_east)
    
    fig.suptitle(str(title))
    
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


class Worker:
    '''
    Class with callable instances that executes the double loop in script
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
        
        # to help reporting percentage already executed
        self.ncount = 0
        self.nrange = index_end - index_init
        
        print("Worker ", name, " - ", index_init, index_end, flush=True)
        
    def __call__(self):
        
        # External loop scans the older plate.

        for i1 in range(self.index_init, self.index_end):
            
            self.ncount += 1
                
            # Internal loop scans the newer plate. We scan the entire table for every entry
            # in the first table. 

            for i2 in range(len(self.table2)):
                
                if self.matched(i1, i2):
                    self.matched_rows.append(i1)
                    break

        return self.matched_rows
    
    def matched(self, i1, i2):
        # look for matching coordinates
        dx = abs(self.table1[self.x_label][i1] - self.table2[self.x_label][i2])

        # X coordinate differ by a tolerance
        if dx > self.tolerance:
            return False

        # same for Y coordinate
        dy = abs(self.table1[self.y_label][i1] - self.table2[self.y_label][i2])

        if dy > self.tolerance:
            return False

        # coordinates match

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
                        
    def __call__(self):
        
        # External loop scans the entire table.

        for i1 in range(self.index_init, self.index_end):
            
            self.ncount += 1
                
            # Internal loop scans only what wasn't scanned yet.

            for i2 in range(i1+1, len(self.table2)):
                
                if self.matched(i1, i2):
                    self.matched_rows.append(i1)
                    break

        return self.matched_rows
    

