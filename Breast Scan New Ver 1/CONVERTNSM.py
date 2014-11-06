from tables import *
import numpy as np
data = np.zeros(4472160)

from tables import *

# Define a user record to characterize some kind of particles
class Particle(IsDescription):
    idNsm  = Int64Col()      # Signed 64-bit integer
    matNsm    = FloatCol()      # double (double-precision)

def convertnsm(nama_nsm,nama_h5):
    filename = nama_h5
    h5file = openFile(filename, mode = "w", title = "Test file")
    group = h5file.createGroup("/", 'detector', 'Detector information')
    table = h5file.createTable(group, 'readout', Particle, "Readout example")
    particle = table.row

    ii=0
    iii=0
    for line in open(nama_nsm, 'r'):    
        fields = line.strip().split(' ')
        for i in range(len(fields)):
            if (len(fields[i])>0):
                 particle['idNsm'] = ii
                 particle['matNsm'] = float(str(fields[i]))
                 particle.append()
                 print ii
                 ii=ii+1
        
        iii=iii+1
    h5file.close()

def saveH5(data,outputfile):
    filename = outputfile
    h5file = openFile(filename, mode = "w", title = "Test file")
    group = h5file.createGroup("/", 'detector', 'Detector information')
    table = h5file.createTable(group, 'readout', Particle, "Readout example")
    particle = table.row
    b = np.size(data)
    
     
    k=0
    for k in range(b):
        particle['idNsm'] = k
        particle['matNsm'] = data[k]
        particle.append()

    h5file.close()

    
#convertnsm("ant3d_20CH.txt","ant3d.h5")
