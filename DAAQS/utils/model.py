import numpy as np
from pyod.models.knn import KNN
from pyod.models.copod import COPOD
from pyod.models.lscp import LSCP
from pyod.models.pca import PCA
from pyod.models.lof import LOF



class Model(object):
    def __init__(self, c_dict, o_dict, cams = True):
        self.c_dict = c_dict
        self.o_dict = o_dict
        self.cams = cams
        x = []
        if cams == True:
            for _, val in self.c_dict.items():
                x.append(val[:8])
        else:
            pass
        for _, val in self.o_dict.items():
            x.append(val[:8])
        
        self.bool_o_dict = bool(o_dict)
    
        self.X = np.stack(x)
    # Dictionary from python 3.6 have insertion order

    def pred_KNN(self, k =5):
        ## hyperparameters for KNN is tuned here
        # if self.bool_o_dict == True:    
        self.clf = KNN(n_neighbors=k)
        self.clf.fit(self.X)
        pred = self.clf.labels_
        return pred 

        #else:
            # pred = []
            # return pred   
    
    def pred_COPOD(self):
        ## hyperparameters for KNN is tuned here
        self.clf = COPOD()
        self.clf.fit(self.X)
        return self.clf.labels_ 

    def pred_LSCP(self):
        ## hyperparameters for KNN is tuned here
        detector_list = [LOF(n_neighbors=3), LOF(n_neighbors=5),
                    LOF(n_neighbors=7)]
        self.clf = LSCP(detector_list, random_state=42)
        self.clf.fit(self.X)
        return self.clf.labels_ 

    def pred_PCA(self):
        ## hyperparameters for KNN is tuned here
        self.clf = PCA(n_components=3)
        self.clf.fit(self.X)
        return self.clf.labels_ 

    def pred_location(self, pred):
        
        if pred == [] :
            outlier_location = []
            other_location = []
        else:
            counter  = 0
            outlier_location = [] 
            other_location = []

            for key, _ in self.c_dict.items():
                if pred[counter] == 1:
                    outlier_location.append([key, self.c_dict[key][-1]["coordinates"]])
                else:
                    other_location.append([key, self.c_dict[key][-1]["coordinates"]])
                counter+=1
            
            for key, _ in self.o_dict.items():
                if pred[counter] == 1:
                    outlier_location.append([key, self.o_dict[key][-1]["coordinates"]])
                else:
                    other_location.append([key, self.o_dict[key][-1]["coordinates"]])
                counter+=1
            
        return outlier_location, other_location
    