from DAAQS import OpenAQData, gen_radial_coordinates
from DAAQS import outlier_station_plot

import numpy as np
import operator

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA as sklearnPCA

from pyod.models.knn import KNN
from pyod.models.copod import COPOD
from pyod.models.lscp import LSCP
from pyod.models.lof import LOF
from pyod.models.so_gaal import SO_GAAL
from pyod.models.pca import PCA

from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize


def read_data(date, span):
    pass


day = "2019-01-15"
# year = " 2020"
span = 0
# locations = ["London Bloomsbury", "官园", "US Diplomatic Post: New Delhi"]

openaq = OpenAQData(day, span = span, parameter="pm25")
openaq.sort_dict()

values= []
oaq = openaq.data_dict["US Diplomatic Post: New Delhi"] 
center = [oaq[0].lat, oaq[0].lon]
# print (oaq[0].lat, oaq[0].lon)
# print (type(openaq.data_dict))


nearby_locations = []
nearby_locations_lat = []
nearby_locations_lon = []
delta = 0.75

def sorting(oaq):
    oaq.sort(key=operator.attrgetter("time"))
    return oaq

def average_time(oaq, time_range = 3):

    average_time_range_value = []

    values = [[] for _ in range(8)]

    for each in oaq:
        
        i =  each.time.hour//3
   
        if each.parameter == "pm25" and each.time.day==15:
            values[i].append(each.value)


    average_time_range_value = [(sum(each_period)/len(each_period)) if len(each_period)!=0 else 0.01 for each_period in values ]
    
    return average_time_range_value

    # values = []    
    # while(start_time < 24):
    #     for each in oaq:
    #         if start_time <= each.time.hour < start_time + time_range and each.parameter == "pm25":
    #             values.append(each.value)
                
    #     average_time_range_value.append(sum(values)/(len(values)+1))

    #     start_time += time_range

    # print(f"Average value is {average_time_range_value}")

    # return average_time_range_value


for key, value in openaq.data_dict.items():
    if (oaq[0].lat + delta > value[0].lat > oaq[0].lat - delta and oaq[0].lon + delta > value[0].lon > oaq[0].lon - delta):
        nearby_locations.append(value[0].location)
        nearby_locations_lat.append(value[0].lat)
        nearby_locations_lon.append(value[0].lon)

print(nearby_locations)

# location = nearby_locations[0]
# oaq_location  =  openaq.data_dict[location]
# print(f"Location is {location}")
# oaq_location = sorting(oaq)
# list_val = []
# for each in oaq_location:
#     if each.parameter == "pm25":
#         list_val.append(each.value)

# print(f"number of datapoint {len(list_val)}")
# print(f"Oaq values are {list_val}")

# oaq_sorted = sorting(oaq_location)
# print(f"Average time {average_time(oaq_sorted)}")

final_average_time_loc = []
for loc in nearby_locations:
    oaq_loc = openaq.data_dict[loc]
    # for each in oaq_loc:
    #     print(f"Oaq value is {each.value}")
    oaq_sorted = sorting(oaq_loc)

    final_average_time_loc.append(average_time(oaq_sorted))

    
print (len(final_average_time_loc))


'''
for each in oaq:
    if each.parameter == "pm25":
        values.append(each.value)

difference_values = [values[i] - values[i-1] for i in range(1,len(values))]
'''

X_train = np.array(final_average_time_loc)


clf_1_name = 'KNN'
clf_1 = KNN()
clf_1.fit(X_train)

# get the prediction labels and outlier scores of the training data
y_train_pred_1 = clf_1.labels_  # binary labels (0: inliers, 1: outliers)
# y_train_scores = clf_1.decision_scores_  # raw outlier scores

# print ((difference_values, values, y_train_pred, y_train_scores))

print (list(y_train_pred_1))

clf_2_name = 'COPOD'
clf_2 = COPOD()
clf_2.fit(X_train)

# get the prediction labels and outlier scores of the training data
y_train_pred_2 = clf_2.labels_  # binary labels (0: inliers, 1: outliers)
# y_train_scores = clf.decision_scores_  #

print (list(map(int,y_train_pred_2)))


clf_3_name = 'LSCP'
detector_list = [LOF(n_neighbors=3), LOF(n_neighbors=5),
                    LOF(n_neighbors=7), LOF(n_neighbors=10)]
clf_3 = LSCP(detector_list, random_state=42)
clf_3.fit(X_train)

y_train_pred_3 = clf_3.labels_ 

print (list(y_train_pred_3))

clf_4_name = 'PCA'
clf_4 = PCA(n_components=3)
clf_4.fit(X_train)

y_train_pred_4 = clf_4.labels_

print (list(y_train_pred_4))

def outliers_plot(prediction):

    outliers_index = []
    for i in range(len(prediction)):
        if prediction[i]==1:
            outliers_index.append(i)


    # outliers_index = [prediction.index(i) for i in prediction if i==1]
    return outliers_index

outliers_index_1 = outliers_plot((y_train_pred_3).tolist())
print (outliers_index_1)

# contamination = 0.1  # percentage of outliers

# # train SO_GAAL detector
# clf_5_name = 'SO_GAAL'
# clf_5 = SO_GAAL(contamination=contamination)
# clf_5.fit(X_train)

# # get the prediction labels and outlier scores of the training data
# y_train_pre_5 = clf_5.labels_  

# print (list(y_train_pre_5))

# print (X_train)

X_train_normalized = (X_train - X_train.min())/(X_train.max() - X_train.min())

# print (X_train_normalized)


# pca = sklearnPCA(n_components=2) #2-dimensional PCA
# transformed = pd.DataFrame(pca.fit_transform(X_train_normalized))

# outliers_x = [transformed[0][i] for i in outliers_index_1]
# outliers_y = [transformed[1][i] for i in outliers_index_1]
# final_outliers = [i for i in zip(outliers_x, outliers_y)]

# plt.scatter(transformed[1], transformed[0], label = 'Non Outliers', c='red')
# plt.scatter(final_outliers[1], final_outliers[0], label = 'Outliers', c='black')

# plt.legend()
# plt.show()
# plt.savefig('plot_AirQS.png')



flatten_values = np.array(final_average_time_loc).flatten().tolist()
print (len(flatten_values))

outliers = [final_average_time_loc[i] for i in outliers_index_1]
print (outliers)




flatten_outliers = np.array(outliers).flatten().tolist()


def time_average_plot( final_average_time_loc, outliers, name = "PCA"):

    index=[]
    for i in range(len(final_average_time_loc)):
        for i in range(8):
            index.append(i)

    index_outlier=[]

    for i in range(8):
        index_outlier.append(i)

    flatten_values = np.array(final_average_time_loc).flatten().tolist()
    fig, ax = plt.subplots(1,1, figsize = (10,5))
    ax.scatter(index, flatten_values,label = 'Non Outliers', c='red')  

    for i in range(len(outliers)):
        ax.plot(index_outlier,outliers[i], label = 'Outliers')
    ax.set_ylim(0,500)
    ax.set_xlabel("3 hours time index")
    ax.legend()

    plt.savefig("plots/AirQS_"+name+".png")

time_average_plot(final_average_time_loc, outliers)

# plt.scatter(index, flatten_values,label = 'Non Outliers', c='red')

# for i in range(len(outliers)):
    
#     plt.plot(index_outlier,outliers[i], label = 'Outliers')

# plt.ylim(0,500)
# # plt.scatter(final_outliers[1], final_outliers[0], label = 'Outliers', c='black')

# plt.legend()
# plt.show()
# plt.savefig('plot_AirQS_PCA.png')

# lat_class = [nearby_locations_lat[i] for i in outliers_index_1]
# lon_class = [nearby_locations_lon[i] for i in outliers_index_1]

# k_value = []
# for i in range(len(nearby_locations_lat)):
#     if i in outliers_index_1:
#         k = 1
#     else:
#         k = 0

#     k_value.append(k)

# lat_lon_class = [i for i in zip(nearby_locations_lat, nearby_locations_lon, k_value)]

# outlier_station_plot(center, lat_lon_class, factor=1, fpath='plots/outlier_plot_1_lscp.png')
