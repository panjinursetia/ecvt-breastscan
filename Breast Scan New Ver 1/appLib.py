import numpy as np
import random 

def gen_mat(ukuran,min_data,max_data):
    data = np.zeros(190)
    for i in range (np.size(data)):
        data[i]=random.randint(min_data,max_data)
    return data
#sensor
#0 = breast
#1 = brain
#2 = silinder
#3 = planar

#channel
#16 = 0
#20 = 1
#24 = 2
#32 = 4
def get_channel(channel):
    #Jumlah Channel    
    if (channel==0):
        channel = 16
    elif (channel==1):
        channel = 20
    elif (channel==2):
        channel = 24
    elif (channel==3):
        channel = 32     
    return channel

def get_sm_files(sensor,channel):    
    #Jenis Sensor
    if (sensor ==0):
        string_sensor = "Breast_"
    elif (sensor==1):
        string_senor = "Brain_"
    elif (sensor == 2):
        string_sensor = "Silinder_"
    elif (sensor==3) :
        string_sensor = "Planar_"
    #Jumlah Channel    
    if (channel==0):
        string_channel = "16CH.h5"
    elif (channel==1):
        string_channel = "20CH.h5"
    elif (channel==2):
        string_channel = "24CH.h5" 
    elif (channel==3):
        string_channel = "32CH.h5" 
    
    string_sm = string_sensor+string_channel
    
    return string_sm
    
    




