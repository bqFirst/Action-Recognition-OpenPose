import pandas as pd
from sklearn.pipeline import Pipeline


from app.main.modeling import IPreProcessing, ModelInfo, IModelPredict
from app.main.services.core.data.project_file_operator import ProjectDataOperator


# Do not modify inheritance relationships, parameters and return value
# If you need more preprocessing measure, copy the following class and rename it
class PreProcessing(IPreProcessing):

    def __init__(self):
        super(PreProcessing, self).__init__()

    def fit(self, X, y=None, **fit_params):
        ...
        return self

    def transform(self, data: pd.DataFrame):
        ...
        return data


# Do not modify the function name, return value and pass only default parameters
def build_and_train():
    # Output interface, using set_info method to get custom info
    # mi.set_info(key='name', value='The message you want')
    mi = ModelInfo()

    # This entity object is used to read the data of the current project
    data_operator = ProjectDataOperator(project_path='')
    data = data_operator.get_original_data(src='', sql=None)

    # PreProcessing() should be the first pipe
    pipe = Pipeline([('my_process', PreProcessing()),
                     ])
    pipe.fit(data, y=None)

    return mi, pipe


# Do not modify the class name, inheritance relationships
class ModelPredict(IModelPredict):

    def predict(self, data):
        # self.model was the model trained and returned by the func build and train.
        # the parameter data is the data used to be predicted by self.model. If it was pictures, it will be transformed
        # into a list type which contains several pictures.
        result = self.model.predict(data)
        return result
