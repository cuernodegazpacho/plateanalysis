# plateanalysis

This repo contains software dedicated to the analysis of archival photographic plates, 
searching for objects that vanish in short time scales.

Code is being developed around the data provided by the APPLAUSE archive. Code is all in the form
of IPython notebooks. With some minor work, scripts can be upgraded to ingest data from other 
archives as well.

APPLAUSE provides not only the hi-res raw scans of plates, but also sextractor-built lists of 
"sources" detected in each scan. These lists are the primary data used by the scripts. To enable
these scripts to work with other archives, the main job would be then to create or adapt such
source lists to the format needed by the search/analysis algorithm.

The notebooks break down the algorithm into manageable steps:

- look for suitable plates in the database that fullfill certain criteria, such as:
   - plates from the same telescope;
   - plates taken in the same night;
   - plate FOVs overlap by a significant area;

- all data for a sequence of such plates (scans, source tables) is downloaded from APPLAUSE;
- a sequence is broken down into pairs of consecutive exposures;
- and, for each one of those pairs:
    - look for all sources listed for the first plate, that *do not* have a counterpart in 
      the second plate - these are the candidates for vanishing objects;
    - fit FWHM and other parameters (from a model Gaussian and from empirical radial profiles)
      onto each one of these non-matched sources;
    - compare these parameters with the same parameters derived from sources *with* a counterpart;
    - display results from the few promising candidates that result from the statistical
      comparison, and vet them manually.

Most of the work can be performed by a pipeline (batch mode). The bottleneck is obviously 
the manual vetting step. We hope that a better statistical analysis will eventually lead to an
almost fully automatic pipeline.



