#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:16:18 2023

@author: 21e8
"""

import os
import shutil

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
        

mfld1Path="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/Books/"
mfld2Path="/Users/21e8/Desktop/tc0/"

destinationFolder="/Users/21e8/Desktop/"
corpusName="newTextCorpus2"
destinationPath=os.path.join(destinationFolder,corpusName)



folders1=[str(d) for d in os.listdir(mfld1Path)]
folders2=[str(d) for d in os.listdir(mfld2Path)] 

if corpusName in os.listdir(destinationFolder):
    print("Corpus' name already exists in destination folder\nPlease, choose another corpus' name.")
else:
       
    if ("manifold" and "points" and "documents") in (folders1 and folders2):
        print("fusion is potentially feasible")
        source1_points_path=os.path.join(mfld1Path,"points")
        source2_points_path=os.path.join(mfld2Path,"points")
        
        documents1Path=os.path.join(mfld1Path,"documents")
        documents2Path=os.path.join(mfld2Path,"documents")
        
        manifold1Path=os.path.join(mfld1Path,"manifold")
        manifold2Path=os.path.join(mfld2Path,"manifold")
        
        points1Path=os.path.join(mfld1Path,"points")
        points2Path=os.path.join(mfld2Path,"points")
        
        images1Path=os.path.join(mfld1Path,"images")
        images2Path=os.path.join(mfld2Path,"images")
        

        
        manifold1Files=remove2([str(d) for d in os.listdir(manifold1Path)],'.DS_Store')
        manifold2Files=remove2([str(d) for d in os.listdir(manifold2Path)],'.DS_Store')
        
        points1Files=remove2([str(d) for d in os.listdir(points1Path)],'.DS_Store')
        points2Files=remove2([str(d) for d in os.listdir(points2Path)],'.DS_Store')
        
        images1Files=remove2([str(d) for d in os.listdir(images1Path)],'.DS_Store')
        images2Files=remove2([str(d) for d in os.listdir(images2Path)],'.DS_Store')
        
        
        documents1Files=remove2([str(d) for d in os.listdir(documents1Path)],'.DS_Store')
        documents2Files=remove2([str(d) for d in os.listdir(documents2Path)],'.DS_Store')
        
     
        if 'register.txt' in (manifold1Files and manifold2Files):
            manifoldPath=os.path.join(destinationPath,"manifold")
            pointsPath=os.path.join(destinationPath,"points")
            documentsPath=os.path.join(destinationPath,"documents")
            
            registerPath1=os.path.join(mfld1Path,"manifold","register.txt")
            registerPath2=os.path.join(mfld2Path,"manifold","register.txt")
            registerPath=os.path.join(destinationPath,"manifold","register.txt")
            
            register1Content= [str(p) for p in readTextFile(registerPath1)]   
            register2Content=[str(p) for p in readTextFile(registerPath2)] 
    
    
            os.mkdir(destinationPath)
            os.mkdir(manifoldPath)
            os.mkdir(pointsPath)
            os.mkdir(documentsPath)

            for c in register1Content:
                appendToText(registerPath,c)
            for c in register2Content:
                if c not in register1Content:
                 appendToText(registerPath,c)
            for p in points1Files:
                try:
                    dirpath=os.path.join(destinationPath,"points",p)
                    ipath=os.path.join(destinationPath,"points",p,"images")
                    spath=os.path.join(destinationPath,"points",p,"sequences")
                    apath=os.path.join(destinationPath,"points",p,"analysis")
                    os.mkdir(dirpath)
                    os.mkdir(ipath)
                    os.mkdir(spath)
                    os.mkdir(apath)
                    isourcepath=os.path.join(mfld1Path,"points",p,"images")
                    #print(isourcepath)
                    #print(ipath)
                    copyFolder(isourcepath,ipath)
                    ssourcepath=os.path.join(mfld1Path,"points",p,"sequences")
                    copyFolder(ssourcepath,spath)

                except:
                    print("%s already in points (1-mfld)" %p)
                    
       
            for p in points2Files:
                try:
                    dirpath=os.path.join(destinationPath,"points",p)
                    ipath=os.path.join(destinationPath,"points",p,"images")
                    spath=os.path.join(destinationPath,"points",p,"sequences")
                    apath=os.path.join(destinationPath,"points",p,"analysis")
                    os.mkdir(dirpath)
                    os.mkdir(ipath)
                    os.mkdir(spath)
                    os.mkdir(apath)
                    isourcepath=os.path.join(mfld2Path,"points",p,"images")
                    copyFolder(isourcepath,ipath)
                    ssourcepath=os.path.join(mfld2Path,"points",p,"sequences")
                    copyFolder(ssourcepath,spath)

                except:
                    print("%s already in points (2-mfld)" %p)
        
                 
                 
        

