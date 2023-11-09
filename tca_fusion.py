#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:16:18 2023

@author: 21e8
"""

import os
import shutil
import time

def readTextFile(path_to_file):
    with open(path_to_file) as f:
        contents = f.readlines()
    f.close()
    return contents

def writeToText(path,text):
    with open(path, 'w') as f:
        f.write(text)
    f.close()
        
def appendToText(path,text):
    with open(path, 'a') as f:
        f.write(text)
    f.close()



def copyFolder(source_folder,destination_folder):
    for file_name in os.listdir(source_folder):
        source = os.path.join(source_folder,file_name)
        destination =os.path.join(destination_folder,file_name)
        shutil.copy(source, destination)
        #print("copied",source)
    return 0


def remove2(inlist,item):
    if item in inlist:
        inlist.remove(item)
    return inlist
        

now=time.time()

def mergeManifolds(groupPath,destination):
    groupPaths=remove2(os.listdir(groupPath),".DS_Store")
    print(groupPaths)
    fusionPath=os.path.join(destination,"fusion"+str(now))
    manifoldPath=os.path.join(destination,fusionPath,"manifold")
    pointsPath=os.path.join(destination,fusionPath,"points")
    documentsPath=os.path.join(destination,fusionPath,"documents")
     
    os.mkdir(fusionPath)
    os.mkdir(manifoldPath)
    os.mkdir(pointsPath)
    os.mkdir(documentsPath)
    
    revfusionPath=os.path.join(fusionPath,"manifold","reviews.txt")
    regfusionPath=os.path.join(fusionPath,"manifold","register.txt")
    print("revfusionPath",revfusionPath)
    print("regfusionPath",regfusionPath)
    
    for m in groupPaths:
        mPath=os.path.join(groupPath,m,"manifold")
        pPath=os.path.join(groupPath,m,"points")
        dPath=os.path.join(groupPath,m,"documents")
        
        revPath=os.path.join(fusionPath,m,"manifold","reviews.txt")
        regPath=os.path.join(fusionPath,m,"manifold","register.txt")
        
        mFiles=remove2([str(d) for d in os.listdir(mPath)],'.DS_Store')
        pFiles=remove2([str(d) for d in os.listdir(pPath)],'.DS_Store')
        dFiles=remove2([str(d) for d in os.listdir(dPath)],'.DS_Store')
        
        
        print("revPath",revPath)
        print("regPath",regPath)
        
        
        if "reviews.txt" in mFiles:
            path=os.path.join(groupPath,m,"manifold","reviews.txt")
            print("path",path)
            reader=readTextFile(path)
            for line in reader:
                appendToText(revfusionPath,line)
                
        for p in pFiles:
            try:
                iPath=os.path.join(groupPath,m,"points",p,"images")
                sPath=os.path.join(groupPath,m,"points",p,"sequences")
                aPath=os.path.join(groupPath,m,"points",p,"analysis")
                
                pfusionPath=os.path.join(fusionPath,"points",p)
                ifusionPath=os.path.join(fusionPath,"points",p,"images")
                sfusionPath=os.path.join(fusionPath,"points",p,"sequences")
                afusionPath=os.path.join(fusionPath,"points",p,"analysis")
                
                os.mkdir(pfusionPath)
                os.mkdir(ifusionPath)
                os.mkdir(sfusionPath)
                os.mkdir(afusionPath)

                copyFolder(iPath,ifusionPath)
                copyFolder(sPath,sfusionPath)
                
                appendToText(regfusionPath,p+"\n")

            except:
                print("error processing %s" %p)
    return 0
     

                 
        

