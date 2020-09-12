import numpy as np
import re
import os
import copy
import shutil
from subprocess import Popen, PIPE
import glob
from sys import argv, exit

device = argv[1]

os.chdir("CLKernelStaging/")
with open('/workspace/codes/long_kernels_list.csv', 'r+') as f:
    kernals = f.readlines()

finaldat = np.zeros((1,7))
headers = np.array([])

platform_id = "-p 0"
device_id = "-d 0"

if (len(argv) == 3):
    if (argv[2] == 'cpu'):
        platform_id = "-p 1"

for kernal in kernals:
    k = kernal.replace("\n", "")
    k = k.split("/")[-1]
    kk = str('/workspace/codes/CLKernelArchive/' + k)
    print(k)
    
    for f in glob.glob('lsb.*'):
        os.remove(f)
    for f in glob.glob('aiwc_A*.csv'):
        os.remove(f)
    
    for psize in ['tiny','small','medium','large']:
        
        # Run the kernel 50 times
        for i in range(0,5):
            process = Popen(["../synthetic-benchmark-driver/sbd", kk, psize, platform_id, device_id, "runtime"], stdout=PIPE)

            (output, err) = process.communicate()
            exit_code = process.wait()
            
            asda = np.genfromtxt("lsb.sbd.r0", skip_header=9, skip_footer=1, dtype=str)
            if (headers.shape == (0,)):
                headers = asda[0,:]
            
            asda = asda[asda[:,2] == 'kernel']
            meantimes = np.mean(asda[:,5].astype(np.float64))
            newdatapoint = asda[0]
            newdatapoint[5] = meantimes
            newdatapoint[1] = k
            finaldat = np.concatenate((finaldat, newdatapoint.reshape(1,7)), axis=0)
            
            for f in glob.glob('lsb.*'):
                os.remove(f)
            for f in glob.glob('aiwc_A*.csv'):
                os.remove(f)
        
namefile = str("../longrunkernels_" + device + "_all_sizes.csv")
np.savetxt(namefile, finaldat, delimiter=',',encoding='utf-8', fmt='%s')
