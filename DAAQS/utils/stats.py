import matplotlib.pylab as plt
from matplotlib import cm
import cartopy.io.img_tiles as cimgt
import cartopy.crs as ccrs

class Statistics(object):
    def __init__(self, parameter):

        self.parameter = parameter

        self.COPOD = "COPOD"
        self.KNN = "KNN"
        self.PCA = "PCA"

        self.cams = "cams"
        self.openaq = "openaq"

        self.data_C_c = self.read_output(self.parameter, self.COPOD, self.cams ) 
        self.data_K_c = self.read_output(self.parameter, self.KNN, self.cams )
        self.data_P_c = self.read_output(self.parameter, self.PCA, self.cams )

        self.data_C_o = self.read_output(self.parameter, self.COPOD, self.openaq )
        self.data_K_o = self.read_output(self.parameter, self.KNN, self.openaq )
        self.data_P_o = self.read_output(self.parameter, self.PCA, self.openaq )


    def compare_methods(self, threshold = 0.9, region = "Global", comp_with = "cams"):
        
        self.region = region

        self.comp_with = comp_with
        if region == "Europe":
            lat_max = 73 
            lat_min = 34
            lon_max = 40
            lon_min = -23
        elif region == "India":
            lat_max = 38 
            lat_min = 8
            lon_max = 98
            lon_min = 66
        elif region == "Analysis":
            lat_max = 54
            lat_min = 48
            lon_max = 10
            lon_min = 0
        else :
            lat_max = 90 
            lat_min = -90
            lon_max = 180
            lon_min = -180
        
        self.lat_max = lat_max
        self.lat_min = lat_min
        self.lon_max = lon_max
        self.lon_min = lon_min

        loc_per_dict = dict()
        
        if comp_with == "cams":
            data_C = self.data_C_c
            data_K = self.data_K_c
            data_P = self.data_P_c
        elif comp_with == "openaq":
            data_C = self.data_C_o
            data_K = self.data_K_o
            data_P = self.data_P_o

        for each in data_C:
            lat, lon , A, B, C, loc = float(each[0]), float(each[1]), int(each[2]), int(each[3]), int(each[4]), each[5]
            if lat_min<lat<lat_max and lon_min<lon<lon_max :
                per = A*100.0/(A+B+C)
                
                if loc in loc_per_dict:
                    loc_per_dict[loc][0] = per 
                else:
                    loc_per_dict[loc] = [per, None, None, lat, lon] 
            
        for each in data_K:
            lat, lon , A, B, C, loc = float(each[0]), float(each[1]), int(each[2]), int(each[3]), int(each[4]), each[5]
            if lat_min<lat<lat_max and lon_min<lon<lon_max :
       
                per = A*100.0/(A+B+C)
                
                if loc in loc_per_dict:
                    loc_per_dict[loc][1] = per 
                else:
                    loc_per_dict[loc] = [None, per, None, lat, lon] 
        
        for each in data_P:
            lat, lon , A, B, C, loc = float(each[0]), float(each[1]), int(each[2]), int(each[3]), int(each[4]), each[5]
            
            if lat_min<lat<lat_max and lon_min<lon<lon_max :
                per = A*100.0/(A+B+C)
                if loc in loc_per_dict:
                    loc_per_dict[loc][2] = per 
                else:
                    loc_per_dict[loc] = [None, None, per, lat, lon] 
        

        comp_set = set()
        C_set = set()
        K_set = set()
        P_set = set()

        for key,val in loc_per_dict.items():
            if val[0]!= None and val[1]!= None and val[2]!= None:
                key_lat_lon = (key, val[3], val[4])
                comp_set.add(key_lat_lon)
                if val[0] > threshold*100:
                    C_set.add(key_lat_lon)
                if val[1] > threshold*100:
                    K_set.add(key_lat_lon)
                if val[2] > threshold*100:
                    P_set.add(key_lat_lon)

        self.loc_per_dict = loc_per_dict
        self.comp_set = comp_set

        self.C_set = C_set
        self.K_set = K_set
        self.P_set = P_set
        
        num_total = len(comp_set)
        C_num = len(C_set)
        K_num = len(K_set)
        P_num = len(P_set)

        CK_num = len(C_set.intersection(K_set))
        CP_num = len(C_set.intersection(P_set))
        KP_num = len(K_set.intersection(P_set))

        CKP_num = len(C_set.intersection(K_set.intersection(P_set)))

        self.stats = {
            "num_total" : num_total,
            "C_num" : C_num,
            "K_num" : K_num,
            "P_num" : P_num,
            "CK_num" : CK_num, 
            "CP_num" : CP_num, 
            "KP_num" : KP_num,
            "CKP_num" : CKP_num 
        }

        return self.stats

    def regional_plot(self, method, region = "global", comp_with = "cams"):
        self.compare_methods(region = region, comp_with = comp_with)
        self.method = method
        if method == "COPOD":
            B = self.comp_set - self.C_set
            A = self.C_set
        elif method == "KNN":
            B = self.comp_set - self.K_set
            A = self.K_set
        elif method == "PCA":
            B = self.comp_set - self.P_set
            A = self.P_set

        self.plot_dir = "plots/regional/"

        self._plot(A, B, method)

    def _plot(self, A, B, method):

        self.c1 = "#ff6d69" # light_red
        self.c2 = "#fecc50" # light_yellow
        self.c3 = "#0be7fb" # light_blue
        self.c4 = "#010b8b" # dark blue
        self.c5 = "#1e0521" # blackish        

        self.s = 0.5

        img_quality =2
        img_size = (8,6)
        if self.region == "India":
            img_quality = 6
            img_size = (6,6)
        elif self.region == "Europe":
            img_quality = 6
            self.s = 1.0
            img_size = (8,6)
        elif self.region == "Analysis":
            self.s = 1.0
            img_quality = 4
            img_size = (8,6)

        fig = plt.figure(figsize=img_size, dpi = 240) 
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        stamen_terrain = cimgt.Stamen('terrain-background')
        ax.set_extent([self.lon_max, self.lon_min, self.lat_min, self.lat_max] 
                        , ccrs.PlateCarree())
        
        ax.add_image(stamen_terrain, img_quality)

        #ax.coastlines()
        #ax.stock_img()
        lat_A = [] 
        lon_A = []
        lat_B = []
        lon_B = []
        for _, lat, lon in A:
            lat_A.append(lat)
            lon_A.append(lon)
        
        for _, lat, lon in B:
            lat_B.append(lat)
            lon_B.append(lon)

        ax.scatter(lon_A, lat_A, color = self.c1, s = self.s, label = "Type A (dissimilar) stations")
        ax.scatter(lon_B, lat_B, color = self.c4, s = self.s, label = "Type B (similar) stations")

        ax.gridlines(crs=ccrs.PlateCarree(), draw_labels = True)
        

        tot_station = str(self.stats["num_total"])
        if method == "COPOD":
            a_station = str(self.stats["C_num"])
        elif method == "KNN":
            a_station = str(self.stats["K_num"])
        elif method == "PCA":
            a_station = str(self.stats["P_num"])

        ax.set_title("Region : "+self.region+" | Parameter : "+self.parameter+"\n Method : " + method 
                        + " | Compared With : " + self.comp_with + "\n Total stations " + tot_station + " | Type A stations : "+a_station, 
                        pad = 20)
        
        ax.legend()
        map_name = "_".join(["regional", method, self.parameter, self.comp_with, self.region])
        
        map_name = self.plot_dir+map_name+".png"
        plt.savefig(map_name)
        plt.close()
            

    def read_output(self,parameter, method, comp_with):
        
        ## directly filename can be used as well

        fname = "_".join(["overall",method, parameter, comp_with])

        fname = "outputs/"+fname+".csv"

        with open(fname, "r") as f:
            f.readline()
            data = []
            for each_line in f:
                data.append(each_line.rstrip("\n").split(",", 6))

        return data




