#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/25 0025 15:41
# @Author : wangw
# @File   : camera_monitor_operator.py
# @Desc   :

import os
import numpy as np
import json
import random

from typing import List
from sqlalchemy.sql.expression import func

from app.models.m_demo_message import *
from conf.data_path import DataDirectoryPath, SimulationDName, SimulationCameraDName

import requests

ak = 'CErvxNguuZ7PTF0uirFvwyBVLG0xoG1G'
url = 'http://api.map.baidu.com/place/v2/search'

config = {'city': '广州市',
          'area': {'越秀区': 398, '荔湾区': 421, '海珠区': 370, '天河区': 387, '白云区': 413, '黄埔区': 442, '番禺区': 364, '花都区': 373, '南沙区': 453, '增城区': 334, '从化区': 513},
          'area2': {'增城区': 334},
          'query': ['路', '道', '街'],
          'page_size': 20,
          'output': 'json',
          'ak': ak,
          'districts': {'越秀区': 1, '荔湾区': 2, '海珠区': 3, '天河区': 4, '白云区': 5, '黄埔区': 6, '番禺区': 7, '花都区': 8, '南沙区': 9, '增城区': 10, '从化区': 11}
          }


class CaseCameraMonitorDemoService(object):

    def __init__(self, path=DataDirectoryPath.get_simulation_camera_path()):
        self.path = path

    def count_street(self):

        area_street_nums = {}
        for root, dirs, files in os.walk('./'):
            for file in files:
                if file.split('.')[-1] == 'json':
                    with open(os.path.join(root, file), 'rb') as f:
                        area_data = json.load(f)
                        street = set()
                        try:
                            for e in area_data['results']:
                                street.add(e['name'])
                            # area_street_nums[area_data['area']] = area_data['area']
                            nums = {s: 0 for s in street}
                            self.assign_street_nums(config['area'][area_data['area']], street, nums, config['area'][area_data['area']])
                            area_street_nums.update(nums)
                        except Exception:
                            continue

        return area_street_nums

    def map_to_mysql(self):
        # 一次入库就可以
        return
        self.get_from_api()
        area_street_nums = self.count_street()
        for root, dirs, files in os.walk('./'):
            for file in files:
                if file.split('.')[-1] == 'json':
                    with open(os.path.join(root, file), 'rb') as f:
                        area_data = json.load(f)
                        try:
                            for e in area_data['results']:
                                if area_data['area'] not in e['address']:
                                    continue
                                address, longitude, latitude, amount, district_id = e['address'], e['longitude'], e['latitude'], area_street_nums[e['name']], config['districts'][area_data['area']]
                                print(longitude, ' ', latitude, ' ', address, ' ', amount, ' ', config['districts'][area_data['area']], area_data['area'])

                                camera_distribution: CameraDistribution = CameraDistribution(longitude=longitude,
                                                                                             latitude=latitude,
                                                                                             address=address,
                                                                                             amount=amount,
                                                                                             district_id=district_id)
                                db.session.add(camera_distribution)
                        except Exception:
                            continue

        db.session.commit()

        # 删除json
        for root, dirs, files in os.walk('./'):
            for file in files:
                if file.split('.')[-1] == 'json' and file.split('.')[0] in config['area'].keys():
                    os.remove(file)
        return area_street_nums

    @staticmethod
    def get_from_api():
        address_location_json = {'data': []}

        for area in config['area'].keys():
            param = {}
            if area in "增城区":
                param['region'] = '广州增城'
            else:
                param['region'] = config['city'] + area

            data = {}
            data['city'] = config['city'],
            data['area'] = area
            data['results'] = []

            for query in config['query']:
                param['query'] = query
                param['page_size'] = config['page_size']
                param['output'] = config['output']
                param['ak'] = config['ak']
                attempts = 0
                success = False
                while attempts < 50 and not success:
                    try:
                        response = requests.get(url, param)
                        jd = json.loads(response.text)

                        streets = set()
                        for e in jd['results']:
                            # print(e['location']['lng'], e['location']['lat'], e['province'] + e['city'] + e['area'] + e['name'])
                            try:
                                if area != e['area']:
                                    continue
                                data['results'].append({'address': e['province'] + e['city'] + e['area'] + e['name'],  'longitude': e['location']['lng'], 'latitude': e['location']['lat'], 'name': e['name']})
                                success = True
                            except Exception:
                                attempts += 1
                        address_location_json['data'].append(data)
                    except Exception:
                        attempts += 1

            with open(area + '.json', 'w') as f:
                json.dump(data, f)

        return address_location_json

    @staticmethod
    def save(file, data):
        with open(file, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load(file):
        with open(file, 'rb') as f:
            add_loc_json = json.load(f)
        return add_loc_json

    def assign_street_nums(self, remain: int, street: set, nums, total: int):
        for k in list(street):
            if not street:
                return
            else:
                nums[k] = np.random.randint(int(remain / len(street))) + 1
                street.remove(k)
                self.assign_street_nums(total - sum(nums.values()), street, nums, total)

    @classmethod
    def distribution(cls) -> list:
        result = []
        cities: List[City] = City.query.all()
        for city in cities:
            city_msg = dict()
            city_msg['city'] = city.name
            city_msg['city_id'] = city.id
            city_msg['districts'] = []
            districts: List[UrbanDistrict] = city.districts.all()
            for district in districts:
                district_msg = dict()
                district_msg['district'] = district.name
                district_msg['district_id'] = district.id
                district_msg['streets'] = []
                streets: List[CameraDistribution] = district.street.all()
                for street in streets:
                    street_msg = dict()
                    street_msg['longitude'] = street.longitude
                    street_msg['latitude'] = street.latitude
                    street_msg['address'] = street.address
                    street_msg['amount'] = street.amount
                    district_msg['streets'].append(street_msg)
                district_msg['amount'] = sum([street['amount'] for street in district_msg['streets']])
                city_msg['districts'].append(district_msg)
            city_msg['amount'] = sum([district['amount'] for district in city_msg['districts']])
            result.append(city_msg)
        return result

    @classmethod
    def get(cls, status_id: int) -> dict:

        if get_dir_time(DataDirectoryPath.get_simulation_camera_path()) != before_time:  # 更新
            load(DataDirectoryPath.get_simulation_camera_path())
        status_id_name = {"0": "正常", "1": "黑屏", "2": "单色", "3": "遮挡", "4": "偏移"}
        try:
            scenes = scenes_json[str(status_id)]
            try:
                rand_scene_num = np.random.randint(len(scenes))
            except Exception:
                raise
            # 随机取一个场景
            rand_scene = scenes[rand_scene_num]

            # 从场景中随机选择两张图片

            rand_pic_num_0 = np.random.randint(len(picture_json[rand_scene][str(0)]))
            rand_pic_num_x = np.random.randint(len(picture_json[rand_scene][str(status_id)]))
            pic_0 = picture_json[rand_scene][str(0)][rand_pic_num_0]
            pic_x = picture_json[rand_scene][str(status_id)][rand_pic_num_x]
            status_name = "正常" if status_id == 0 else "异常" + '(' + status_id_name[str(status_id)] + ')'
            camera_type: CameraType = CameraType.query.order_by(func.random()).limit(1).all()[0]
            camera_business: CameraBusiness = CameraBusiness.query.order_by(func.random()).limit(1).all()[0]
            camera_ip = '.'.join([str(random.randint(1, 254)) for _ in range(4)])
            return {'normal_picture': pic_0["path"], 'current_picture': pic_x["path"], 'status_name': status_name,
                    'camera_type': camera_type.name, 'camera_businesses': camera_business.name,
                    'camera_businesses_telephone': camera_business.telephone, 'camera_ip': camera_ip}
        except Exception:
            raise


def write_scene_json(path):
    scene_json_file = os.path.join(path, "scene_category.json")
    categories = ["0", "1", "2", "3", "4"]
    scenes_category = {c: [] for c in categories}
    for root, dirs, files in os.walk(path):
        sp1 = os.path.split(root)
        sp2 = os.path.split(sp1[0])
        if sp1[-1].startswith('normal') and os.listdir(root):
            scenes_category["0"].append(sp2[-1])
        elif sp1[-1].startswith('black') and os.listdir(root):
            scenes_category["1"].append(sp2[-1])
        elif sp1[-1].startswith('gray') and os.listdir(root):
            scenes_category["2"].append(sp2[-1])
        elif sp1[-1].startswith('shelter') and os.listdir(root):
            scenes_category["3"].append(sp2[-1])
        elif sp1[-1].startswith('shift') and os.listdir(root):
            scenes_category["4"].append(sp2[-1])
    with open(scene_json_file, 'w') as f:
        json.dump(scenes_category, f)


def write_picture_json(path):
    picture_category_file = os.path.join(path, "picture_category.json")
    scenes = os.listdir(path)
    picture_json_data = {s: {"0": [], "1": [], "2": [], "3": [], "4": []} for s in scenes}
    url = '/' + SimulationDName + '/' + SimulationCameraDName
    for root, dirs, files in os.walk(path):
        for f in files:
            sp1 = os.path.split(root)
            sp2 = os.path.split(sp1[0])
            if sp1[-1].startswith("normal"):
                picture_json_data[sp2[-1]]["0"].\
                    append({"name": f, "path": url + '/' + sp2[-1] + '/' + sp1[-1] + '/' + f})
            elif sp1[-1].startswith("black"):
                picture_json_data[sp2[-1]]["1"]. \
                    append({"name": f, "path": url + '/' + sp2[-1] + '/' + sp1[-1] + '/' + f})
            elif sp1[-1].startswith("gray"):
                picture_json_data[sp2[-1]]["2"]. \
                    append({"name": f, "path": url + '/' + sp2[-1] + '/' + sp1[-1] + '/' + f})
            elif sp1[-1].startswith("shelter"):
                picture_json_data[sp2[-1]]["3"]. \
                    append({"name": f, "path": url + '/' + sp2[-1] + '/' + sp1[-1] + '/' + f})
            elif sp1[-1].startswith("shift"):
                picture_json_data[sp2[-1]]["4"]. \
                    append({"name": f, "path": url + '/' + sp2[-1] + '/' + sp1[-1] + '/' + f})
    with open(picture_category_file, 'w') as f:
        json.dump(picture_json_data, f)


scenes_json = None
picture_json = None
before_time = None


def load(path):
    write_picture_json(path)

    write_scene_json(path)

    global scenes_json
    global picture_json
    global before_time
    scenes_json = json.load(open(
        os.path.join(path, "scene_category.json"), 'rb'))
    picture_json = json.load(open(
        os.path.join(path, 'picture_category.json'), 'rb'))
    before_time = get_dir_time(path)


def get_dir_time(path):
    time = 0
    for root, dirs, files in os.walk(path):
        time += os.stat(root).st_mtime
    return time


load(DataDirectoryPath.get_simulation_camera_path())


if __name__ == '__main__':
    demo = CaseCameraMonitorDemoService.get(4)
    CaseCameraMonitorDemoService().map_to_mysql()
