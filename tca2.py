#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 12 oct 2023

@author: 21e8
"""
import datetime
import glob
import os
import wx

from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

import pytesseract
from PIL import Image 
from pdf2image import convert_from_path
import numpy as np

from PIL import Image, ImageDraw, ImageFont
import seaborn as sns
import matplotlib.pyplot as plt

specials=[',','.','!',';','"',':','?','-','’','—','”','[',']','(',')','*','“',"'",'¢','‘']

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
    
def writeToText(path,text):
    with open(path, 'w') as f:
        f.write(text)
    f.close()
        
def appendToText(path,text):
    with open(path, 'a') as f:
        f.write(text)
    f.close()
    
def writeSequenceToText(path,seq):
    with open(path, 'w') as f:
        lines=[str(p)+"\n" for p in seq]
        f.writelines(lines)
    f.close()    

def readText(path,text):
    with open(path) as f:
        lines = f.readlines()
    return lines

def readTextFile(path_to_file):
    with open(path_to_file) as f:
        contents = f.readlines()
    f.close()
    return contents

def extractImages(pdfpath,pdirectory):
    images = convert_from_path(pdfpath)
    for i in range(len(images)):
        images[i].save(pdirectory+'/page'+ str(100000+i) +'.png', 'PNG') 

def extractPageWords(indirectory,page):
    paths=sorted(os.listdir(indirectory))
    path=indirectory+paths[page]
    im=Image.open(path)
    text = pytesseract.image_to_string(im)
    words=text.split()
    return words

def extractTextWords(directory):
    pagePaths=sorted(os.listdir(directory))
    pageWords={}
    for k in range(len(pagePaths)):
        pageWords[k]=extractPageWords(directory,k)
    return pageWords

def removePuntuation(word):
    w=word
    n=len(word)
    while w[-1] in specials:
        if n>1:
            n=n-1
            w=word[0:n]
        else:break
    counter=0
    while w[0] in specials:
        if len(w)==1:break
        counter+=1
        w=word[counter:n]
    return w
        
def cleanWord(word):
    w=removePuntuation(word.lower())
    return w

def wordSequence(pagewords):
    n=len(pagewords.keys())
    seq=[]
    for k in range(n):
        for word in pagewords[k]:
            if len(word)>1:
                seq.append(cleanWord(word))
    return seq

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

        
cgPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images/corpusGraph.png"
chmPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images/corpusDistanceHeatMap.png"
cwcPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images/corpusWordCounts.png"
imagesPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/images"

sizes=[30,50,100,70,80,70,70,65]

#from wx.lib.pubsub import Publisher





class ViewerPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        width, height = wx.DisplaySize()
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
        Publisher.subscribe(self.updateImages, ("update images"))

        self.slideTimer = wx.Timer(None)
        self.slideTimer.Bind(wx.EVT_TIMER, self.update)
        
        self.layout()
        
    #----------------------------------------------------------------------
    def layout(self):
        """
        Layout the widgets on the panel
        """
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.BoxSizer(wx.VERTICAL)

        
        img =wx.Image("images/corpusGraph.png")
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        

        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
        self.imageLabel = wx.StaticText(self, label="")
        self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
        
        
        btnData = [("previous", btnSizer, self.onPrevious),
                   ("next", btnSizer, self.onNext)]
        for data in btnData:
            label, sizer, handler = data
            self.btnBuilder(label, sizer, handler)
            
        self.mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)
        
        
        btn = wx.Button(self, label="new analysis / enter directory",size=(350,50))
        btn.Bind(wx.EVT_BUTTON,self.on_choose_folder)
        self.mainSizer.Add(btn, 0, wx.ALL|wx.CENTER, 2)
        self.mainSizer.Add(textSizer, wx.ALL|wx.CENTER, 5)
        self.SetSizer(self.mainSizer)
        
   
    #----------------------------------------------------------------------
    def btnBuilder(self, label, sizer, handler):
        """
        Builds a button, binds it to an event handler and adds it to a sizer
        """
        btn = wx.Button(self, label=label)
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        
    #----------------------------------------------------------------------
    def loadImage(self, image):
        """"""
        #image_name = wx.Image(240,240)
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.photoMaxSize
            NewH = self.photoMaxSize * H / W
        else:
            NewH = self.photoMaxSize
            NewW = self.photoMaxSize * W / H
        img = img.Scale(NewW,NewH)

        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        #self.imageLabel.SetLabel(image_name)
        self.Refresh()
        Publisher.sendMessage("resize", "")
        
    #----------------------------------------------------------------------
    def nextPicture(self):
        """
        Loads the next picture in the directory
        """

        if self.currentPicture >= self.totalPictures-1:
            self.currentPicture=0 
        else:
            self.currentPicture=self.currentPicture+1
        #print(self.currentPicture,self.picPaths[self.currentPicture])
        self.loadImage(self.picPaths[self.currentPicture])
        
    #----------------------------------------------------------------------
    def previousPicture(self):
        """
        Displays the previous picture in the directory
        """
        if self.currentPicture==0:
            self.currentPicture = self.totalPictures-1
        else:
            self.currentPicture= self.currentPicture-1
        print(self.currentPicture,self.picPaths[self.currentPicture])
        self.loadImage(self.picPaths[self.currentPicture])
        
    #----------------------------------------------------------------------
    def update(self, event):
        """
        Called when the slideTimer's timer event fires. Loads the next
        picture from the folder by calling th nextPicture method
        """
        self.nextPicture()
        
    #----------------------------------------------------------------------
    def updateImages(self, msg):
        """
        Updates the picPaths list to contain the current folder's images
        """
        self.picPaths = msg.data
        self.totalPictures = len(self.picPaths)
        self.loadImage(self.picPaths[0])
        
    #----------------------------------------------------------------------
    def onNext(self, event):
        """
        Calls the nextPicture method
        """
        self.nextPicture()
    
    #----------------------------------------------------------------------
    def onPrevious(self, event):
        """
        Calls the previousPicture method
        """
        self.previousPicture()
    
    #----------------------------------------------------------------------
    def onSlideShow(self, event):
        """
        Starts and stops the slideshow
        """
        btn = event.GetEventObject()
        label = btn.GetLabel()
        if label == "Slide Show":
            self.slideTimer.Start(3000)
            btn.SetLabel("Stop")
        else:
            self.slideTimer.Stop()
            btn.SetLabel("Slide Show")
            
    def extractImages(self,event):
        path=event.GetPath()
        print("folder path:",path)
        
    
    #----------------------------------------------------------------------
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
               



        
########################################################################
class ViewerFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="TCA")
        panel = ViewerPanel(self)
        self.folderPath = ""
        Publisher.subscribe(self.resizeFrame, ("resize"))
        
        #self.initToolbar()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.Show()
        self.sizer.Fit(self)
        self.Center()
        
        
    #----------------------------------------------------------------------
    def initToolbar(self):
        """
        Initialize the toolbar
        """
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        
        open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
        
        self.toolbar.Realize()
        
    #----------------------------------------------------------------------
    def onOpenDirectory(self, event):
        """
        Opens a DirDialog to allow the user to open a folder with pictures
        """
        dlg = wx.DirDialog(self, "Choose a directory",
                           style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.folderPath = dlg.GetPath()
            print(self.folderPath)
            picPaths = glob.glob(self.folderPath + "\\*.jpg")
            print(picPaths)
        Publisher.sendMessage("update images", picPaths)
        
    #----------------------------------------------------------------------
    def resizeFrame(self, msg):
        """"""
        self.sizer.Fit(self)
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = ViewerFrame()
    app.MainLoop()
    
    
#%%

    

"""
directory="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books"
pointsFolderPath=os.path.join(directory,"points")
pointsPaths=os.listdir(pointsFolderPath)
if '.DS_Store' in pointsPaths:
    pointsPaths.remove('.DS_Store')
sequences={}
for name in pointsPaths:
    seqpath=os.path.join(directory,"points",name,"sequences","word_sequence.txt")
    seq=[s.split('\n')[0] for s in readTextFile(seqpath)]
    sequences[name]=seq

updateCorpusGraph(cgPath,[len(sequences[name]) for name in pointsPaths])

"""

#%%