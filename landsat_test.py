#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: landsat_test.py
Version: v1.0
Date: 2023-03-14
Authors: Chen G.
Description: This script creates downloading and processing SLandsat images.
License: This code is distributed under the MIT License.

    Landsat_download Parameter:
        USER_NAME: The account name to log in USGS website (https://earthexplorer.usgs.gov/).
        PASSWORD: The account password to log in USGS website.
        SEARCH_FILE: The region to include imagery within.
        PRODUCT_TYPE: Type of sentinel-2 product to apply (String):
            'landsat_tm_c1' - Landsat 5 TM Collection 1 Level 1
            'landsat_tm_c2_l1' - Landsat 5 TM Collection 2 Level 1
            'landsat_tm_c2_l2' - Landsat 5 TM Collection 2 Level 2
            'landsat_etm_c1' - Landsat 7 ETM+ Collection 1 Level 1
            'landsat_etm_c2_l1' - Landsat 7 ETM+ Collection 2 Level 1
            'landsat_etm_c2_l2' - Landsat 7 ETM+ Collection 2 Level 2
            'landsat_8_c1' - Landsat 8 Collection 1 Level 1
            'landsat_ot_c2_l1' - Landsat 8 Collection 2 Level 1
            'landsat_ot_c2_l2' - Landsat 8 Collection 2 Level 2
            'sentinel_2a' - Sentinel 2A
        START_DATE: A time interval filter based on the Sensing Start Time of the products.
        END_DATE: A time interval filter based on the Sensing Start Time of the products.
        MAX_CLOUD_COVER: (Optional) cloud cover percentage to apply landsat products filter.
        OUTPUT_DIR: Download the landsat images to local.


    """

import datetime
import landsat_download as ld
import landsat_process as lp

# Parameters
landsat_download_parameter = {'USER_NAME': 'gongchen9369',
                              'PASSWORD': '13919389875Er',
                              'SEARCH_FILE': 'F:/geoserver_data/shp/lingang_field',
                              'DATASET': 'landsat_8_c1',
                              'START_DATE': '2023-01-01',
                              'END_DATE': '2023-03-15',
                              'MAX_CLOUD_COVER': 50,
                              'OUTPUT_DIR': 'G:/landsat/download'
                              }

landsat_process_parameter = {'INPUT_PATH': 'G:/landsat/download',
                             'OUTPUT_PATH': 'G:/landsat/export',
                             'DELETE_ORIGINAL': 1,
                             'SAVE_RADIATION': 0,
                             'SAVE_REFLECTANCE': 0,
                             'CAL_KELVIN': 0,
                             'ALL_INDICES': 0,
                             'SAVE_INDICES': 0
                             }

# /***************************/
# // MAIN
# /***************************/
if __name__ == "__main__":
    start_time = datetime.datetime.now()

    # (1) Landsat产品数据下载
    ld.landsat_download(landsat_download_parameter)

    # (2) Landsat产品数据处理
    lp.land_process(landsat_process_parameter)

    end_time = datetime.datetime.now()
    # 输出程序运行所需时间
    print("Elapsed Time:", end_time - start_time)
