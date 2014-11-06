import serial
from numpy import *
from math import *
import numpy as np
import binascii
import base64
from compiler.ast import Bitxor
import time
import h5py
from appLib import *


from mayavi import mlab
from mayavi import *
import numpy as np
import matplotlib.pyplot as plt

program_dir = "F:/CHPC/Breast Scan New Ver 1"

def getDeviceSetting():
        fname = program_dir+"/database/setting.h5"
        fname = unicode(fname)  
        device_data = h5py.File(fname)          
        sensor=array(device_data['sensor'])
        channel=array(device_data['channel'])
        channel = get_channel(channel)
	device_data.close()
        return channel    

CH = getDeviceSetting()
m=CH*(CH-1)/2   

ser = serial.Serial(
       port='COM31',
       baudrate=115200,
       stopbits=1,
       timeout=10)     


def konvertnan(matriks):
    [a,  b]=shape(matriks)
    for i in range(a):
         if (isnan(matriks[i])):
            matriks[i]=0
    return matriks
    
def konvertbinaryhexa(data):
    MAX_UU = 45
    lines = []
    for i in range(0, len(data)):
        b = data[i]
        a = binascii.b2a_hex(b)
        #a = binascii.hexlify(a)
        lines.append(a)
    return lines 

def output_ecvt(ser_con):
    ser = ser_con
    ser.write('$RUNN\n')    
    a=ser.read(4000)
    ser.write('$STOP\n')
    b=ser.read(50) 
    return a+b

##fungsi perintah ke DAS
def setting_ecvt(con_ser):
    ser = con_ser
    CH = getDeviceSetting()
    strCH = str(CH)
    par = "$SETT,"+strCH+"*\n"
    ser.write(par)            
    a=ser.readline()
    b=ser.readline()
    return a+b

def warmoff_ecvt(): 
        ser.write('$WMOF\n')           
        a=ser.readline()       
        return a

def sdac_ecvt(): 
        ser.write('$SDAC,1500,*\n')          
        a=ser.readline()       
        return a

def gain_ecvt(): 
        ser.write('$GAIN,0.5,*\n')          
        a=ser.readline()        
        return a
    
def mean_ecvt(): 
        ser.write('$MEAN,5,*\n')         
        a=ser.readline()        
        return a
    
def empty_cal(con_ser):
    ser = con_ser
    ser.write('$EMPT,900,*\n')         
    E1=ser.readline() 
    E2=ser.readline()
    E3=ser.readline()
    ViDAC=E3[6:len(E3)]
    #empty=find_empt_ecvt(a)
    #vdac=find_vdac_ecvt(a)
    #EMPT=a[empty(0):vdac-1]
    #VDAC=a[vdac(0):len(a)]
    return E1,E2,E3,ViDAC
    
def stop_ecvt():
        ser.write('$STOP\n')  
        a=ser.read(500)  
        return a
    
def full_cal(con_ser):   
    ser=con_ser
    ser.write('$FULL,1500,*\n')    
    F1=ser.readline() 
    F2=ser.readline()
    F3=ser.readline()
    VieF=F1[6:len(F1)-3]
    VifF=F2[6:len(F2)-3]
    VigF=F2[6:len(F3)-6]
    Ve=VieF.split(' ')
    Vf=VifF.split(' ')
    return Ve, Vf 


    
def data_header_ecvt(m,dataEcvt):
    kar = dataEcvt
    #hitung jumlah string $ECVT di paket data
    count_string = kar.count('$ECVT')
    ecvt=[]
    ecvt1 = kar.find('$ECVT')
    i=0
    while (i<count_string):
        if (i==0):            
            ecvt.append(kar.find('$ECVT'))
        else:
           ecvt.append(kar.find('$ECVT', ecvt[i-1]+5 , m*5))
        i=i+1
    #output matriks indeks data header ecvt    
    return ecvt

def find_empt_ecvt(dataEcvt):
    kar = dataEcvt
    #hitung jumlah string $ECVT di paket data
    count_string = kar.count('$EMPT')
    ecvt=[]
    ecvt1 = kar.find('$EMPT')
    i=0
    while (i<count_string):
        if (i==0):
            ecvt.append(kar.find('EMPT'))
        else:
           ecvt.append(kar.find('$EMPT', ecvt[i-1]+5 , 120*5))
        i=i+1
    #output matriks indeks data header ecvt
    return ecvt

def find_vdac_ecvt(dataEcvt):
    kar = dataEcvt
    #hitung jumlah string $ECVT di paket data
    count_string = kar.count('$VDAC')
    ecvt=[]
    ecvt1 = kar.find('$VDAC')
    i=0
    while (i<count_string):
        if (i==0):
            ecvt.append(kar.find('VDAC'))
        else:
           ecvt.append(kar.find('$VDAC', ecvt[i-1]+5 , m*5))
        i=i+1
    #output matriks indeks data header ecvt
    return ecvt


def ecvt_get_data(m, dataEcvt, dtValid):
    ecvt = data_header_ecvt(m, dataEcvt)
    print ecvt
    kar = dataEcvt
    #print kar
    ii=0
    dec=[]
    Data=[]
    ww=[]
    www=[]
    while (ii<len(ecvt)):
        if (len(kar)>=ecvt[ii]+5+m*2+1):
            #ambil data dan simpan ke array data 4 diganti 5
            Data[ii:]=kar[ecvt[ii]+5:ecvt[ii]+5+m*2]
	    #print Data[ii:]
            #ambil data ceksum
            DatCekSum=kar[ecvt[ii]:ecvt[ii]+5+m*2+1]
            #konvert decimal ke hexadecimal
            s=kar[ecvt[ii]+5:ecvt[ii]+5+m*2]
            ww[ii:]=np.array([konvertbinaryhexa(s)]).T
            [a,  b] = shape(ww[ii:])    
            dtValid=dtValid+1
            #tukar posisi dimensi matriks
            www[ii:]=np.reshape(ww[ii:], (1, a*b))
            newPos = 0            
            datadec=[]            
            #print len(www[ii])
            #print www[ii]
            k=0
            for i in xrange(0,len(www[ii]),2):
                 if (k+1>(len(www[ii])/2)):   
                    print "Data"
		    
                    stringData = str(www[ii][i])
                 else:
		     stringData = str(www[ii][i]+www[ii][i+1])
		     #stringData = str(www[ii][i+1]+www[ii][i])
		 #stringData = stringData[3]+stringData[4]+stringData[0]+stringData[1]    
                 #print k, i,i+1,  stringData, int(stringData, 16)
		 #print stringData
                 k=k+1
                #konvert dari hexa ke desimal
                 datadec.append(int(stringData, 16))                
            dec[dtValid-1:]=np.array([datadec])
	    #print dec
            #print shape(dec)
        ii=ii+1         
    return dec, dtValid         
            
def full_ecvt_get_data(dtValid,con_ser):    
    ser = con_ser
    CH = getDeviceSetting()
    m=CH*(CH-1)/2      
    dataEcvt = output_ecvt(con_ser)
    datValid,  dtValid = ecvt_get_data(m, dataEcvt, dtValid)
    ser.write('$STOP\n')
    return datValid, dtValid


def empty_full_gain_ecvt():
    start_time = time.clock()
    ser.write('$SETT,20,*\n')
    a=ser.readline() 
    print a
    b=ser.readline()
    print b
    c=ser.readline()
    print c
    d=ser.readline()
    print d    
    
    print sdac_ecvt()
    print gain_ecvt()
    print mean_ecvt()
    
    ser.write('$WMOF\n')           
    a=ser.readline()          
    print a
    print "setting time elapsed in", time.clock() - start_time, "seconds" 

def kal_plotchart(Ve,Vf):
	plt.plot(Ve,'r', label="Ve")
	plt.plot( Vf, 'b', label="Vf")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.ylabel('Voltase (mV)')
	plt.xlabel('Jumlah M')
	plt.title('Grafik Hubungan Ve|Vf|Vr')
	plt.show()

def plot_grafik(nama_variabel):
    plt.plot(nama_variabel,'r', label="label_grafik")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylabel('Voltase (mV)')
    plt.xlabel('Jumlah M')    
    plt.title('Grafik')
    plt.show()
    
#print output_ecvt(20)
##a= full_empty_cal(20,1)
##print a

