#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
 ZTF filter informations.
"""
import os
import numpy as np
import pandas

_FILTER_LOC = os.path.dirname(os.path.realpath(__file__))+"/data/"

P48_FILTER = {"ztf:g":{"band":"g", "telescope":"p48", "instrument":"ztf"},
              "ztf:r":{"band":"r", "telescope":"p48", "instrument":"ztf"},
              "ztf:i":{"band":"i", "telescope":"p48", "instrument":"ztf"},
                }
try:
    import sncosmo
    _HAS_SNCOSMO = True
except:
    _HAS_SNCOSMO = False
    

def get_p48_filter(band):
    """ returns a pandas dataframe for the corresponding filter 
    Parameters
    ----------
    band: [str]
        P48 filter name g, r or i
        
    Returns
    -------
    pandas DataFrame (Wavelength, Effective Transmission)
    """
    
    band_ = band.lower()
    if band_ in P48_FILTER.keys():
        band_ = band_.replace("ztf:","")
    elif band_ not in ["g","r","i"]:
        raise ValueError("Only g, r, or i filter accepted, '%s' given"%band_)
    
    return pandas.read_csv(_FILTER_LOC+"filter_p48_%s.dat"%band_, sep=" ")

        
def get_p48_bandpass(band):
    """ """
    try:
        import sncosmo
    except ImportError:
        raise ImportError("You do not have sncosmo. Please install it (pip install sncosmo)")

    band_ = band.lower()
    if band_ in ["g","r","i"]:
        band_ = "z"+band
    elif band_ not in P48_FILTER.keys():
        raise ValueError("Only (ztf:)g, (ztf:)r, or (ztf:)i  filter accepted, '%s' given"%band_)
    
    try:
        return sncosmo.get_bandpass(band_)
    except:
        raise Exception("If seems that sncosmo does not know '%s' ; have you ran load_p48_filters_to_sncosmo() ?"%band_)
        
def load_p48_filters_to_sncosmo(bands="*", basename="ztf:"):
    """ register the given bands ['g','r' or 'i'] as basename+`band`"""
    try:
        import sncosmo
    except ImportError:
        raise ImportError("You do not have sncosmo. Please install it (pip install sncosmo)")
    
    bands_ = ["g","r","i"] if bands in ["all","*"] else np.atleast_1d(bands)
    
    for bandname in bands_:
        df_ = get_p48_filter(bandname)
        band = sncosmo.Bandpass(df_["wavelength"].values, df_["eff_trans"].values, name=basename+bandname.lower())
        sncosmo.registry.register(band, force=True)
    
if _HAS_SNCOSMO:
    load_p48_filters_to_sncosmo()
    
