import numpy as np
from pyod.models.knn import KNN
from pyod.models.copod import COPOD
from pyod.models.lscp import LSCP
from pyod.models.pca import PCA
from pyod.models.lof import LOF



class Model(object):
    def __init__(self, c_dict, o_dict):
        self.c_dict = c_dict
        self.o_dict = o_dict

        self.center_o = []

        self.X_o = []
        self.X_c = []

        x_o = []
        for _, val_o in self.o_dict.items():
            x_o.append(val_o[:8])
            if self._in_center(val_o):
                self.center_o.append(True)
            else:
                self.center_o.append(False)

        self.X_o = self._stack(x_o)

        for _, val_o in self.o_dict.items():
            if self._in_center(val_o):
                x_c = []
                for _, val_c in self.c_dict.items():
                    x_c.append(val_c[:8])
                if bool(self.c_dict):
                    x_c.append(val_o[:8])
                    self.X_c.append(self._stack(x_c))
                    
    # Dictionary from python 3.6 have insertion order
    def _in_center(self, val):
            return val[9]["lat_lon_index"] == val[10]["center_index"]

    def _stack(self, x):
        if len(x) >0:
            return np.stack(x)
        else:
            return []

    def pred_KNN(self, k =5, comp_with = "openaq"):
        ## hyperparameters for KNN is tuned here
        # if self.bool_o_dict == True:    
        self.comp_with = comp_with
        
        if comp_with == "openaq":
            if self.X_o == []:
                pred = []
            elif self.X_o.shape[0] > k:
                self.clf = KNN(n_neighbors=k)
                self.clf.fit(self.X_o)
                pred = self.clf.labels_
            elif self.X_o.shape[0] > 2: 
                # print(f"The value of k is changed from {k} to {self.X_o.shape[0]-1}")
                k = self.X_o.shape[0]-1
                self.clf = KNN(n_neighbors=k)
                self.clf.fit(self.X_o)
                pred = self.clf.labels_
            else:
                pred = []
            #A_location, B_location, C_location = self.pred_location(pred)
        
        elif comp_with == "cams":
            pred = []
            for each_X in self.X_c:
                # if each_X exists then it will have a shape of (10,8)
                self.clf = KNN(n_neighbors=k)
                self.clf.fit(each_X)
                pred.append(self.clf.labels_[-1])
            
        A_location, B_location, C_location = self.pred_location(pred)
        
        return A_location, B_location, C_location    
        
    def pred_COPOD(self, comp_with = "openaq"):

        self.comp_with = comp_with
        
        if comp_with == "openaq":
            if self.X_o == []:
                pred = []
            else:
                self.clf = COPOD()
                self.clf.fit(self.X_o)
                pred = self.clf.labels_
            
        elif comp_with == "cams":
            pred = []
            for each_X in self.X_c:
                self.clf = COPOD()
                self.clf.fit(each_X)
                pred.append(self.clf.labels_[-1])
            
        A_location, B_location, C_location = self.pred_location(pred)
        
        return A_location, B_location, C_location    


    # def pred_LSCP(self, k, comp_with = "openaq"):
    #     ## hyperparameters for KNN is tuned here
    #     ## number of data points cannot be lesser than the local_regio_size (5 in this case)
    #     self.comp_with = comp_with
        
    #     detector_list = [LOF(n_neighbors=3), LOF(n_neighbors=5), LOF(n_neighbors=7)]
        
    #     if comp_with == "openaq":
    #         if self.X_o == []:
    #             pred = []
    #         elif self.X_o.shape[0] > k:
    #             self.clf = LSCP(detector_list, random_state=42, local_region_size=k)
    #             try:
    #                 self.clf.fit(self.X_o)
    #             except:
    #                 print(self.X_o.shape)
    #             pred = self.clf.labels_
    #         elif self.X_o.shape[0] > 3: 
    #             # print(f"The value of k is changed from {k} to {self.X_o.shape[0]-1}")
    #             k = self.X_o.shape[0]-1
    #             self.clf = LSCP(detector_list, random_state=42, local_region_size=k)
    #             try:
    #                 self.clf.fit(self.X_o)
    #             except:
    #                 print(self.X_o.shape)
    #             pred = self.clf.labels_
    #         else:
    #             pred = []

    #     elif comp_with == "cams":
    #         pred = []
    #         for each_X in self.X_c:
    #             self.clf = LSCP(detector_list, random_state=42, local_region_size=k)
    #             self.clf.fit(each_X)
    #             pred.append(self.clf.labels_[-1])           
            
    #     A_location, B_location, C_location = self.pred_location(pred)
        
    #     return A_location, B_location, C_location  

    def pred_PCA(self, n_comp=3, comp_with = 'openaq'):
        
        ## hyperparameters for KNN is tuned here
        # Number of samples must be greater than the n_components (3 in this case). It can be made 0.3 to make it work

        self.comp_with = comp_with
        
        if comp_with == "openaq":
            if self.X_o == []:
                pred = []
            elif self.X_o.shape[0] > n_comp:
                self.clf = PCA(n_components= n_comp)
                self.clf.fit(self.X_o)
                pred = self.clf.labels_
            elif self.X_o.shape[0] > 2: 
                # print(f"The value of k is changed from {k} to {self.X_o.shape[0]-1}")
                n_comp = self.X_o.shape[0]-1
                self.clf = PCA(n_components= n_comp)
                self.clf.fit(self.X_o)
                pred = self.clf.labels_
            else:
                pred = []
            
        elif comp_with == "cams":
            pred = []
            for each_X in self.X_c:
                self.clf = PCA(n_components= n_comp)
                self.clf.fit(each_X)
                pred.append(self.clf.labels_[-1])
            
        A_location, B_location, C_location = self.pred_location(pred)
       
        return A_location, B_location, C_location


    def pred_location(self, pred):
        if pred == [] :
            counter = 0
            A_location = []
            B_location = []
            C_location = []
            
            for key, _ in self.o_dict.items():
                if self.center_o[counter] == True:
                    C_location.append([key, self.o_dict[key][-3]["coordinates"]])
                    counter+=1
        else:
            counter  = 0
            counter_center = 0
            counter_pred =0 
            A_location = [] 
            B_location = []
            C_location = []

            if self.comp_with == "cams":
                for key, _ in self.o_dict.items():
                    if self.center_o[counter_center] == True:
                        if pred[counter_pred] == 1 :
                            A_location.append([key, self.o_dict[key][-3]["coordinates"]])
                        else:
                            B_location.append([key, self.o_dict[key][-3]["coordinates"]])
                        counter_pred+=1
                        counter_center+=1
                    else:
                        counter_center+=1

            
            elif self.comp_with == "openaq":
                for key, _ in self.o_dict.items():
                    if self.center_o[counter] == True:
                        if pred[counter] == 1 :
                            A_location.append([key, self.o_dict[key][-3]["coordinates"]])
                        else:
                            B_location.append([key, self.o_dict[key][-3]["coordinates"]])
                    counter+=1  
        

            
        return A_location, B_location, C_location
    