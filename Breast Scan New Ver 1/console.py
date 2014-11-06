import tables
import numpy as np
from outputEcvt import *
#from bTesKalibrasi import Ve, Vf
from math import *
from mayavi.mlab import *
import matplotlib.pyplot as plt
from tables import *
from CONVERTNSM import *
#from rekonstruksi import *
import tkFileDialog 
import matplotlib.gridspec as gridspec

import h5py

def kalibrasi():
        raw_input("Press Enter to begin empty calibration...")
        E1,E2,E3,ViDAC = empty_cal()
        raw_input("Press Enter to begin full calibration...")
        Ve, Vf = full_cal()
        saveH5(Ve,"Ve.h5")
        saveH5(Vf,"Vf.h5")
        kal_plotchart(Ve,Vf)
        return Ve, Vf


def scanning():
        ant3d=np.zeros(6255920)
        an3d=np.zeros(6255920)
        
        f=tables.openFile("ant3d.h5")
        g=tables.openFile("an3d.h5")
        h=tables.openFile("Ve.h5")
        j=tables.openFile("Vf.h5")
        
        ant3d= f.root.detector.readout.cols.matNsm[:]
        an3d= g.root.detector.readout.cols.matNsm[:]
        Ve= h.root.detector.readout.cols.matNsm[:]
        Vf= j.root.detector.readout.cols.matNsm[:]
        
        
        
        
        ant3d=ant3d.reshape(32768, 190)
        an3d=an3d.reshape(190, 32768)
        
        CH=20
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
        Vr=[]
        ncp=[]
        cp=[]
        image1=[]

        for i in range(1):
                [datValid[i:], dtValid] = full_ecvt_get_data(dtValid)    
                [a, b]=shape(datValid)                
                Vr=datValid[0]
                plotchart(Ve,Vf,Vr)
                #print Vr
                frames=frames+1
                Vr1=Vr/Vf
                Vr1=Vr1.reshape(1, m)
                #dataArbai=Vr
                dn = (Vr1-Ve1)/(Vf1-Ve1)
                dn[nonzero(dn>=1)]=1
                dn[nonzero(dn<=0)]=0
                y1=dn.T
                y1=konvertnan(y1)
                ncp[i:]=np.array([y1])
                Vrr=Vr1.T
                Vrr=konvertnan(Vrr)
                cp[i:]=Vrr
                iter=2                                                                                                                                      
                alpha0=0.1
                t=0
                v0=dot(ant3d, y1)
                eval=1
                t1=1
                serr=0
                v=v0
                while (t1<=iter):
                        phi1=y1-dot(ant3d.T, v0)
                        v=v0+alpha0*dot(an3d.T, phi1)
                        err=abs(v-v0)
                        serr=serr+sum(err**2)
                        v[nonzero(v>=1)]=1
                        v[nonzero(v<=0)]=0
                        v0=v
                        t1=t1+1
                image1=v.reshape((32, 32, 32))   
    
        x, y, z = np.ogrid[0:31:31j, 0:31:31j, 0:31:31j]
        s = image1
        
        src = mlab.pipeline.scalar_field(s, 
                                         scaling=(1, 1, 1), 
                                         origin=(1,1,1))
        
        src.spacing = [0.75, 1, 1]
        
        #iso surface
        m=mlab.pipeline.iso_surface(src, 
                                    contours=[s.min()+0.01*s.ptp(), ],
                                    opacity=0.3
                                    )
        
        #imageplane X
        mlab.pipeline.image_plane_widget(src,plane_orientation='y_axes',slice_index=16,)
        
	#imageplane X
        mlab.pipeline.image_plane_widget(src,plane_orientation='x_axes',slice_index=16,)        
        
        
        #volume 
        mlab.pipeline.volume(
                src, 
                vmin=s.min(), 
                vmax=0.2
        )       
        
        m.module_manager.scalar_lut_manager.show_scalar_bar = True
        mlab.colorbar(orientation='vertical')  
	f = mlab.gcf()
	camera = f.scene.camera
	camera.yaw(60)	
        # LUT means "Look-Up Table", it give the mapping between scalar value and color
        mlab.view(15, 15, 15, (20, 20, 20))
        mlab.show()
	
	return Ve, Vf, Vr