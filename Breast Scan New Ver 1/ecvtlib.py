import serial
from numpy import *
from math import *
import numpy as np
import binascii
import base64
from compiler.ast import Bitxor
from appLib import *
import h5py
program_dir = "F:/CHPC/Breast Scan New Ver 1"

def resize_sm(an3d,start,end,scale):
    m = 276
    an3d = an3d.reshape(276,32,32,32)
    for i in range (0,m):
        an3d[i,start:end,:,:] = an3d[i,start:end,:,:]*scale
    an3d = an3d.reshape(276,32*32*32)
    return an3d

def resize_sm_0(an3d,start,end,scale):
    m = 276
    an3d = an3d.reshape(1,276*32*32*32)
    for i in range (1,276*32*32*32):
        if (an3d[0,i] > 0):
            an3d[0,i] = 0
    an3d = an3d.reshape(276,32*32*32)
    return an3d

def resize_sm_x(an3d,start,end,scale):
    m = 276
    an3d = an3d.reshape(276,32,32,32)
    for i in range (0,m):
        an3d[i,start:end,:,:] = an3d[i,start:end,:,:]*scale
    an3d = an3d.reshape(276,32*32*32)
    return an3d

def resize_sm_y(an3d,start,end,scale):
    m = 276
    an3d = an3d.reshape(276,32,32,32)
    for i in range (0,m):
        an3d[i,:,start:end,:] = an3d[i,:,start:end,:]*scale
    an3d = an3d.reshape(276,32*32*32)
    return an3d

def resize_sm_z(an3d,start,end,scale):
    m = 276
    an3d = an3d.reshape(276,32,32,32)
    for i in range (0,m):
        an3d[i,:,:,start:end] = an3d[i,:,:,start:end]*scale
    an3d = an3d.reshape(276,32*32*32)
    return an3d

def resize_sm_z_pixel(an3d,pixel,scale):
    m = 276
    an3d = an3d.reshape(276,32,32,32)
    for i in range (0,m):
        an3d[i,:,:,pixel] = an3d[i,:,:,pixel]*scale
    an3d = an3d.reshape(276,32*32*32)
    return an3d

def smooth_image(im_mat, scale):
    max_mat = np.max(im_mat)
    treshold = max_mat*scale
    a, b, c = np.shape(im_mat)
    matshape = np.size(im_mat)
    im_mat= im_mat.reshape(1,matshape)
    for i in range(matshape):
        if (im_mat[0,i] < treshold):
            im_mat[0,i] = 0
    im_mat = im_mat.reshape(a, b, c)    
    return im_mat

def smooth_image1(im_mat, scale):
    max_mat = np.max(im_mat)
    treshold = max_mat*scale
    treshold1 = max_mat*0.8
    a, b, c = np.shape(im_mat)
    matshape = np.size(im_mat)
    im_mat= im_mat.reshape(1,matshape)
    for i in range(matshape):
        if (im_mat[0,i] < treshold):
            im_mat[0,i] = 0
    im_mat = im_mat.reshape(a, b, c)    
    return im_mat
    
    
    

def ecvt_mat_r1(Ve,Vf,Vr,an3d,ant3d):
    #----------get normalize capacitance
    fr=1 #num of frame
    ncp = []
    for i in range(fr):               
        cnorm = (Vr-Ve)/(Vf-Ve)  #normalize
        cnorm[nonzero(cnorm>=1)]=1  #filter assumption
        cnorm[nonzero(cnorm<=0)]=0
        
        cdat=cnorm.T
        cdat[np.isnan(cdat)]=0
        
        ncp[fr:]=array([cdat])
        g0=dot(an3d.T,cdat)     #LBP
        
        iter=100      #num of iteration                            
        alpha=0.9     #penalty factor
        
    #----------iteration linear back projection
        t1=1
        serr=0
        while (t1<=iter):        
            delc=cdat-dot(an3d, g0)       #capacitance difference
            g=g0+alpha*dot(an3d.T, delc)      
            err=abs(g-g0)                 #calculate error
            serr=serr+sum(err**2)
            g[nonzero(g>=1)]=1
            g[nonzero(g<=0)]=0
            g0=g
            t1+=1
        image1=g.reshape((32, 32, 32),order="F")   
    return image1
        
def ecvt_matriks(fname):  
    
    v_data = h5py.File(fname)    
    Ve=array(v_data['Ve'])
    Vf=array(v_data['Vf'])
    Vr=array(v_data['Vr'])         
    sensor=array(v_data['sensor'])
    channel=array(v_data['channel'])     
    data_sm = get_sm_files(sensor,channel)
    smfile = program_dir+"/database/"+data_sm
    
    sm_data=h5py.File(smfile)
    an3d=array(sm_data['an3d'])   
    ant3d=array(sm_data['ant3d']) 
    
    Vr = np.array(Ve, np.float)
    Vf = np.array(Vf, np.float)
    Ve = np.array(Ve, np.float)
    v_data.close()
    sm_data.close()
    
    CH = get_channel(channel)
    m=CH*(CH-1)/2
    SETi=10
    b=0
    frames=0
    Frame=SETi
    urut =1
    urut=0
    dec=np.zeros((1,m))
    dataArbai=np.zeros((SETi,1))
    ADC=np.zeros((1,2*m))
    DataRec=np.zeros((SETi,m))
    dt=0
    Avg=8
    iAvg=0
    datAvg=0
    datValid=0
    Ve1=Ve/Vf
    Vf1=np.ones((1, m))
    dtValid=0
    datValid=[]
    ncp=[]
    cp=[]
    image1=[]    
    for i in range(Frame):
        frames=frames+1    
        Vr1=Vr/Vf        
        Vr1=Vr1.reshape(1, m)
        #dataArbai=Vr
        dn = (Vr1-Ve1)/(Vf1-Ve1)
        dn[np.nonzero(dn>=1)]=1
        dn[np.nonzero(dn<=0)]=0
        y1=dn.T
        y1=konvertnan(y1)
        ncp[i:]=np.array([y1])
        Vrr=Vr1.T
        Vrr=konvertnan(Vrr)
        cp[i:]=Vrr
        iter=2                                                                                                                                      
        alpha0=0.9
        t=0
        v0=dot(ant3d, y1)
        eval=1
        t1=1
        serr=0
        v=v0
        while (t1<=1):
            phi1=y1-dot(ant3d.T, v0)
            v=v0+alpha0*dot(an3d.T, phi1)
            err=abs(v-v0)
            serr=serr+sum(err**2)
            v[np.nonzero(v>=1)]=1
            v[np.nonzero(v<=0)]=0
            v0=v
            t1=t1+1
        image1=v.reshape((32, 32, 32))   
    
    return image1    

def ecvt_mat(Ve,Vf,Vr,an3d,ant3d):    
    Vr = np.array(Vr, np.float)
    Vf = np.array(Vf, np.float)
    Ve = np.array(Ve, np.float)
    
    CH = 20
    m=CH*(CH-1)/2
    SETi=10
    b=0
    frames=0
    Frame=SETi
    urut =1
    urut=0
    dec=np.zeros((1,m))
    dataArbai=np.zeros((SETi,1))
    ADC=np.zeros((1,2*m))
    DataRec=np.zeros((SETi,m))
    dt=0
    Avg=8
    iAvg=0
    datAvg=0
    datValid=0
    Ve1=Ve/Vf
    Vf1=np.ones((1, m))
    dtValid=0
    datValid=[]
    ncp=[]
    cp=[]
    image1=[]    
    for i in range(Frame):
        frames=frames+1    
        Vr1=Vr/Vf        
        Vr1=Vr1.reshape(1, m)
        #dataArbai=Vr
        dn = (Vr1-Ve1)/(Vf1-Ve1)
        dn[np.nonzero(dn>=1)]=1
        dn[np.nonzero(dn<=0)]=0
        y1=dn.T
        y1=konvertnan(y1)
        ncp[i:]=np.array([y1])
        Vrr=Vr1.T
        Vrr=konvertnan(Vrr)
        cp[i:]=Vrr
        iter=2                                                                                                                                      
        alpha0=0.9
        t=0
        v0=dot(ant3d, y1)
        eval=1
        t1=1
        serr=0
        v=v0
        while (t1<=1):
            phi1=y1-dot(ant3d.T, v0)
            v=v0+alpha0*dot(an3d.T, phi1)
            err=abs(v-v0)
            serr=serr+sum(err**2)
            v[np.nonzero(v>=1)]=1
            v[np.nonzero(v<=0)]=0
            v0=v
            t1=t1+1
        image1=v.reshape((32, 32, 32))   
    
    return image1    

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