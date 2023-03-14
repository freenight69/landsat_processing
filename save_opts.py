#!/usr/bin/env python
# -*- coding: utf-8 -*-
import helper
import cal_index as ci


def saveRadOpt(lsName, curFol, rrdict, calcKelvin):
    """
    Save radiation rasters to disk

    :param lsName: Landsat product name
    :param curFol: Current folder
    :param rrdict: A dictionary containing each bands/rasters name and corresponding arrays
    :param calcKelvin: Flag of calculation surface temperature in Kelvin

    """
    if lsName[3] == '8':

        if calcKelvin == 0:
            endRange = 10
        else:
            endRange = 12

        for x in range(1, endRange):
            xStr = str(x)
            helper.array_to_raster(curFol + lsName + "_B" + xStr + ".tif", rrdict['lambda' + xStr],
                                   curFol + "Radiation_B" + xStr + ".tif")
            # del rrdict['lambda'+xStr]

    elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':

        if lsName[3] == '7':
            lastBand = 9
        else:
            lastBand = 8

        for x in range(1, lastBand):
            xStr = str(x)
            if lsName[3] == '7':
                if x != 6:
                    helper.array_to_raster(curFol + lsName + "_B" + xStr + ".tif", rrdict['lambda' + xStr],
                                           curFol + "Radiation_B" + xStr + ".tif")
                    # del rrdict['lambda'+xStr]

                else:
                    if calcKelvin != 0:
                        for y in range(1, 3):
                            yStr = str(y)
                            try:
                                helper.array_to_raster(curFol + lsName + "_B" + xStr + "_VCID_" + yStr + ".tif",
                                                       rrdict['lambda' + xStr + yStr],
                                                       curFol + "Radiation_B" + xStr + yStr + ".tif")
                                # del  rrdict['lambda'+xStr+yStr]

                            except:
                                pass

            if lsName[3] == '5' or lsName[3] == '4':
                if calcKelvin != 0:
                    helper.array_to_raster(curFol + lsName + "_B" + xStr + ".tif", rrdict['lambda' + xStr],
                                           curFol + "Radiation_B" + xStr + ".tif")
                # del rrdict['lambda'+xStr]


def saveReflOpt(lsName, curFol, rrdict):
    """
    Save reflectance rasters to disk

    :param lsName: Landsat product name
    :param curFol: Current folder
    :param rrdict: A dictionary containing each bands/rasters name and corresponding arrays

    """
    if lsName[3] == '8':
        for x in range(1, 10):
            xStr = str(x)
            helper.array_to_raster(curFol + lsName + "_B" + xStr + ".tif", rrdict['reflectance' + xStr],
                                   curFol + "Reflectance_B" + xStr + ".tif")
            # del rrdict['reflectance'+xStr]

    elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':

        if lsName[3] == '7':
            lastBand = 9
        else:
            lastBand = 8

        for x in range(1, lastBand):
            xStr = str(x)
            if x != 6:
                helper.array_to_raster(curFol + lsName + "_B" + xStr + ".tif", rrdict['reflectance' + xStr],
                                       curFol + "Reflectance_B" + xStr + ".tif")
                # del rrdict['reflectance'+xStr]


def specIndOpt(lsName, curFol, allIndices, rrdict, saveInd=1):
    """
    Calculate spectral indices, returns a dictionary and also saves all tiffs to disk

    :param lsName: Landsat product name
    :param curFol: Current folder
    :param allIndices: Flag of calculation vegetation indices
    :param rrdict: A dictionary containing each bands/rasters name and corresponding arrays
    :param saveInd: Flag of saving indices to disk

    """

    specDict = {}

    # Calculate NDVI
    if allIndices == 1 or allIndices == 2:
        if lsName[3] == '8':
            ndviAr = ci.cal_ndvi(rrdict['reflectance4'], rrdict['reflectance5'])
        elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':
            ndviAr = ci.cal_ndvi(rrdict['reflectance3'], rrdict['reflectance4'])
        if saveInd == 1:
            helper.array_to_raster(curFol + lsName + "_B4.TIF", ndviAr, curFol + lsName[:-5] + "_NDVI.tif")
        specDict['ndviAr'] = ndviAr

    # Calculate OSAVI
    if allIndices == 1 or allIndices == 3:
        if lsName[3] == '8':
            osaviAr = ci.cal_osavi(rrdict['reflectance4'], rrdict['reflectance5'])
        elif lsName[2] == '7' or lsName[2] == '5' or lsName[2] == '4':
            osaviAr = ci.cal_osavi(rrdict['reflectance3'], rrdict['reflectance4'])
        if saveInd == 1:
            helper.array_to_raster(curFol + lsName + "_B4.TIF", osaviAr, curFol + lsName[:-5] + "_OSAVI.tif")
        specDict['osaviAr'] = osaviAr

    # Calculate GNDVI
    if allIndices == 1 or allIndices == 4:
        if lsName[3] == '8':
            gndviAr = ci.cal_gndvi(rrdict['reflectance3'], rrdict['reflectance5'])
        elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':
            gndviAr = ci.cal_gndvi(rrdict['reflectance2'], rrdict['reflectance4'])
        if saveInd == 1:
            helper.array_to_raster(curFol + lsName + "_B3.TIF", gndviAr, curFol + lsName[:-5] + "_GNDVI.tif")
        specDict['gndviAr'] = gndviAr

    # Calculate RECI
    if allIndices == 1 or allIndices == 5:
        if lsName[3] == '8':
            reciAr = ci.cal_reci(rrdict['reflectance4'], rrdict['reflectance5'])
        elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':
            reciAr = ci.cal_reci(rrdict['reflectance3'], rrdict['reflectance4'])
        if saveInd == 1:
            helper.array_to_raster(curFol + lsName + "_B4.TIF", reciAr, curFol + lsName[:-5] + "_RECI.tif")
        specDict['reciAr'] = reciAr

    # Calculate NDMI
    if allIndices == 1 or allIndices == 6:
        if lsName[3] == '8':
            ndmiAr = ci.cal_ndmi(rrdict['reflectance5'], rrdict['reflectance6'])
        elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':
            ndmiAr = ci.cal_ndmi(['reflectance4'], rrdict['reflectance5'])
        if saveInd == 1:
            helper.array_to_raster(curFol + lsName + "_B5.TIF", ndmiAr, curFol + lsName[:-5] + "_NDMI.tif")
        specDict['ndmiAr'] = ndmiAr

    return specDict
