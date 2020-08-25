#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/26 0026 15:47
# @Author : wangw
# @File   : human_intrusion_operator.py
# @Desc   :

import os
import json
from conf.data_path import DataDirectoryPath


class CaseHumanIntrusionDemoService:
    def __init__(self, path=DataDirectoryPath.get_simulation_human_path()):
        self.path = path

    @classmethod
    def get(cls):
        if get_dir_time(DataDirectoryPath.get_simulation_human_path()) != before_time:
            load(DataDirectoryPath.get_simulation_human_path())
        return {'data': data}


data = None
before_time = None


def load(path):
    global data
    global before_time
    data = None
    camera = []
    areas = {}
    area = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.split('.')[-1] == 'json':

                video_info = json.load(open(os.path.join(root, f), 'rb'))
                camera.append({"alarm_info": video_info['alarm_info'],
                               "camera_address": video_info['area_name']+'--'+video_info['camera_address'],
                               "key": video_info["key"],
                               'video': video_info['video']})

                if video_info['area_name'] not in areas.keys():
                    areas[video_info['area_name']] = []

                areas[video_info['area_name']].append(
                    {"camera_address": video_info["camera_address"], "key": video_info["key"]})

    for k, v in areas.items():
        area.append({"area_name": k, "child": v})

    data = {"area": area, "camera": camera}

    before_time = get_dir_time(path)


def get_dir_time(path):
    time = 0
    for root, dirs, files in os.walk(path):
        time += os.stat(root).st_mtime
    return time


load(DataDirectoryPath.get_simulation_human_path())

# if __name__ == '__main__':
#     path = "E:\eshore\data\case_demo\human_intrusion"
#     demo = CaseHumanIntrusionDemoService.get()