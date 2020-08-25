#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/6 14:34
# @Author : wangweimin
# @File   : i_model.py
# @Desc   :

from abc import abstractmethod
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


AllowedFormat = ['int64', 'float64']


class IPreProcessing(BaseEstimator, TransformerMixin):
    """Do not modify inheritance relationships, parameters and return value
    """

    def __init__(self):
        self.__ramadi_data_format_extracted: dict = dict()
        self.__fit_control: bool = False
        self.__transform_control: bool = False

    @staticmethod
    def __ramadi_get_format(data: pd.DataFrame):
        # data_drop: pd.DataFrame = data.dropna(how='all', axis=1)
        # if data_drop.empty:
        #     return {}
        # data_drop_na: pd.DataFrame = data_drop.dropna(how='any', axis=0)
        # if not data_drop_na.empty:
        #     data_dict: dict = data_drop_na[0:1].to_dict(orient='record')[0]
        #     return dict([(k, type(v).__name__) for k, v in data_dict.items()])
        # else:
        #     format_ = dict()
        #     columns = data_drop.columns.tolist()
        #     for column in columns:
        #         data_temp = data_drop[column].dropna(how='any', axis=0)
        #         if not data_temp.empty:
        #             format_[column] = type(data_temp.values[0]).__name__
        #     return format_
        d_type = dict(data.dtypes)
        return dict([(k, str(v)) for k, v in d_type.items()])

    def __ramadi_extract_format(self, data: pd.DataFrame):
        self.__ramadi_data_format_extracted = self.__ramadi_get_format(data=data)

    def __ramadi_check_format(self, data: pd.DataFrame):
        data_format_extracted = self.__ramadi_get_format(data=data)
        for key, value in self.__ramadi_data_format_extracted.items():
            if key not in data_format_extracted:
                raise KeyError(
                    'The columns names of trained data are {}'.format(list(self.__ramadi_data_format_extracted.keys())))
            value_p = data_format_extracted[key]
            if value_p != value:
                if value_p in AllowedFormat and value in AllowedFormat:
                    continue
                raise TypeError('The data type {} that needed is \n{}'.format(type(self).__name__,
                                                                              self.__ramadi_data_format_extracted))

    @property
    def format(self):
        """the train data format after fit(train).
        """
        return self.__ramadi_data_format_extracted

    def __ramadi_fit(self, X, y=None, **fit_params):
        try:
            self.__ramadi_extract_format(X)
            self.__fit_control = True
            ramadi = self.fit(X=X, y=y, **fit_params)
        except Exception:
            raise
        finally:
            self.__fit_control = False
        return ramadi

    def __ramadi_transform(self, data: pd.DataFrame):
        try:
            self.__ramadi_check_format(data)
            self.__transform_control = True
            ramadi = self.transform(data=data)
        except Exception:
            raise
        finally:
            self.__transform_control = False
        return ramadi

    @abstractmethod
    def fit(self, X, y=None, **fit_params):
        """Fitting the Training dataset & calculating the required values from train
        """

        return self

    @abstractmethod
    def transform(self, data: pd.DataFrame):
        """Regular transform() that is a help for training, validation & testing datasets
           (NOTE: The operations performed here are the ones that we did prior to this cell)
        """

        return data

    def __getattribute__(self, item):
        if 'fit' == item and not self.__fit_control:
            return super(IPreProcessing, self).__getattribute__('_IPreProcessing__ramadi_fit')
        elif 'transform' == item and not self.__transform_control:
            return super(IPreProcessing, self).__getattribute__('_IPreProcessing__ramadi_transform')
        else:
            return super(IPreProcessing, self).__getattribute__(item)


class ModelInfo(object):

    def __init__(self):
        self.__info: dict = {}

    def set_info(self, key, value) -> None:
        self.__info[key] = value
        return

    @property
    def info(self) -> dict:
        return self.__info


class IModelPredict(object):

    def __init__(self, model):
        self.__model = model

    @property
    def model(self):
        return self.__model

    @abstractmethod
    def predict(self, data):
        pass
