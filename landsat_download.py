#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import geopandas as gpd
import warnings


def search_image(username, password, search_file, dataset, start_date, end_date, max_cloud_cover):
    """
    利用EarthExplorer portal根据搜索条件查询影像

    :param username: USGS网站（https://earthexplorer.usgs.gov/）注册用户名
    :param password: USGS网站注册用户密码
    :param search_file: 查询矢量文件
    :param dataset: 查询影像数据集
    :param start_date: 查询起始日期
    :param end_date: 查询终止日期
    :param max_cloud_cover: 查询光学影像云量条件

    :return: 查询结果影像
    """
    warnings.filterwarnings(action="ignore")
    # 初始化API接口获取key
    api = API(username, password)
    # 输入要查询的边界
    data = gpd.read_file(search_file)
    # 输入轨道矢量
    grid_file = ""
    if "sentinel" in dataset.lower():
        grid_file = "./grid_shp/sentinel2_grid.shp"
    elif "landsat" in dataset.lower():
        # 输入landsat轨道矢量
        grid_file = "./grid_shp/WRS2_descending.shp"
    wrs = gpd.GeoDataFrame.from_file(grid_file)
    # 查询边界覆盖的轨道中心坐标
    wrs_intersection = wrs[wrs.intersects(data.geometry[0])]
    longitude = wrs_intersection.centroid.x.values
    latitude = wrs_intersection.centroid.y.values

    # 查询
    all_scene = []
    for i in range(len(latitude)):
        scenes = api.search(dataset=dataset, latitude=latitude[i], longitude=longitude[i],
                            start_date=start_date, end_date=end_date, max_cloud_cover=max_cloud_cover)
        all_scene += scenes
    api.logout()
    return all_scene


def download_from_landsatexplore(username, password, output_dir, scene_list):
    """
    根据查询结果下载影像

    :param username: USGS网站（https://earthexplorer.usgs.gov/）注册用户名
    :param password: USGS网站注册用户密码
    :param output_dir: 下载影像保存地址
    :param scene_list: 查询影像结果
    """
    if len(scene_list) > 0:
        # 登入EarthExplorer
        ee = EarthExplorer(username, password)
        # 根据ID下载影像
        for scene in scene_list:
            output_dir_demon = output_dir + '\\' + str(scene['acquisition_date'].year)
            if not os.path.isdir(output_dir_demon):
                os.mkdir(output_dir_demon)
            print("Downloading: " + scene['display_id'])
            ee.download(identifier=scene['entity_id'], output_dir=output_dir_demon)
        ee.logout()


# ---------------------------------------------------#
#   从USGS官网下载Landsat数据
# ---------------------------------------------------#
def landsat_download(params):
    """
    Downloading Landsat images from USGS.

    param: params
        These parameters determine the data selection and image saving parameters.
    """
    USER_NAME = params['USER_NAME']
    PASSWORD = params['PASSWORD']
    SEARCH_FILE = params['SEARCH_FILE']
    DATASET = params['DATASET']
    START_DATE = params['START_DATE']
    END_DATE = params['END_DATE']
    MAX_CLOUD_COVER = params['MAX_CLOUD_COVER']
    OUTPUT_DIR = params['OUTPUT_DIR']

    ###########################################
    # 0. CHECK PARAMETERS
    ###########################################

    if USER_NAME is None:
        raise ValueError("ERROR!!! Parameter USER_NAME is none")
    if PASSWORD is None:
        raise ValueError("ERROR!!! Parameter PASSWORD is none")
    if SEARCH_FILE is None:
        raise ValueError("ERROR!!! Parameter SEARCH_FILE not correctly defined")
    if START_DATE is None:
        raise ValueError("ERROR!!! Parameter START_DATE not correctly defined")
    if END_DATE is None:
        raise ValueError("ERROR!!! Parameter END_DATE not correctly defined")
    if MAX_CLOUD_COVER is None:
        MAX_CLOUD_COVER = 100
    if OUTPUT_DIR is None:
        raise ValueError("ERROR!!! Parameter OUTPUT_DIR not correctly defined")

    dateset_required = ['landsat_tm_c1', 'landsat_tm_c2_l1', 'landsat_tm_c2_l2', 'landsat_etm_c1', 'landsat_etm_c2_l1',
                        'landsat_etm_c2_l2', 'landsat_8_c1', 'landsat_ot_c2_l1', 'landsat_ot_c2_l2', 'sentinel_2a']
    if DATASET not in dateset_required:
        raise ValueError("ERROR!!! Parameter DATASET not correctly defined")

    ###########################################
    # 1. DATA SELECTION
    ###########################################

    # 查询数据
    print("searching...")
    search_list = search_image(USER_NAME, PASSWORD, SEARCH_FILE, DATASET, START_DATE, END_DATE, MAX_CLOUD_COVER)
    print("%s scenes found" % (len(search_list)))
    for i in range(len(search_list)):
        print(search_list[i].get('display_id'))

    # 下载数据
    download_from_landsatexplore(USER_NAME, PASSWORD, OUTPUT_DIR, search_list)
