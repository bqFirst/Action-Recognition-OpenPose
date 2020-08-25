#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/3 0003 18:44
# @Author : wangw
# @File   : baidu_map.py
# @Desc   :

import requests
import json
import numpy as np
import os

# from app import db
from flask_sqlalchemy import SQLAlchemy

from app.models import CameraDistribution

db = SQLAlchemy()

# ak = 'oBLUllE25FshpUu3f4PBSb30r2haQ6iB'  # ak2
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


class BaiduMap(object):
    def __init__(self):
        pass

    def count_street(self):

        area_street_nums = {}
        for root, dirs, files in os.walk('./'):
            for file in files:
                if file.split('.')[-1] == 'json':
                    with open(os.path.join(root, file), 'rb') as f:
                        area_data = json.load(f)
                        street = set()
                        for e in area_data['results']:
                            street.add(e['name'])
                        # area_street_nums[area_data['area']] = area_data['area']
                        nums = {s: 0 for s in street}
                        self.assign_street_nums(config['area'][area_data['area']], street, nums, config['area'][area_data['area']])
                        area_street_nums.update(nums)

        return area_street_nums

    def get(self):
        # self.get_from_api()
        area_street_nums = self.count_street()
        for root, dirs, files in os.walk('./'):
            for file in files:
                if file.split('.')[-1] == 'json':
                    with open(os.path.join(root, file), 'rb') as f:
                        area_data = json.load(f)
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

                            db.session.commit()
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


if __name__ == '__main__':
    file = 'address_location.json'

    # BaiduMap.get_from_api()
    BaiduMap().get()
    #
    # r = BaiduMap.load('增城区.json')
    # print(r)