#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:12:15 2023

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

specials=[',','.','!',';','"',':','?','-','’','—','”','[',']','(',')','*','“',"'",'¢','‘']

def pdfname(pdf):
    u=pdf.split(".")
    name=u[0]
    for k in range(1,len(u)-1):
        name=name+"."+u[k]
    return name

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

#from wx.lib.pubsub import Publisher


description="Text corpus analysis in the multinomial manifold \n \n 1) text extraction from pdf files \n 2) geodesic distance analysis \n 3) cluster analysis \n 4) kernel based classification \n 5) review and annotation tools \n 6) fractal word ranking. \n \n"
########################################################################
class ViewerPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        
        width, height = wx.DisplaySize()
        self.picPaths =[]
        self.currentPicture = 0
        self.totalPictures = 0
        self.photoMaxSize = height - 200
        self.imagesPath=""
        Publisher.subscribe(self.updateImages, ("update images"))
        #Publisher.subscribe(self.extractImages, ("build viewer"))

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
        folderSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        btnSizer2=wx.BoxSizer(wx.VERTICAL)
        
        img =wx.Image("images/image0.png")
        #wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        

        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
        self.imageLabel = wx.StaticText(self, label="")
        self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
        
        btn = wx.Button(self, label="choose a directory to build assets",size=(350,50))
        btn.Bind(wx.EVT_BUTTON,self.on_choose_folder)
        folderSizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        self.mainSizer.Add(folderSizer, wx.ALL|wx.CENTER, 5)
        
        ######
        
        
        #######
        #self.textLabel=wx.StaticText(self,label=description)
        #textSizer.Add(self.textLabel)
        #self.mainSizer.Add(textSizer, wx.ALL|wx.CENTER, 5)
        
        
        
        btnData = [("Previous", btnSizer, self.onPrevious),
                   ("Slide Show", btnSizer, self.onSlideShow),
                   ("Next", btnSizer, self.onNext)]
        for data in btnData:
            label, sizer, handler = data
            self.btnBuilder(label, sizer, handler)
            
        self.mainSizer.Add(btnSizer, 0, wx.CENTER)
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
        image_name = wx.EmptyImage(240,240)
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

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.imageLabel.SetLabel(image_name)
        self.Refresh()
        Publisher.sendMessage("resize", "")
        
    #----------------------------------------------------------------------
    def nextPicture(self):
        """
        Loads the next picture in the directory
        """
        if self.currentPicture == self.totalPictures-1:
            self.currentPicture = 0
        else:
            self.currentPicture += 1
        self.loadImage(self.picPaths[self.currentPicture])
        
    #----------------------------------------------------------------------
    def previousPicture(self):
        """
        Displays the previous picture in the directory
        """
        if self.currentPicture == 0:
            self.currentPicture = self.totalPictures - 1
        else:
            self.currentPicture -= 1
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
        with wx.DirDialog(self, "Choose a directory 2:",
                          style=wx.DD_DEFAULT_STYLE,
                          ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                
                directory=dlg.GetPath()
                documentsPath=os.path.join(directory,"documents")
                documents=os.listdir(documentsPath)
                names=[pdfname(p) for p in documents]
                folders=[str(d) for d in os.listdir(directory)]
                if '.DS_Store' in documents:
                    documents.remove('.DS_Store')
                if "manifold" not in folders:
                    print("starting to build  manifold")
                    self.picPaths=[os.path.join(directory,"documents",p) for p in documents]
                    mfldDir=os.path.join(directory,"manifold")
                    os.mkdir(mfldDir)
                    pointsDir=os.path.join(directory,"points")
                    os.mkdir(pointsDir)
                    l1="21E8 Text Corpus Analysis in the Multinomial Manifold"
                    l2="Created on "+str(datetime.datetime.now())
                    l3="This folder contains the assets that are required for text corpus analysis based on our multinomial manifold model."
                    l4="To add a new point to this manifold, add the pdf files that you want to include in the manifolds to the documents folder."
                    l5="and type 'pythonw tca.py' on the terminal to start the application."
                    readme=l1+"\n \n"+l2+"\n \n"+l3+"\n \n"+l4+"\n \n"+l5
                    readmePath=os.path.join(directory,"readme.txt")
                    registerPath=os.path.join(directory,"manifold","register.txt")
                    writeToText(readmePath,readme)
                    writeToText(registerPath,"")
                    for name in names:
                        os.mkdir(os.path.join(directory,"points",name))
                    for k in range(len(names)):
                        doc=names[k]
                        pi=os.path.join(directory,"points",doc,"images")
                        ps=os.path.join(directory,"points",doc,"sequences")
                        pa=os.path.join(directory,"points",doc,"analysis")
                        os.mkdir(pi)
                        os.mkdir(ps)
                        os.mkdir(pa)
                        docpath=os.path.join(directory,"documents",doc+".pdf")
                        extractImages(docpath,pi+"/")
                        pageWords=extractTextWords(pi+"/")
                        wordseq=wordSequence(pageWords)
                        wspath=os.path.join(ps+"/","word_sequence.txt")
                        writeSequenceToText(wspath,wordseq)
                        appendToText(registerPath,doc+"\n")
                        print("processing %s is done." %doc)

                    print("multinomial manifold points, page-images and word sequences have been created succesfully \n Manifold is ready for corpus analysis.")
        
                elif "manifold" in folders:
                    print("starting to update manifold")
                    print("******************************************")
                    registerPath=os.path.join(directory,"manifold","register.txt")
                    rawNames=readTextFile(registerPath)
                    oldNames=[p.split("\n")[0] for p in rawNames]
                    newNames=[]
                    for p in names:
                        if p not in oldNames:
                            newNames.append(p)
                    if "" in newNames:
                        newNames.remove("")
                    for name in newNames:
                        os.mkdir(os.path.join(directory,"points",name))
                    if len(newNames)>0:
                        for k in range(len(newNames)):
                            doc=newNames[k]
                            print("doc",doc)
                            pi=os.path.join(directory,"points",doc,"images")
                            ps=os.path.join(directory,"points",doc,"sequences")
                            pa=os.path.join(directory,"points",doc,"analysis")
                            os.mkdir(pi)
                            os.mkdir(ps)
                            os.mkdir(pa)
                            docpath=os.path.join(directory,"documents",doc+".pdf")
                            extractImages(docpath,pi+"/")
                            pageWords=extractTextWords(pi+"/")
                            wordseq=wordSequence(pageWords)
                            wspath=os.path.join(ps+"/","word_sequence.txt")
                            writeSequenceToText(wspath,wordseq)
                            appendToText(registerPath,doc+"\n")
                            print("processing %s is done." %doc)
                        
                        print("new points have been added to manifold. Manifold is ready for analysis.")
                    else:
                        print("  ")
                        print("There are not new records to update. Manifold is ready for analysis")

                  

                    
        
        
########################################################################
class ViewerFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Text Corpus Builder")
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
dirPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/A"
paths=os.listdir(dirPath)
os.mkdir
"""


#%%