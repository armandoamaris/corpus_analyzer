#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 10:17:06 2023

@author: 21e8
"""




import glob
import os
import wx
from wx.lib.pubsub import pub as Publisher #use pypubsub, available on PyPI
import pytesseract
from PIL import Image 
from datetime import datetime
import json


def wreview(reviewer,mytime,review):
    wr=[reviewer,mytime,review.replace("\n","")]
    return wr

def writeToText(path,text):
    with open(path, 'w') as f:
        f.write(text)
    f.close()
        
def appendToText(path,text):
    with open(path, 'a') as f:
        f.write(text)
    f.close()

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

pointsPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/Books/points"
imagesPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/Books/points/alice/images"
description="Text corpus analysis in the multinomial manifold \n \n 1) text extraction from pdf files \n 2) geodesic distance analysis \n 3) cluster analysis \n 4) kernel based classification \n 5) review and annotation tools \n 6) fractal word ranking. \n \n"
reviewPath="/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/Books/manifold/reviews.txt"

ppaths=os.listdir(pointsPath)

class ViewerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        ripaths=os.listdir(imagesPath)
        if '.DS_Store' in ripaths:
            ripaths.remove('.DS_Store')
        pics=[os.path.join(imagesPath, p) for p in ripaths]
        
        width, height = wx.DisplaySize()
        self.picPaths=sorted(pics)
        self.currentPicture = 0
        self.totalPictures =len(self.picPaths)
        self.photoMaxSize = height - 200
        self.imagesPath=""
        self.reviewPath=""
        self.document=""
        Publisher.subscribe(self.updateImages, ("update images"))

        self.slideTimer = wx.Timer(None)
        self.slideTimer.Bind(wx.EVT_TIMER, self.update)
        
        self.layout()
        
    def layout(self):
        self.reviewer=""
        self.MaxImageSize=600
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.BoxSizer(wx.VERTICAL)
        self.folderSizer = wx.BoxSizer(wx.VERTICAL) #wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        
        reviewSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer2=wx.BoxSizer(wx.VERTICAL)
        self.imageSizer = wx.BoxSizer(wx.VERTICAL)
        
        reviewerSizer=wx.FlexGridSizer(cols=2,hgap=6,vgap=6)
        
        reviewLabel=wx.StaticText(self,-1,"reviewer:")
        reviewText=wx.TextCtrl(self,-1,"",size=(200,20)) #,size=(175,-1))
        reviewText.SetInsertionPoint(0)
        reviewText.Bind(wx.EVT_TEXT,self.getReviewer)
        docLabel=wx.StaticText(self,-1,"document:")
        docbtn = wx.Button(self, label="choose folder here",size=(200,20)) #
        docbtn.Bind(wx.EVT_BUTTON,self.on_choose_document)
        sliderLabel=wx.StaticText(self,-1,"page")
        self.slider = wx.Slider(self, minValue=0, maxValue=self.totalPictures,style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.slider.Bind(wx.EVT_SLIDER, self.sliderAction)
        reviewerSizer.AddMany([reviewLabel,reviewText,docLabel,docbtn,sliderLabel,self.slider])
        self.mainSizer.Add(reviewerSizer, wx.ALL|wx.CENTER, 5)
        self.Img = wx.Image(self.picPaths[self.currentPicture], wx.BITMAP_TYPE_ANY)
        self.imageCtrl =wx.StaticBitmap(self, bitmap=wx.Bitmap(self.MaxImageSize, self.MaxImageSize)) #wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.Img))
        self.imageSizer.Add(self.imageCtrl)#, 0, wx.ALL|wx.CENTER, 5)
        self.mainSizer.Add(self.imageSizer,wx.ALL|wx.CENTER, 5)
        self.review = wx.TextCtrl(self, size=(600,400),style = wx.TE_MULTILINE)
        self.review.Bind(wx.EVT_TEXT,self.OnKeyTyped) 
        self.Bind(wx.EVT_BUTTON, self.OnSubmit) 
        self.reviewButton = wx.Button(self, label="submit review",size=(180,20))

        reviewSizer.Add(self.review,wx.ALL|wx.CENTER, 5)
        reviewSizer.Add(self.reviewButton,0, wx.ALL|wx.CENTER, 5)
        self.mainSizer.Add(reviewSizer,wx.ALL|wx.CENTER, 5)
        
        self.mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)
        
    def getReviewer(self, event): 
      reviewer=event.GetString()
      self.reviewer=reviewer
      self.Refresh
      
    def OnKeyTyped(self, event): 
      review=event.GetString()
      
    def OnSubmit(self, event): 
     
      review=self.review.GetValue()
      review=review.split("\n")
      sreview=review[0]
      for w in range(1,len(review)):
          sreview=sreview+","+str(w)
      wr=str(datetime.now())+","+str(self.document)+","+str(self.currentPicture)+","+str(self.reviewer)+","+sreview+"\n"
      with open(reviewPath, "a") as outfile:
         outfile.write(wr)
      print("review was submitted")
      event.Skip()
    
    def sliderAction(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        self.currentPicture=value
        
        Img = wx.Image(self.picPaths[self.currentPicture], wx.BITMAP_TYPE_ANY)
        
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = self.MaxImageSize
            NewH = self.MaxImageSize * H / W
        else:
            NewH = self.MaxImageSize
            NewW = self.MaxImageSize * W / H
        Img = Img.Scale(int(NewW),int(NewH),quality=wx.IMAGE_QUALITY_HIGH)
        self.imageCtrl.SetBitmap(wx.Bitmap(Img))
        self.Refresh()
                
    def on_choose_document(self, event):
        with wx.DirDialog(self, "Choose a folder:",
                          style=wx.DD_DEFAULT_STYLE,
                          ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory=dlg.GetPath()
                imagesPath=os.path.join(directory,"images")
                dp1=directory.split("/")
                dp2=""
                for k in range(len(dp1)-2):
                    dp2=dp2+dp1[k]+"/"
                reviewPath=dp2+"manifold/reviews.json"
        self.document=dp1[-1]
        print("doc: ",self.document)        
        ripaths=os.listdir(imagesPath)
        if '.DS_Store' in ripaths:
            ripaths.remove('.DS_Store')
        pics=[os.path.join(imagesPath, p) for p in ripaths]
        self.picPaths=sorted(pics)
        self.reviewPath=reviewPath
        self.slider.Max=len(self.picPaths)-1
        self.Refresh()
                             
    def on_choose_folder(self, event):
        with wx.DirDialog(self, "Choose a directory 2:",
                          style=wx.DD_DEFAULT_STYLE,
                          ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory=dlg.GetPath()
                self.picPaths=[os.path.join(directory,p) for p in sorted(os.listdir(directory))]
                print("directory",directory)
                for k in range(len(self.picPaths)):
                    print("k=%s %s" %(k,self.picPaths[k]))
                
    def btnBuilder(self, label, sizer, handler):
        btn = wx.Button(self, label=label)
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)

    def loadImage(self, image):
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
        
    def nextPicture(self):
        if self.currentPicture == self.totalPictures-1:
            self.currentPicture = 0
        else:
            self.currentPicture += 1
        self.loadImage(self.picPaths[self.currentPicture])

    def previousPicture(self):
        if self.currentPicture == 0:
            self.currentPicture = self.totalPictures - 1
        else:
            self.currentPicture -= 1
        self.loadImage(self.picPaths[self.currentPicture])
        
    def update(self, event):
        self.nextPicture()

    def updateImages(self, msg):
        self.picPaths = msg.data
        self.totalPictures = len(self.picPaths)
        self.loadImage(self.picPaths[0])
        
    def onNext(self, event):
        self.nextPicture()

    def onPrevious(self, event):
        self.previousPicture()

    def onSlideShow(self, event):
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
        
class ReviewerFrame(wx.adv.WizardPageSimple):
    def __init__(self,parent):
        #wx.Frame.__init__(self, None, title="reviewer's area")
        wx.adv.WizardPageSimple.__init__(self,parent)
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
        panel = ViewerPanel(self)
        self.folderPath = ""
        Publisher.subscribe(self.resizeFrame, ("resize"))

        #self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(panel,wx.ALL|wx.CENTER, 5)

        
    def initToolbar(self):
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        
        open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
        
        self.toolbar.Realize()
        
    def onOpenDirectory(self, event):
        dlg = wx.DirDialog(self, "Choose a directory",
                           style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.folderPath = dlg.GetPath()
            print(self.folderPath)
            picPaths = glob.glob(self.folderPath + "\\*.jpg")
            print(picPaths)
        Publisher.sendMessage("update images", picPaths)

    def resizeFrame(self, msg):
        self.sizer.Fit(self)


    
    

