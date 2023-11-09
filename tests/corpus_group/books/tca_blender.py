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


from wx.lib.pubsub import pub as Publisher


import shutil


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
        self.slideTimer = wx.Timer(None)
        self.layout()
        
        self.sourceFolder=""
        self.destination=""
        
    def layout(self):
        """
        Layout the widgets on the panel
        """
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        folderSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        img =wx.Image("images/merger.png")
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        

        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
        self.imageLabel = wx.StaticText(self, label="")
        self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
        

        self.mainSizer.Add(folderSizer, wx.ALL|wx.CENTER, 5)
        
        
        btnData = [("choose corpus group folder", btnSizer, self.on_choose_folder),
                   ("choose destination folder", btnSizer, self.on_choose_folder2),
                   ("blend", btnSizer, self.on_blend)]
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
        

    def on_choose_folder(self, event):
        with wx.DirDialog(self, "Choose a directory 2:",
                          style=wx.DD_DEFAULT_STYLE,
                          ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.sourceFolder=dlg.GetPath()
                #print("source",self.sourceFolder)
                
    def on_choose_folder2(self, event):
        with wx.DirDialog(self, "Choose a directory 2:",
                           style=wx.DD_DEFAULT_STYLE,
                           ) as dlg:
             if dlg.ShowModal() == wx.ID_OK:
                 self.destination=dlg.GetPath()
                 #print("destination",self.destination)
                 
    def on_blend(self, event):
        print("corpus blending process starting")
        print("source",self.sourceFolder)
        print("destination",self.destination)
        print("corpuses fusion ended succesfully.")
                
                  

class ViewerFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Text Corpus Blender")
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
        
        
    #----------------------------------------------------------------------
    def resizeFrame(self, msg):
        """"""
        self.sizer.Fit(self)
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = ViewerFrame()
    app.MainLoop()
    
    
