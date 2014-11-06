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
    
    

