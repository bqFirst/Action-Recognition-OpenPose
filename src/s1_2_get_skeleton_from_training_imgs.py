#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/27 0027 16:13
# @Author : wangw
# @File   : s1_2_get_skeleton_from_training_imgs.py
# @Desc   :

'''
Read training images based on `valid_images.txt` and then detect skeletons.

In each image, there should be only 1 person performing one type of action.
Each image is named as 00001.jpg, 00002.jpg, ...

An example of the content of valid_images.txt is shown below:

    jump_03-12-09-18-26-176
    58 680

    jump_03-13-11-27-50-720
    65 393

    kick_03-02-12-36-05-185
    54 62
    75 84

The two indices (such as `56 680` in the first `jump` example)
represents the starting index and ending index of a certain action.

Input:
    SRC_IMAGES_DESCRIPTION_TXT
    SRC_IMAGES_FOLDER

Output:
    DST_IMAGES_INFO_TXT
    DST_DETECTED_SKELETONS_FOLDER
    DST_VIZ_IMGS_FOLDER
'''

import cv2
import yaml
import numpy as np


if True:  # Include project path
    import sys
    import os

    ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../"
    CURR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
    sys.path.append(ROOT)

    from utils.lib_openpose import SkeletonDetector
    from utils.lib_tracker import Tracker
    from utils.lib_skeletons_io import ReadValidImagesAndActionTypesByTxt
    import utils.lib_commons as lib_commons

    from pose.estimator import TfPoseEstimator
    from pose.networks import get_graph_path
    from utils.sort import Sort

    from PIL import Image
    from yolo import YOLO


def par(path):  # Pre-Append ROOT to the path if it's not absolute
    return ROOT + path if (path and path[0] != "/") else path


# -- Settings


cfg_all = lib_commons.read_yaml(ROOT + "config/config.yaml")
cfg = cfg_all["s1_get_skeletons_from_training_imgs.py"]

IMG_FILENAME_FORMAT = cfg_all["image_filename_format"]
SKELETON_FILENAME_FORMAT = cfg_all["skeleton_filename_format"]

# Input
if True:
    SRC_IMAGES_DESCRIPTION_TXT = par(cfg["input"]["images_description_txt"])
    SRC_IMAGES_FOLDER = par(cfg["input"]["images_folder"])

# Output
if True:
    # This txt will store image info, such as index, action label, filename, etc.
    # This file is saved but not used.
    DST_IMAGES_INFO_TXT = par(cfg["output"]["images_info_txt"])

    # Each txt will store the skeleton of each image
    DST_DETECTED_SKELETONS_FOLDER = par(
        cfg["output"]["detected_skeletons_folder"])

    # Each image is drawn with the detected skeleton
    DST_VIZ_IMGS_FOLDER = par(cfg["output"]["viz_imgs_folders"])

# Openpose
if True:
    OPENPOSE_MODEL = cfg["openpose"]["model"]
    OPENPOSE_IMG_SIZE = cfg["openpose"]["img_size"]


# -- Functions


class ImageDisplayer(object):
    ''' A simple wrapper of using cv2.imshow to display image '''

    def __init__(self):
        self._window_name = "cv2_display_window"
        cv2.namedWindow(self._window_name)

    def display(self, image, wait_key_ms=1):
        cv2.imshow(self._window_name, image)
        cv2.waitKey(wait_key_ms)

    def __del__(self):
        cv2.destroyWindow(self._window_name)


def humans_to_skels_list(humans, img_size=None):
    ''' Get skeleton data of (x, y * scale_h) from humans.
    Arguments:
        humans {a class returned by self.detect}
        scale_h {float}: scale each skeleton's y coordinate (height) value.
            Default: (image_height / image_widht).
    Returns:
        skeletons {list of list}: a list of skeleton.
            Each skeleton is also a list with a length of 36 (18 joints * 2 coord values).
        scale_h {float}: The resultant height(y coordinate) range.
            The x coordinate is between [0, 1].
            The y coordinate is between [0, scale_h]
    '''
    skeletons = []
    NaN = 0

    scale_h = 1.0 * img_size[1] / img_size[0]

    for human in humans:
        skeleton = [NaN]*(18*2)
        for i, body_part in human.items(): # iterate dict
            idx = i
            skeleton[2*idx]=(body_part[0]-0.5) / img_size[0]
            skeleton[2*idx+1]=(body_part[1]-0.5) / img_size[1] * scale_h
        skeletons.append(skeleton)
    return skeletons, scale_h


# -- Main
if __name__ == "__main__":

    # -- Detector
    # skeleton_detector = SkeletonDetector(OPENPOSE_MODEL, OPENPOSE_IMG_SIZE)
    # multiperson_tracker = Tracker()

    poseEstimator = TfPoseEstimator(
        get_graph_path('mobilenet_thin'), target_size=(432, 368))
    tracker = Sort(20, 3)
    yolo = YOLO()

    # -- Image reader and displayer
    images_loader = ReadValidImagesAndActionTypesByTxt(
        img_folder=SRC_IMAGES_FOLDER,
        valid_imgs_txt=SRC_IMAGES_DESCRIPTION_TXT,
        img_filename_format=IMG_FILENAME_FORMAT)
    # This file is not used.
    images_loader.save_images_info(filepath=DST_IMAGES_INFO_TXT)
    img_displayer = ImageDisplayer()

    # -- Init output path
    os.makedirs(os.path.dirname(DST_IMAGES_INFO_TXT), exist_ok=True)
    os.makedirs(DST_DETECTED_SKELETONS_FOLDER, exist_ok=True)
    os.makedirs(DST_VIZ_IMGS_FOLDER, exist_ok=True)

    # -- Read images and process
    num_total_images = images_loader.num_images
    for ith_img in range(num_total_images):
        # -- Read image
        img, str_action_label, img_info = images_loader.read_image()
        img_disp = img.copy()

        # -- Detect
        # humans = skeleton_detector.detect(img)
        humans = poseEstimator.inference(img)
        img, joints, bboxes, xcenter, sk = TfPoseEstimator.get_skeleton(img, humans, imgcopy=False)

        # -- Draw
        # skeleton_detector.draw(img_disp, humans)
        poseEstimator.draw_humans(img_disp, humans)

        img_displayer.display(img_disp, wait_key_ms=1)

        # -- Get skeleton data and save to file

        height = img.shape[0]
        width = img.shape[1]

        skeletons, scale_h = humans_to_skels_list(joints, (width, height))
        # dict_id2skeleton = multiperson_tracker.track(
        #     skeletons)  # dict: (int human id) -> (np.array() skeleton)
        dict_id2skeleton = {}
        if bboxes:
            result = np.array(bboxes)
            det = result[:, 0:5]
            det[:, 0] = det[:, 0] * width
            det[:, 1] = det[:, 1] * height
            det[:, 2] = det[:, 2] * width
            det[:, 3] = det[:, 3] * height
            trackers = tracker.update(det)

            for d in range(len(trackers)):
                xmin = int(trackers[d][0])
                ymin = int(trackers[d][1])
                xmax = int(trackers[d][2])
                ymax = int(trackers[d][3])
                label = int(trackers[d][4])
                # yolo detect person
                img_yolo = Image.fromarray(img[..., ::-1])  # bgr to rgb
                img_cut = img_yolo.crop((xmin, xmax, ymin, ymax))
                try:
                    boxs_yolo = yolo.detect_image(img_cut)
                except:
                    print("detect not person")

                try:
                    dict_id2skeleton[label] = np.asarray(skeletons[d])
                except:
                    continue

        skels_to_save = [img_info + skeleton.tolist()
                         for skeleton in dict_id2skeleton.values()]

        # -- Save result

        # Save skeleton data for training
        filename = SKELETON_FILENAME_FORMAT.format(ith_img)
        lib_commons.save_listlist(
            DST_DETECTED_SKELETONS_FOLDER + filename,
            skels_to_save)

        # Save the visualized image for debug
        filename = IMG_FILENAME_FORMAT.format(ith_img)
        cv2.imwrite(
            DST_VIZ_IMGS_FOLDER + filename,
            img_disp)

        print(f"{ith_img}/{num_total_images} th image "
              f"has {len(skeletons)} people in it")

    print("Program ends")
