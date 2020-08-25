#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/14 10:52
# @Author : wangweimin
# @File   : data_path.py
# @Desc   :

"""
文件目录改动
1、增加临时文件夹 —— 2020/01/02
2、所有表格数据存储在同一目录，包括上传的和从数据库查询的 —— 2020/01/19

"""

import os
import shutil

CurPath = os.path.abspath(os.path.dirname(__file__))
PackagePath = os.path.split(CurPath)[0]

LogDName = 'log'
DataDName = 'data'  # 数据根目录名
AppDName = 'app'
ConfDName = 'conf'
DataFileDName = 'data_file'  # 数据文件，包括上传的数据文件以及数据库查询的数据
# DataSourceDName = 'data_source'  # 数据源根目录名
DataOverviewDName = 'data_overview'  # 数据概览根目录名
ApplicationDName = 'application'  # 应用结果数据根目录名
ModelDName = 'model'  # 模型文件根目录名
ModelInfoDName = 'info'  # 模型输出结果根目录名
ModelSrcDName = 'src'  # 模型源码文件根目录名
ModelFileDName = 'file'  # 模型文件根目录名
ModelDataFormatDName = 'format'  # 模型数据格式根目录名
ModelPackageDName = 'package'
ProjectDName = 'project'  # 工程过程数据根目录名
DockerDName = 'docker'
DockerImageDName = 'image'
PictureDName = 'picture'
VideoDName = 'video'
OriginalPictureDName = 'original'
ThumbnailDName = 'thumbnail'
# DatabaseDName = 'database'
CaseDName = 'case'
TempDName = 'temp'

SimulationDName = "simulation"
SimulationHumanDName = "human_intrusion"
SimulationCameraDName = "camera_monitor"


class DataDirectoryPath(object):
    DataRootPath: str = os.path.join(PackagePath, DataDName)
    AppRootPath: str = os.path.join(PackagePath, AppDName)
    ConfRootPath: str = os.path.join(PackagePath, ConfDName)
    DataFilePath: str = os.path.join(DataRootPath, DataFileDName)
    # DataSourceFilePath: str = os.path.join(DataRootPath, DataSourceDName)
    DataOverviewPath: str = os.path.join(DataRootPath, DataOverviewDName)
    ProjectProcessFilePath: str = os.path.join(DataRootPath, ProjectDName)
    ApplicationResultFilePath: str = os.path.join(DataRootPath, ApplicationDName)
    ModelPath = os.path.join(DataRootPath, ModelDName)
    ModelFilePath: str = os.path.join(ModelPath, ModelFileDName)
    ModelSrcPath: str = os.path.join(ModelPath, ModelSrcDName)
    ModelInfoPath: str = os.path.join(ModelPath, ModelInfoDName)
    ModelDataFormatPath: str = os.path.join(ModelPath, ModelDataFormatDName)
    ModelPackagePath: str = os.path.join(ModelPath, ModelPackageDName)
    LogPath: str = os.path.join(PackagePath, LogDName)
    DockerPath: str = os.path.join(DataRootPath, DockerDName)
    DockerImagePath: str = os.path.join(DockerPath, DockerImageDName)
    DistributedPath: str = None
    PicturePath: str = os.path.join(DataRootPath, PictureDName)
    VideoPath: str = os.path.join(DataRootPath, VideoDName)
    OriginalPicturePath: str = os.path.join(PicturePath, OriginalPictureDName)
    ThumbnailPath: str = os.path.join(PicturePath, ThumbnailDName)
    # DatabasePath: str = os.path.join(DataRootPath, DatabaseDName)
    CasePath: str = os.path.join(DataRootPath, CaseDName)
    TempPath: str = os.path.join(DataRootPath, TempDName)

    SimulationPath: str = os.path.join(DataRootPath, SimulationDName)
    SimulationHumanPath: str = os.path.join(SimulationPath, SimulationHumanDName)
    SimulationCameraPath: str = os.path.join(SimulationPath, SimulationCameraDName)

    @classmethod
    def init(cls) -> None:
        # cls.DataRootPath = root_path or os.path.join(PackagePath, DataDName)
        cls.make_dirs(cls.DataRootPath)

        cls.make_dirs(cls.DataFilePath)
        # cls.DataSourceFilePath = os.path.join(cls.DataRootPath, DataSourceDName)
        # cls.make_dirs(cls.DataSourceFilePath)

        # cls.DataOverviewPath = os.path.join(cls.DataRootPath, DataOverviewDName)
        cls.make_dirs(cls.DataOverviewPath)

        # cls.ProjectProcessFilePath = os.path.join(cls.DataRootPath, ProjectDName)
        cls.make_dirs(cls.ProjectProcessFilePath)

        # cls.ApplicationResultFilePath = os.path.join(cls.DataRootPath, ApplicationDName)
        cls.make_dirs(cls.ApplicationResultFilePath)

        # model_path = os.path.join(cls.DataRootPath, 'model')
        cls.make_dirs(cls.ModelPath)
        # cls.ModelFilePath = os.path.join(cls.ModelPath, ModelFileDName)
        cls.make_dirs(cls.ModelFilePath)
        # cls.ModelInfoPath = os.path.join(cls.ModelPath, ModelInfoDName)
        cls.make_dirs(cls.ModelInfoPath)
        # cls.ModelSrcPath = os.path.join(cls.ModelPath, ModelSrcDName)
        cls.make_dirs(cls.ModelSrcPath)
        # cls.ModelDataFormatPath = os.path.join(cls.ModelPath, ModelDataFormatDName)
        cls.make_dirs(cls.ModelDataFormatPath)

        cls.make_dirs(cls.ModelPackagePath)

        # cls.LogPath = os.path.join(cls.PackagePath, LogDName)
        cls.make_dirs(cls.LogPath)

        # cls.DockerPath = os.path.join(cls.DataRootPath, DockerDName)
        cls.make_dirs(cls.DockerPath)

        # cls.DockerImagePath = os.path.join(cls.DockerPath, DockerImageDName)
        cls.make_dirs(cls.DockerImagePath)

        # cls.PicturePath = os.path.join(cls.DataRootPath, PictureDName)
        cls.make_dirs(cls.PicturePath)

        cls.make_dirs(cls.VideoPath)
        # cls.OriginalPicturePath = os.path.join(cls.PicturePath, OriginalPictureDName)
        cls.make_dirs(cls.OriginalPicturePath)
        # cls.ThumbnailPath = os.path.join(cls.PicturePath, ThumbnailDName)
        cls.make_dirs(cls.ThumbnailPath)

        # cls.DatabasePath = os.path.join(cls.DataRootPath, DatabaseDName)
        # cls.make_dirs(cls.DatabasePath)

        cls.make_dirs(cls.CasePath)

        cls.make_dirs(cls.TempPath)

        cls.make_dirs(cls.SimulationHumanPath)
        cls.make_dirs(cls.SimulationCameraPath)

        cls.DistributedPath: str = ''

    @classmethod
    def get_package_path(cls) -> str:
        return PackagePath

    @classmethod
    def get_data_path(cls) -> str:
        return cls.DataRootPath

    @classmethod
    def get_app_path(cls) -> str:
        return cls.AppRootPath

    @classmethod
    def get_conf_path(cls) -> str:
        return cls.ConfRootPath

    @classmethod
    def get_data_source_path(cls) -> str:
        """
        获取数据源路径，使用data_file代替
        :return:
        """
        return cls.DataFilePath

    @classmethod
    def get_data_overview_path(cls) -> str:
        """
        获取数据概览路径
        :return:
        """
        return cls.DataOverviewPath

    @classmethod
    def get_log_path(cls) -> str:
        """
        获取日志路径
        :return:
        """
        return cls.LogPath

    @classmethod
    def get_model_file_path(cls) -> str:
        """
        获取模型文件路径
        :return:
        """
        return cls.ModelFilePath

    @classmethod
    def get_project_path(cls) -> str:
        """
        获取工程过程数据路径
        :return:
        """
        return cls.ProjectProcessFilePath

    @classmethod
    def get_application_path(cls) -> str:
        """
        获取应用结果数据的路径
        """
        return cls.ApplicationResultFilePath

    @classmethod
    def get_model_src_path(cls) -> str:
        """
        获取项目模型源码文件路径
        """
        return cls.ModelSrcPath

    @classmethod
    def get_model_info_path(cls) -> str:
        """
        获取模型信息路径
        """
        return cls.ModelInfoPath

    @classmethod
    def get_model_data_format_path(cls) -> str:
        """
        获取模型数据格式路径
        """
        return cls.ModelDataFormatPath

    @classmethod
    def get_model_package_path(cls) -> str:
        """
        获取模型打包路径
        """
        return cls.ModelPackagePath

    @classmethod
    def get_docker_path(cls) -> str:
        """
        获取Docker路径
        :return:
        """
        return cls.DockerPath

    @classmethod
    def get_docker_image_path(cls) -> str:
        """
        获取docker镜像路径
        :return:
        """
        return cls.DockerImagePath

    @classmethod
    def get_picture_path(cls) -> str:
        """
        获取图片路径
        :return:
        """
        return cls.PicturePath

    @classmethod
    def get_video_path(cls) -> str:
        """
        获取视频路径
        :return:
        """
        return cls.VideoPath

    @classmethod
    def get_original_picture_path(cls) -> str:
        """
        获取原始图片路径
        :return:
        """
        return cls.OriginalPicturePath

    @classmethod
    def get_thumbnail_path(cls) -> str:
        """
        获取缩略图路径
        :return:
        """
        return cls.ThumbnailPath

    @classmethod
    def get_database_path(cls) -> str:
        """
        获取数据库数据路径，使用data_file代替
        :return:
        """
        return cls.DataFilePath

    @classmethod
    def get_temp_path(cls) -> str:
        """
        获取临时数据文件夹
        :return:
        """
        return cls.TempPath

    @classmethod
    def get_distributed_path(cls) -> str:
        return cls.DistributedPath

    @classmethod
    def get_module_path(cls) -> str:
        return os.path.join(DataDName, ModelDName, ModelSrcDName)

    @classmethod
    def get_case_path(cls) -> str:
        return cls.CasePath

    @classmethod
    def get_simulation_camera_path(cls) -> str:
        return cls.SimulationCameraPath

    @classmethod
    def get_simulation_human_path(cls) -> str:
        return cls.SimulationHumanPath

    @classmethod
    def make_dirs(cls, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass

    @classmethod
    def rm_dirs(cls, path: str, is_force: bool = True):
        if os.path.exists(path):
            if is_force:
                shutil.rmtree(path)
            else:
                os.rmdir(path)

    @classmethod
    def rm_file(cls, file):
        if os.path.exists(file):
            os.remove(file)
