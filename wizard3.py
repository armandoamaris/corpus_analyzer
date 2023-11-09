#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:05:15 2023

@author: 21e8
"""


import wx

from wx.adv import Wizard

import glob
import os

from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

import pytesseract
from pdf2image import convert_from_path
import numpy as np

from PIL import Image, ImageDraw, ImageFont
import seaborn as sns
import matplotlib.pyplot as plt

import pagetools as pag
import pagetools1 as pag1
import pagetools2 as pag2

mazePath="images/bondOfUnion.png"


#"/Users/21e8/Desktop/PythonProjects/hdc-based-handwriting-Recognition/books/bondOfUnion.png"


description="Text corpus analysis in the multinomial manifold \n \n 1) text extraction from pdf files \n 2) geodesic distance analysis \n 3) cluster analysis \n 4) kernel based classification \n 5) review and annotation tools \n 6) sentiment analysis. \n \n"

class TitlePage(wx.adv.WizardPageSimple):
    
    def __init__(self,parent,title):
        wx.adv.WizardPageSimple.__init__(self,parent)
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText=wx.StaticText(self,-1,title)
        titleText.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))
        self.sizer.Add(wx.StaticLine(self,-1),0,wx.EXPAND|wx.ALL,5)
        
 

        
if __name__=="__main__":
    app=wx.App()
    wizard=wx.adv.Wizard(None,-1,"Corpus Analyzer \n")
    
    
    ########################################
    # page1
    ########################################
    page1=TitlePage(wizard,"")    
    btnSizer = wx.BoxSizer(wx.HORIZONTAL)
    textSizer = wx.BoxSizer(wx.VERTICAL)
    
    img =wx.Image(mazePath) #wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
    page1.imageCtrl = wx.StaticBitmap(page1, wx.ID_ANY, 
                                     wx.Bitmap(img))
    page1.Sizer.Add(page1.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
    page1.imageLabel = wx.StaticText(page1, label="")
    page1.Sizer.Add(page1.imageLabel, 0, wx.ALL|wx.CENTER, 5)

    page1.textLabel=wx.StaticText(page1,label=description)
    page1.Sizer.Add(page1.textLabel)
    page1.Sizer.Add(textSizer, wx.ALL|wx.CENTER, 5)
    
    
    ########################################
    # page2
    ########################################
    
    page2=pag.imagePage(wizard,"")

    ########################################
    # page3
    ########################################
    
    
    page3=pag2.ReviewerFrame(wizard)#TitlePage(wizard,"document reviewer") 
    
    ########################################
    # page4
    ########################################
    page4=TitlePage(wizard,"document classification")
    page4.Sizer.Add(wx.StaticText(page4,-1,"\n 1) manifold kernel based SVM classification"))
    page4.Sizer.Add(wx.StaticText(page4,-1,"\n 2) python/skelearn implementation"))
    page4.Sizer.Add(wx.StaticText(page4,-1,"\n."))
    
    
    
    ########################################
    # make chain area
    ########################################
    page1.Chain(page2).Chain(page3).Chain(page4)
    wizard.FitToPage(page1)
    
    
    
    
    
    if wizard.RunWizard(page1):
        print('success')
    #app.MainLoop()