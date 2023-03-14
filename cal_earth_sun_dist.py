#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


# ----------------------------------------------------------------------------------#
#    All of the follwing are used to calculate earth-sun distance, adapted from
#    http://davit.ece.vt.edu/davitpy/_modules/utils/calcSun.html#calcSunRadVector
# ----------------------------------------------------------------------------------#
def cal_geoMeanAnomalySun(t):
    """
    Calculate the Geometric Mean Anomaly of the Sun (in degrees)

    :param t: time

    :return: geometric mean anomaly of the sun (in degrees)
    """
    M = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    return M  # in degrees


def cal_eccentricityEarthOrbit(t):
    """
    Calculate the eccentricity of earth's orbit (unitless)

    :param t: time

    :return: the eccentricity of earth's orbit (unitless)
    """
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    return e  # unitless


def cal_sunEqOfCenter(t):
    """
    Calculate the equation of center for the sun (in degrees)

    :param t: time

    :return: the equation of center for the sun (in degrees)
    """
    mrad = np.radians(cal_geoMeanAnomalySun(t))
    sinm = np.sin(mrad)
    sin2m = np.sin(mrad + mrad)
    sin3m = np.sin(mrad + mrad + mrad)
    C = (sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) +
         sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289)
    return C  # in degrees


def cal_sunTrueAnomaly(t):
    """
    Calculate the True Anomaly of the Sun (in degrees)

    :param t: time

    :return: the true anomaly of the sun (in degrees)
    """
    m = cal_geoMeanAnomalySun(t)
    c = cal_sunEqOfCenter(t)
    v = m + c
    return v  # in degrees


def es_dist(t):
    """
    Calculate earth-sun distance

    :param t: time

    :return: the earth-sun distance
    """
    # eccent = 0.01672592        # Eccentricity of Earth orbit
    # axsmaj = 1.4957            # Semi-major axis of Earth orbit (km)
    # solyr  = 365.2563855       # Number of days in a solar year

    v = cal_sunTrueAnomaly(t)
    e = cal_eccentricityEarthOrbit(t)
    R = (1.000001018 * (1. - e * e)) / (1. + e * np.cos(np.radians(v)))
    return R
