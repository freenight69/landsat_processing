#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np
import helper
import cal_earth_sun_dist as cesd


def rad_toa(lsName, curFol, metaDict):
    """
    Calculate radiation and toa_reflectance

    creates a dict that will hold each bands/rasters name and corresponding arrays
    done beforw with eval(varName = create.array), this strangly didn't work for
    all band in Python 3.5

    :param lsName: Landsat product name
    :param curFol: Current folder
    :param metaDict: A dictionary containing the metadata

    :return: rrdict
    """

    rrdict = {}

    # Handle Landsat 8 differently than 4,5 or 7
    if lsName[3] == '8':

        for x in range(1, 10):
            xStr = str(x)

            # read bands as arrays
            rrdict['arrayDN' + xStr] = helper.singleTifToArray(curFol + lsName + "_B" + xStr + ".TIF")

            # convert to radiance and convert to 32-bit floating point for memory saving
            rrdict['lambda' + xStr] = metaDict['radiance_mult_B' + xStr] * rrdict['arrayDN' + xStr] + metaDict[
                'radiance_add_B' + xStr]
            rrdict['lambda' + xStr] = rrdict['lambda' + xStr].astype(np.float32)

            # convert to reflectance and convert to 32-bit floating point for memory saving
            rrdict['reflectance' + xStr] = ((metaDict['reflectance_mult_B' + xStr] * rrdict['arrayDN' + xStr] +
                                             metaDict['reflectance_add_B' + xStr]) / math.sin(
                math.radians(metaDict['sun_elevation'])))

            rrdict['reflectance' + xStr] = rrdict['reflectance' + xStr].astype(np.float32)

            del rrdict['arrayDN' + xStr]

    elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':
        # calculate radiation and toa relfectance
        if lsName[3] == '7':
            lastBand = 9
        else:
            lastBand = 8

        for x in range(1, lastBand):
            xStr = str(x)
            # read bands as arrays, bands 6 need to be handled separately
            if x != 6:
                rrdict['arrayDN' + xStr] = helper.singleTifToArray(curFol + lsName + "_B" + xStr + ".TIF")

                # convert to radiance and convert to 32-bit floating point for memory saving
                rrdict['lambda' + xStr] = ((metaDict['radiance_max_B' + xStr] - metaDict['radiance_min_B' + xStr]) /
                                           (metaDict['quant_max_B' + xStr] - metaDict['quant_min_B' + xStr])) * \
                                          (rrdict['arrayDN' + xStr] - metaDict['quant_min_B' + xStr]) + \
                                          metaDict['radiance_min_B' + xStr]

                rrdict['lambda' + xStr] = rrdict['lambda' + xStr].astype(np.float32)

                # convert to reflectance and convert to 32-bit floating point for memory saving
                esun = [1970, 1842, 1547, 1044, 225.7, 0, 82.06, 1369][x - 1]  # band depending constant
                e_s_dist = cesd.es_dist(metaDict["julDay"])

                rrdict['reflectance' + xStr] = (np.pi * rrdict['lambda' + xStr] * e_s_dist ** 2) / (
                        esun * math.sin(math.radians(metaDict['sun_elevation'])))

                rrdict['reflectance' + xStr] = rrdict['reflectance' + xStr].astype(np.float32)

                del rrdict['arrayDN' + xStr]

    return rrdict


def cKelvin(cal_kelvin, lsName, curFol, metaDict):
    """
    Calculates surface temperature in Kelvin, returns a dictionary with arrays

    :param cal_kelvin: Flag of calculation surface temperature in Kelvin by band 10&11
    :param lsName: Landsat product name
    :param curFol: Current folder
    :param metaDict: A dictionary containing the metadata

    :return: rrdict
    """

    kDict = {}

    # Handle Landsat 8 differently than 5 or 7
    if lsName[3] == '8':
        # calculate temperature in Kelvin  from bands 10 and 11

        if cal_kelvin == 1 or cal_kelvin == 2:
            kDict['arrayDN10'] = helper.singleTifToArray(curFol + lsName + "_B10.TIF")
            kDict['lambda10'] = metaDict['radiance_mult_B10'] * kDict['arrayDN10'] + metaDict['radiance_add_B10']
            kDict['lambda10'] = kDict['lambda10'].astype(np.float32)
            kDict['t10'] = metaDict['k2_const_B10'] / (
                np.log((metaDict['k1_const_B10'] / kDict['lambda10']) + 1))  # T in Kelvin
            kDict['t10'] = kDict['t10'].astype(np.float32)

            helper.array_to_raster(curFol + lsName + "_B10.TIF", kDict['t10'], curFol + "Temp_B10.TIF")
            del kDict['t10']

        if cal_kelvin == 1 or cal_kelvin == 3:
            kDict['arrayDN11'] = helper.singleTifToArray(curFol + lsName + "_B11.TIF")
            kDict['lambda11'] = metaDict['radiance_mult_B11'] * kDict['arrayDN11'] + metaDict['radiance_add_B11']
            kDict['lambda11'] = kDict['lambda11'].astype(np.float32)
            kDict['t11'] = metaDict['k2_const_B11'] / (np.log((metaDict['k1_const_B11'] / kDict['lambda11']) + 1))
            kDict['t11'] = kDict['t11'].astype(np.float32)

            helper.array_to_raster(curFol + lsName + "_B11.TIF", kDict['t11'], curFol + "Temp_B11.TIF")
            del kDict['t11']

    elif lsName[3] == '7' or lsName[3] == '5' or lsName[3] == '4':

        if lsName[3] == '7':
            if cal_kelvin == 1:
                startNum = 1
                endNum = 3
            elif cal_kelvin == 2:
                startNum = 1
                endNum = 2
            else:
                startNum = 2
                endNum = 3

            for y in range(startNum, endNum):
                yStr = str(y)

                kDict['arrayDN6' + yStr] = helper.singleTifToArray(curFol + lsName + "_B6_VCID_" + yStr + ".TIF")

                kDict['lambda6' + yStr] = ((metaDict['radiance_max_B6' + yStr] - metaDict['radiance_min_B6' + yStr]) /
                                           (metaDict['quant_max_B6' + yStr] - metaDict['quant_min_B6' + yStr])) * (
                                                  kDict['arrayDN6' + yStr] - metaDict['quant_min_B6' + yStr]) + \
                                          metaDict['radiance_min_B6' + yStr]

                kDict['lambda6' + yStr] = kDict['lambda6' + yStr].astype(np.float32)

                k1_const_B61 = 666.09  # 607.76 for LS5
                k2_const_B62 = 1282.71  # 1260.56 for LS5

                kDict['t6' + yStr] = k2_const_B62 / (np.log((k1_const_B61 / kDict['lambda6' + yStr]) + 1))
                kDict['t6' + yStr] = kDict['t6' + yStr].astype(np.float32)

                # del kDict['arrayDN6'+yStr]

                helper.array_to_raster(curFol + lsName + "_B6_VCID_" + yStr + ".TIF", kDict['t6' + yStr],
                                       curFol + "Temp_B6" + yStr + ".TIF")

                del kDict['t6' + yStr]

        if lsName[3] == '5' or lsName[3] == '4':
            kDict['arrayDN6'] = helper.singleTifToArray(curFol + lsName + "_B6.TIF")
            kDict['lambda6'] = (((metaDict['radiance_max_B6'] - metaDict['radiance_min_B6']) /
                                 (metaDict['quant_max_B6'] - metaDict['quant_min_B6'])) *
                                (kDict['arrayDN6'] - metaDict['quant_min_B6']) +
                                metaDict['radiance_min_B6'])
            kDict['lambda6'] = kDict['lambda6'].astype(np.float32)

            k1_const_B6 = 607.76
            k2_const_B6 = 1260.56

            kDict['t6'] = k2_const_B6 / np.log((k1_const_B6 / kDict['lambda6']) + 1)
            kDict['t6'] = kDict['t6'].astype(np.float32)

            # del kDict['arrayDN6']

            helper.array_to_raster(curFol + lsName + "_B6.TIF", kDict['t6'], curFol + "Temp_B6.TIF")

            del kDict['t6']

    return kDict
