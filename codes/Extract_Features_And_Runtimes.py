import pandas as pd
import numpy as np
import re
import os
import copy
import re
import shutil
from subprocess import Popen, PIPE
import glob
from sys import argv, exit
import Mappings

###############
# This version doesn't take into account invocation numbers
###############
       
# renames the regions of each runtime file into the correct kernel namings
def normaliseRegions(allruntimes):   
    allregionsList = []
    for region in Mappings.kernelMappings.keys():
        allruntimes.loc[allruntimes['region'] == region, 'region'] = Mappings.kernelMappings[region]
        allregionsList.append(Mappings.kernelMappings[region])
    return allruntimes[allruntimes['region'].isin(allregionsList)][['application','region','total_time','kernel_time','size','device']]

readAIWCFeatures = False
failedfiles = []

if len(argv) == 4:
    aiwcfeaturesfolder = str(argv[1])
    print("AIWC Features located at: ", aiwcfeaturesfolder)
    runtimesfolder = str(argv[2])
    print("Opendwarfs runtimes found at: ", runtimesfolder)
    destinationcsv = str(argv[3])
    print("Output destination is: ", destinationcsv)
elif len(argv) == 3:
    readAIWCFeatures = True
    aiwcfeaturesfolder = str(argv[1])
    print("AIWC Features located at: ", aiwcfeaturesfolder)
    targetfile = str(argv[2])
    print("Output file found at: ", targetfile)
else:
    print("Invalid arguments")
    print("Expected arguments: <AIWC Features folder> <Program Runtimes folder> <Destination csv file>")
    print("or arguments: <AIWC Features folder> <Destination csv file>")
    exit()
    
#############################
# Loads in the AIWC features
# from the AIWCFeatures directory
#############################

counter = 0
kernals = list()
parsedAlready = set()
for size in ['tiny', 'small', 'medium', 'large', 'default']:
    print("Currently handling ", size)
    for f in glob.glob(aiwcfeaturesfolder + size + "/*.csv"):
        kernelString = "_".join(f.split("_")[0:-1])
        if (readAIWCFeatures or (not (kernelString in parsedAlready))):
            aiwcfeatures = pd.read_csv(f).values.T
            lastcol = aiwcfeatures.shape[0]-1
#             print(aiwcfeatures.shape, lastcol)
#             break
            if (counter == 0):
                aiwcfeaturesdf = pd.DataFrame(columns=aiwcfeatures[0,])
                aiwcfeaturesdf['kernel'] = ""
                aiwcfeaturesdf['size'] = ""
            try:
                aiwcfeaturesdf.loc[counter,0:-2] = aiwcfeatures[lastcol,]
                kername = "_".join(f.split('/')[-1].split("_")[1:-1])
                aiwcfeaturesdf.iloc[counter,-2] = kername
                aiwcfeaturesdf.iloc[counter,-1] = size
                counter+=1
            except:
                print(aiwcfeatures[1,])
            parsedAlready.add(kernelString)
            print(kernelString)
#         break
#     break

if (readAIWCFeatures):
    print("Writing AIWC features to:", targetfile)
    aiwcfeaturesdf.to_csv(targetfile, index=False)
    exit()
            
aiwcfeaturesdf.groupby(['kernel', 'size']).max().reset_index()

#############################
# Loads in the Opendwarfs Kernel runtime features into allruntimes
#############################

if (".csv" in runtimesfolder):
    allruntimes = pd.read_csv(runtimesfolder)
else:
    start = True
    allruntimes = []
    parsed = []
    for root, dirs, files in os.walk(runtimesfolder):
        # Iterates through a single instance of a file and adds all of the information to a dataframe
        for file in files:
            file = os.path.join(root,file)
            try:
                testfolder = pd.read_csv(file, skiprows=9, sep="[ ]+", engine='python', skipfooter=1)

                totalTimes = testfolder.groupby("repeats_to_two_seconds").sum().reset_index()
                totalTimes = totalTimes.rename(columns={"time":"total_time"})
                totalTimes = totalTimes[['total_time','repeats_to_two_seconds']]
                testfolder = pd.merge(testfolder, totalTimes, on='repeats_to_two_seconds')
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

                testfolder = testfolder.groupby(['region', 'size']).mean().reset_index()

                testfolder['device'] = file.split("/")[1].split("_")[0]
                testfolder['application'] = file.split("/")[1].split("_")[1]
                testfolder['kernel'] = file.split("/")[-1].split('.')[1]    

                print(file, testfolder.values.shape)
                if (start):
                    allruntimes = testfolder
                    start = False
                else:
                    allruntimes = pd.concat([allruntimes, testfolder], axis=0)
            except:
                print("Failed on:", file)
                failedfiles.append(file)
            
normalisedAllRuntimes = normaliseRegions(allruntimes)
normalisedAllRuntimes = normalisedAllRuntimes.rename(columns={"region":"kernel"})
daaaata = pd.merge(aiwcfeaturesdf, normalisedAllRuntimes, how='inner', on=['kernel', 'size'])
daaaata.to_csv(destinationcsv, index=False)
print("Failed on these files: ", failedfiles)
