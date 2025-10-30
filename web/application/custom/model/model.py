from abc import ABC, abstractmethod
import pickle
import os




class Model(ABC):

    models_path = 'application/models'

    def __init__(self, pickle_name) -> None:
        
        self.model = self.__load_pickle(pickle_name)


    def __load_pickle(self, pickle_name):

        pickle_path = os.path.join(self.models_path, pickle_name)
        with open(pickle_path, 'rb') as f:
            model = pickle.load(f)

        return model
    
    @abstractmethod
    def _inference(self) -> dict:
        ...