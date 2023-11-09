#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 09:41:45 2023

@author: 21e8
"""

import wx

from wx.adv import Wizard
#import wizard

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
    wizard=wx.adv.Wizard(None,-1,"Simple Wizard \n")
    page1=TitlePage(wizard,"page1 \n")
    page1.SetBackgroundColour('Green')
    page2=TitlePage(wizard,"page2")
    page3=TitlePage(wizard,"page3")
    page4=TitlePage(wizard,"page4")
    page1.Sizer.Add(wx.StaticText(page1,-1,"\n\n Testing the wizard1 \n"))
    page1.Sizer.Add(wx.StaticText(page1,-1,"\n Testing the wizard2 \n"))
    page4.Sizer.Add(wx.StaticText(page4,-1,"\n This is the last page."))
    img = wx.Image('maze.png', wx.BITMAP_TYPE_ANY)
    sb1 = wx.StaticBitmap(page2, -1, wx.BitmapFromImage(img))
    sb2 = wx.StaticBitmap(page2, -1, wx.BitmapFromImage(img))
    button=wx.Button(page3,-1,"Click Me",pos=(50,50))
    button1=wx.Button(page1,-1,"Click Me",pos=(50,50))
    page2.Sizer.Add(sb1)
    page2.Sizer.Add(sb2)
    page3.Sizer.Add(button)
    page1.Sizer.Add(button1)
    page1.Chain(page2).Chain(page3).Chain(page4)
    wizard.FitToPage(page1)
    if wizard.RunWizard(page1):
        print('success')
    #app.MainLoop()