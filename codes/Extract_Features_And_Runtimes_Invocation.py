import pandas as pd
import numpy as np
import re
import os
import copy
import clgen.clutil
import clgen.model
import sqlite3
import clgen.sampler
import clgen.dbutil
import clgen.explore
import re
import shutil
from subprocess import Popen, PIPE
import glob
from sys import argv, exit
import Mappings

###############
# This version doesn't take into account invocation numbers
###############

# Renames old features to new features
def renamecolumns(df):
    for k in Mappings.renameDictionary.keys():
        df = df.rename(columns={k:Mappings.renameDictionary[k]})
    return df    

# renames the regions of each runtime file into the correct kernel namings
def normaliseRegions(allruntimes):   
    allregionsList = []
    for region in Mappings.kernelMappings.keys():
        allruntimes.loc[allruntimes['region'] == region, 'region'] = Mappings.kernelMappings[region]
        allregionsList.append(Mappings.kernelMappings[region])
    return allruntimes[allruntimes['region'].isin(allregionsList)]

readAIWCFeatures = False

if len(argv) == 4:
    aiwcfeaturesfolder = str(argv[1])
    print("AIWC Features located at: ", aiwcfeaturesfolder)
    runtimesfolder = str(argv[2])
    print("Opendwarfs runtimes found at: ", runtimesfolder)
    destinationcsv = str(argv[3])
    print("Output destination is: ", destinationcsv)
else:
    print("Invalid arguments")
    print("Required: Aiwc Features Folder, Opendwarfs runtimes folder, destination csv file")
    exit    
    
#############################
# Loads in the AIWC features
# from the AIWCFeatures directory
# includes invocation numbers 
#############################

if (".csv" in aiwcfeaturesfolder):
    currentdf = pd.read_csv(aiwcfeaturesfolder)
else:
    counter = 0
    kernals = list()
    parsedAlready = set()
    currentdf = []
    for size in ['tiny', 'small', 'medium', 'large', 'default']:
        print("Currently handling ", size)
        for f in glob.glob(aiwcfeaturesfolder + size + "/*.csv"):
            kernelString = "_".join(f.split("_")[0:-1])
            print(kernelString)
            invonum = int(re.findall(r'\d+', f)[-1])

            featuresdf = pd.read_csv(f).values.T
            fdf = pd.DataFrame(columns=featuresdf[0,])
            fdf.loc[0] = featuresdf[1,]
            fdf['invocation'] = invonum
            fdf['kernel'] = "_".join(f.split('/')[-1].split("_")[1:-1])
            fdf['size'] = size
            if (len(currentdf) == 0):
                currentdf = fdf
            else:
                currentdf = pd.concat([currentdf, fdf], axis=0)
            

#############################
# Loads in the Opendwarfs Kernel runtime features into allruntimes
# handles this by invocation
#############################

def extractInvocation(lsbFile):
    kernelsSeen = dict()
    invocation = []
    currentRepeat = 0
    for index, row in lsbFile.iterrows():
        if ("repeats_to_two_seconds" in lsbFile.columns):
            if (currentRepeat != row['repeats_to_two_seconds']):
                kernelsSeen = dict()
                currentRepeat = row['repeats_to_two_seconds']
        reg = row['region']
        if (reg in kernelsSeen):
            kernelsSeen[reg] += 1
        else:
            kernelsSeen[reg] = 0
        invocation.append(kernelsSeen[reg])
    return invocation

if (".csv" in runtimesfolder):
    allruntimes = pd.read_csv(runtimesfolder)
else:
    start = True
    allruntimes = []
    parsed = []
    for root, dirs, files in os.walk(runtimesfolder):
        for file in files:
            if ('lsb' in file):
                file = os.path.join(root,file)
                try:
                    testfolder = pd.read_csv(file, skiprows=9, sep="[ ]+", engine='python', skipfooter=1)
                    invo = extractInvocation(testfolder)
                    try:
                        totalTimes = testfolder.groupby("repeats_to_two_seconds").sum().reset_index()
                        totalTimes = totalTimes.rename(columns={"time":"total_time"})

                        totalTimes = totalTimes[['total_time','repeats_to_two_seconds']]
                        testfolder = pd.merge(testfolder, totalTimes, on='repeats_to_two_seconds')
                    except:
                        testfolder["total_time"] = np.sum(testfolder['time'])
                        print("Repeats_to_to_seconds not detected, numerically likely unstable in: ", file)
                    testfolder = testfolder.rename(columns={"time":"kernel_time"})

                    problemSize = ""
                    if ('tiny' in file):
                        problemSize = 'tiny'
                    elif ('small' in file):
                        problemSize = 'small'
                    elif ('medium' in file):
                        problemSize = 'medium'
                    elif ('large' in file):
                        problemSize = 'large'

                    testfolder['size'] = problemSize
                    testfolder['device'] = file.split("/")[1].split("_")[0]
                    testfolder['application'] = file.split("/")[1].split("_")[1]
                    testfolder['kernel'] = file.split("/")[-1].split('.')[1]   

                    testfolder['invocation'] = invo

                    testfolder = testfolder[['application','region','total_time','kernel_time','size','kernel','device','invocation']]
                    testfolder = testfolder.groupby(['application','invocation','size','device','region']).mean().reset_index()

                    print(file, testfolder.values.shape)
                    if (start):
                        allruntimes = testfolder
                        start = False
                        dickhead += 1
                    else:
                        allruntimes = pd.concat([allruntimes, testfolder], axis=0)
                except:
                    print("Failed on:", file)
            else:
                print("Skipping file:", file)
            
currentdf.to_csv(str("backups/aiwcfeatures-invocation" + "_".join(np.unique(testfolder['device']))) + ".csv", index=False)
allruntimes.to_csv("backups/allruntimes-alldevices-invocation.csv", index=False)
 
kernelruntimes = normaliseRegions(allruntimes)
kernelruntimes = kernelruntimes.rename(columns={'region':'kernel'})
kernelruntimes = kernelruntimes.groupby(['kernel','invocation','size','application','device']).mean().reset_index()
mergedStuff = pd.merge(kernelruntimes, currentdf, how='inner', left_on=['invocation','size','kernel'], right_on=['invocation','size','kernel'])
try:
    mergedStuff = renamecolumns(mergedStuff)
except:
    print("Failed to rename the columns because of unexpected keys")
mergedStuff.to_csv(destinationcsv,index=False)







