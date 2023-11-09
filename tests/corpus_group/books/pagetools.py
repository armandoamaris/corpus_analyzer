#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:07:51 2023

@author: 21e8
"""

import wx
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns
import matplotlib.pyplot as plt


def drawWCircle(img_draw,center,radius,sizes,minNodeSize,maxNodeSize):
    n=len(sizes)
    points=[[center[0]+radius*np.cos(2*np.pi*k/n),center[1]+radius*np.sin(2*np.pi*k/n)] for k in range(n)]
    slope=(maxNodeSize-minNodeSize)/(max(sizes)-min(sizes))
    for k in range(len(points)):
        x=points[k][0]
        y=points[k][1]
        pointSize=slope*(sizes[k]-min(sizes))+minNodeSize
        img_draw.ellipse((x-pointSize/2, y-pointSize/2, x+pointSize/2, y+pointSize/2),fill="blue")
        fnt = ImageFont.truetype('Arial',8)
        #img_draw.text((x-0.1*pointSize,y-0.3*pointSize),str(k), fill='white')
        img_draw.text((x-4,y-5),str(k), fill='white')

def readTextFile(path_to_file):
    with open(path_to_file) as f:
        contents = f.readlines()
    f.close()
    return contents

# geodesic distance in the multinomial manifold
def geodesicDistance0(coords1,coords2):
    c1=[np.sqrt(x) for x in coords1]
    c2=[np.sqrt(x) for x in coords2]
    p=[]
    if len(coords1)==len(coords2):
        p=[c1[k]*c2[k] for k in range(len(coords1))]
        w=min(sum(p),1)
        d=2*np.arccos(np.sqrt(w))
    else:
        print
        ("this function is defined only for simplex-coordinates of the same dimension.")
    return d

def updateCorpusGraph(inpath,sizes):
    img = Image.new('RGB', (400, 400), 'black')
    img_draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('Arial',15)
    img_draw.text((150, 20), 'Text Corpus Graph', fill='white',font=fnt)
    #vspace=15
    center=[200,200]
    minNodeSize=20
    maxNodeSize=40
    R=100
    drawWCircle(img_draw,center,R,sizes,minNodeSize,maxNodeSize)
    img.save(inpath)
    #img.show()  

imagesPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images"
cgPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images/corpusGraph.png"
chmPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images/corpusDistanceHeatMap.png"
cwcPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images/corpusWordCounts.png"

class imagePage(wx.adv.WizardPageSimple):
    
    def __init__(self,parent,folder):
        wx.adv.WizardPageSimple.__init__(self,parent)
        width, height = wx.DisplaySize()
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        ripaths=os.listdir(imagesPath)
        if "image0.png" in ripaths:
            ripaths.remove("image0.png")
        if '.DS_Store' in ripaths:
            ripaths.remove('.DS_Store')
        pics=[os.path.join(imagesPath, p) for p in ripaths]
        self.picPaths =pics
        self.currentPicture = 0
        self.totalPictures =len(self.picPaths)
        self.photoMaxSize = height - 200
        self.imagesPath=""
        #Publisher.subscribe(self.Next, ("update images"))
        #Publisher.subscribe(self.Previous, ("update images"))
        #self.slideTimer = wx.Timer(None)
        #self.slideTimer.Bind(wx.EVT_TIMER, self.update)
        
        img = wx.Image(self.picPaths[self.currentPicture ], wx.BITMAP_TYPE_ANY)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        #sb1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(img))
        self.sizer.Add(self.imageCtrl,wx.ALL|wx.CENTER, 5)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(self, label="back")
        btn2 = wx.Button(self, label="next")
        btn1.Bind(wx.EVT_BUTTON,self.onPrevious)
        btn2.Bind(wx.EVT_BUTTON,self.onNext)
        btnSizer.Add(btn1,wx.ALL|wx.CENTER, 5)
        btnSizer.Add(btn2,wx.ALL|wx.CENTER, 5)
        self.sizer.Add(btnSizer,wx.ALL|wx.CENTER, 5)
        self.sizer.Add(wx.StaticLine(self,-1),0,wx.EXPAND|wx.ALL,5)
        
        textSizer = wx.BoxSizer(wx.VERTICAL)
        btn = wx.Button(self, label="new analysis / enter directory",size=(350,50))
        btn.Bind(wx.EVT_BUTTON,self.on_choose_folder)
        self.sizer.Add(btn, 0, wx.ALL|wx.CENTER, 2)
        self.sizer.Add(textSizer, wx.ALL|wx.CENTER, 5)
        #self.SetSizer(self.mainSizer)
        
    def onNext(self,event):
        if self.currentPicture >= self.totalPictures-1:
            self.currentPicture=0 
        else:
            self.currentPicture=self.currentPicture+1
        print(self.currentPicture,self.picPaths[self.currentPicture])
        img = wx.Image(self.picPaths[self.currentPicture ], wx.BITMAP_TYPE_ANY)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()
        #Publisher.sendMessage("resize", "")
        
    def onPrevious(self,event):
        if self.currentPicture==0:
            self.currentPicture = self.totalPictures-1
        else:
            self.currentPicture= self.currentPicture-1
        print(self.currentPicture,self.picPaths[self.currentPicture])
        img = wx.Image(self.picPaths[self.currentPicture ], wx.BITMAP_TYPE_ANY)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()
        #Publisher.sendMessage("resize", "")

    def updateImages(self, msg):
        self.picPaths = msg.data
        self.totalPictures = len(self.picPaths)
        self.loadImage(self.picPaths[0])
        
    def on_choose_folder(self, event):
        with wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE,
                          ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                
                directory=dlg.GetPath()
                folders=[str(d) for d in os.listdir(directory)]

                if "manifold" not in folders:
                    line1="Manifold data was not found.\n"
                    line2="To continue with corpus analysis you have several choices:\n"
                    line3="a) choose another directory with valid corpus manifold data" 
                    line4="b) return to the TCA builder page to create a new corpus manifold."
                    print("=========================================================================")
                    print(line1+"\n"+line2+"\n"+line3+"\n"+line4)
                    print("=========================================================================")

                    
                elif "manifold" and "images" and "points" in folders:
                    print("TCA is building analysis...")
                    print("******************************************")
                    sequences={}
                    vocabulary=[]
                    
                    
                    registerPath=os.path.join(directory,"manifold","register.txt")
                    pointsFolderPath=os.path.join(directory,"points")
                    pointsPaths=os.listdir(pointsFolderPath)
                    names=[w.split("\n")[0] for w in readTextFile(registerPath)]
                    if '.DS_Store' in pointsPaths:
                        pointsPaths.remove('.DS_Store')
                    
                    for name in pointsPaths:
                        seqpath=os.path.join(directory,"points",name,"sequences","word_sequence.txt")
                        seq=[s.split('\n')[0] for s in readTextFile(seqpath)]
                        sequences[name]=seq
                        vocabulary=list(set(vocabulary+list(seq)))
                        
                    vocabulary=sorted(vocabulary)
                    
                    tf_coordinates={name:[0 for w in vocabulary] for name in pointsPaths} # simple TF representation of a text in a corpus
                    
                    tfidf_coordinates={name:[0 for w in vocabulary] for name in pointsPaths}
                    
                    wordIDF={word:0 for word in vocabulary}
                    
                    for word in wordIDF.keys():
                        for name in sequences.keys():
                            if word in sequences[name]:
                                wordIDF[word]=wordIDF[word]+(1/len(pointsPaths))
                    
                    wordPosition={}
                    for k in range(len(vocabulary)):
                        wordPosition[vocabulary[k]]=k

                    for name in pointsPaths:
                        for word in sequences[name]:
                            tf_coordinates[name][wordPosition[word]]=tf_coordinates[name][wordPosition[word]]+1
                            #tfidf_coordinates[name][wordPosition[word]]=(tfidf_coordinates[name][wordPosition[word]]+1)*np.log((len(pointsPaths)/wordIDF[word])) #nans are produced during computation check problem 
                            
                        tf_coordinates[name]=np.array(tf_coordinates[name])/sum(np.array(tf_coordinates[name]))
                        #tfidf_coordinates[name]=np.array(tfidf_coordinates[name])/sum(np.array(tfidf_coordinates[name]))  
                        
                    tf_distances=np.zeros((len(pointsPaths),len(pointsPaths)))
                    #tfidf_distances=np.zeros((len(pointsPaths),len(pointsPaths)))   
                    for i in range(len(pointsPaths)):
                        for j in range(len(pointsPaths)):
                            name1=pointsPaths[i]
                            name2=pointsPaths[j]
                            tf_distances[i,j]=geodesicDistance0(tf_coordinates[name1],tf_coordinates[name2])
                            #tfidf_distances[i,j]=geodesicDistance0(tfidf_coordinates[name1],tfidf_coordinates[name2])
                    print(pointsPaths)        
                    #print("tf distances",tf_distances)
                    #print("tfidf distances",tfidf_distances)
                    updateCorpusGraph(cgPath,[len(sequences[name]) for name in pointsPaths])
                    
                    hm= sns.heatmap(tf_distances, linewidth=0.5)
                    
                    plt.title("Corpus manifold-distance heatmap")
                    plt.savefig(chmPath)
                    plt.close('all')

                    plt.bar(range(len(pointsPaths)),[len(set(sequences[name])) for name in pointsPaths])
                    plt.title("document's word counts")
                    plt.savefig(cwcPath)
                    plt.close()
                    

                    
                    newimg =wx.Image(chmPath)
                    self.imageCtrl.SetBitmap(wx.Bitmap(cwcPath)) 
