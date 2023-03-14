#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import tarfile
import helper
import meta_data
import cal_rad_ref_temp as crrt
import save_opts as saveopt


def lan_preprocess(inFile, outFol, deleteOriginal, saveRadiation, saveReflectance, calcKelvin, allIndices, saveInd):
    """
    Handles the calls for all above functions
    Basically fills the 'metaDict'dictionary with data from the Landsat MTL file and
    the 'rrdict' dictionary with arrays that may be saved to disk later

    :param inFile:             a tar.gz file path
    :param outFol:             output folder, here a subfolder with the LS name will be created
                               This folder will store all desired final tiffs

    :param deleteOriginal:     Flag for deleting exracted inital DN Rasters
                               1 = keep all, 2 = delete all, 3 = delete but keep metafile
                               Note: folder needs to be empty at start, else all is deleted

    :param saveRadiation:      if True Radiation Tiffs will be saved to disk

    :param saveReflectance:    if True Reflectance Tiffs will be saved to disk

    :param calcKelvin:         Flag for calculating temperature rasters in Kelvin
                               0 = no calculation, 1 = calc Band 10&11 or 61/62,
                               2 = calc B10/61 only, 3=calc B11/62 only

    :param allIndices:         Flag for calculating all/one indices
                               0 = none, 1= all, 2 = NDVI, 3 = OSAVI, 4 = GNDVI, 5 = RECI, 6 = NDMI

    :param saveInd:     	  Flag if Indices should be saved to disk? 0 = no, 1 = yes (default)


    """

    # Extract Metainfo from packaged Landsat Data
    tar = tarfile.open(inFile)
    # members = tar.getmembers()

    # Name of current Landsat file, extracted from tarfile name
    lsName = inFile[inFile.rfind("/") + 1:inFile.find(".")]

    # Define output Folder and extract tar-file into it
    curFol = outFol + lsName + "/"
    helper.chkdir2(curFol)
    tar.extractall(curFol)

    # Read out the metafile
    metaDict = meta_data.extract_metaData(curFol, lsName)

    # collect filenames in a list to maybe delete later
    orgList = []
    for x in os.listdir(curFol):
        orgList.append(curFol + x)

    # Fill dictionary with radiation and toa
    rrdict = crrt.rad_toa(lsName, curFol, metaDict)

    # update rrdict if Temperatures should be calculated
    if calcKelvin > 0:
        kDict = crrt.cKelvin(calcKelvin, lsName, curFol, metaDict)
        rrdict.update(kDict)

    # Save radioation rasters to disk. Thermal bands only if temperature calculated before
    if saveRadiation > 0:
        saveopt.saveRadOpt(lsName, curFol, rrdict, calcKelvin)

    if allIndices > 0:
        specDict = saveopt.specIndOpt(lsName, curFol, allIndices, rrdict, saveInd)
        rrdict.update(specDict)

    if saveReflectance > 0:
        saveopt.saveReflOpt(lsName, curFol, rrdict)

    # delete originally extracted files
    if deleteOriginal == 2:
        for x in orgList:
            if x[-4] == ".":
                os.remove(x)
            else:
                shutil.rmtree(x)  # accounts for folder, os.remove only removes files
    elif deleteOriginal == 3:
        for x in orgList:
            if x[-7:].lower() != "mtl.txt":
                if x[-4] == ".":
                    os.remove(x)
                else:
                    shutil.rmtree(x)  # accounts for folder, os.remove only removes files
    return rrdict


# ---------------------------------------------------#
#   Processing Landsat product data
# ---------------------------------------------------#
def land_process(params):
    """
    Processing Landsat product.

    :param params: These parameters determine the data processing parameters.
    """
    INPUT_PATH = params['INPUT_PATH']
    OUTPUT_PATH = params['OUTPUT_PATH']
    DELETE_ORIGINAL = params['DELETE_ORIGINAL']
    SAVE_RADIATION = params['SAVE_RADIATION']
    SAVE_REFLECTANCE = params['SAVE_REFLECTANCE']
    CAL_KELVIN = params['CAL_KELVIN']
    ALL_INDICES = params['ALL_INDICES']
    SAVE_INDICES = params['SAVE_INDICES']

    ###########################################
    # CHECK PARAMETERS
    ###########################################

    if INPUT_PATH is None:
        raise ValueError("ERROR!!! Parameter INPUT_PATH not correctly defined")
    if OUTPUT_PATH is None:
        raise ValueError("ERROR!!! Parameter OUTPUT_PATH not correctly defined")
    if DELETE_ORIGINAL is None:
        DELETE_ORIGINAL = 1
    if SAVE_RADIATION is None:
        SAVE_RADIATION = 0
    if SAVE_REFLECTANCE is None:
        SAVE_REFLECTANCE = 0
    if CAL_KELVIN is None:
        CAL_KELVIN = 0
    if ALL_INDICES is None:
        ALL_INDICES = 0
    if SAVE_INDICES is None:
        SAVE_INDICES = 0

    ###########################################
    # PROCESSING LANDSAT PRODUCT
    ###########################################
    # Create output directory
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # Get input products
    fileList = []
    for files in os.listdir(INPUT_PATH):
        fileList.append(INPUT_PATH + files)

    # processing Landsat products
    myDict = {}
    for inFilex in fileList:
        myDict = lan_preprocess(INPUT_PATH, OUTPUT_PATH, DELETE_ORIGINAL, SAVE_RADIATION, SAVE_REFLECTANCE, CAL_KELVIN,
                                ALL_INDICES, SAVE_INDICES)
        print("%s file completed" % inFilex[-47:-7])
