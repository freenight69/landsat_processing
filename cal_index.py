#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def cal_ndvi(red, nir):
    """
    归一化差值植被指数 NDVI = (NIR - R) / (NIR + R)
    NDVI 是最常用的植被指数。可以用来表征地面植被密集程度和植物的叶绿素含量。NDVI 数值为 -1 到 1，
    特点：通常正值表示有植被覆盖，数值越高，植被越密集或叶绿素含量越高。0 和负值表示岩石、裸土、水体等非植被覆盖。
    使用阶段：NDVI 在作物最活跃生长阶段的季节中期最准确，可以用于诊断作物的叶绿素、氮素含量，从而指导合理施用氮肥。

    :param red: red 波段矩阵
    :param nir: near infrared 波段矩阵

    :return: NDVI 矩阵
    """
    ndvi = (nir - red) / (nir + red)
    ndvi = ndvi.astype(np.float32)
    return ndvi


def cal_osavi(red, nir):
    """
    优化土壤调整植被指数 NDRE = (NIR – RED) / (NIR + RED + 0.16)
    OSAVI 主要在 NDVI 的基础上将土壤因素纳入考量，在植被生长初期、密度不高的时候，
    可以更好地排除土壤影响、反映植被的叶绿素含量。因此 OSAVI 比较适用于植被稀疏或者农田作物出苗初期的植被健康度诊断。

    :param red: red 波段矩阵
    :param nir: near infrared 波段矩阵

    :return: OSAVI 矩阵
    """
    osavi = (nir - red) / (nir + red + 0.16)
    osavi = osavi.astype(np.float32)
    return osavi


def cal_gndvi(green, nir):
    """
    绿色归一化差异植被指数 GNDVI = (NIR – GREEN) / (NIR + GREEN)
    GNDVI 相比 NDVI 能更稳定地探测植被，因此 GDNVI 也经常用于植被覆盖监测、植被和作物健康度调查中。

    :param green: green 波段矩阵
    :param nir: near infrared 波段矩阵

    :return: GNDVI 矩阵
    """
    gndvi = (nir - green) / (nir + green)
    gndvi = gndvi.astype(np.float32)
    return gndvi


def cal_reci(red, nir):
    """
    红边叶绿素植被指数 RECI = (NIR – RED) - 1
    ReCI 植被指数对受氮滋养的叶子中的叶绿素含量有反应。ReCI 显示了冠层的光合活性。
    特点：由于叶绿素含量直接取决于植物中的氮含量，这是植物“绿色”的原因，因此遥感中的这种植被指数有助于检测黄色或落叶区域。
    使用阶段：ReCI 值在植被活跃发育阶段最有用，但不适用于收获季节。

    :param red: red 波段矩阵
    :param nir: near infrared 波段矩阵

    :return: RECI 矩阵
    """
    reci = (nir - red) - 1.0
    reci = reci.astype(np.float32)
    return reci


def cal_ndmi(nir, swir1):
    """
    归一化差值水分指数 NDMI = (NIR - SWIR1) / (NIR + SWIR1)
    NDMI 通过计算近红外与短波红外之间的差异来定量化反映植被冠层的水分含量情况。
    特点：由于植被在短波红外波段对水分的强吸收，导致植被在短波红外波段的反射率相对于近红外波段的反射率要小，因此 NDMI 与冠层水分含量高度相关，
    可以用来估计植被水分含量，而且 NDMI 与地表温度之间存在较强的相关性，因此也常用于分析地表温度的变化情况。
    使用阶段：作物水分含量与地表温度的变化情况。

    :param nir: near infrared 波段矩阵
    :param swir1: shortwave infrared 1 波段矩阵

    :return: NDMI 矩阵
    """
    ndmi = (nir - swir1) / (nir + swir1)
    ndmi = ndmi.astype(np.float32)
    return ndmi
