#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Emerson Grabke (2014)
# Written in Python 2.7.6

# Special thanks to:
# WxGlade for the basic GUI layout
# PYPDF (Copyright 2006, Mathieu Fenniak, Copyright 2007, Ashish Kulkarni)
# Bryan Helmig for the Crossword algorithm (Copyright 2010, Bryan Helmig)
# And rboulton (through GitHub) for the Wordsearch algorithm!

# In accordance with copyrights, this software is free to use and distribute"

import wx
import wx.lib.filebrowsebutton as fbb
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib import utils
from reportlab.platypus import Frame, Image
import random, re, time, string
from copy import copy as duplicate
import StringIO
from win32api import LoadResource
#import os
#import io
from pyPdf import pdf
#from PyPDF import PdfFileMerger, PdfFileReader

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        m_load = wxglade_tmp_menu.Append(wx.ID_OPEN, _("&Open"), _("Load Inputs from File"), wx.ITEM_NORMAL)
        m_saveas = wxglade_tmp_menu.Append(wx.ID_SAVEAS, _("&Save As"), _("Save Inputs to File"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        m_about = wxglade_tmp_menu.Append(wx.ID_ABOUT, _("&About"), _("About this application"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        m_exit = wxglade_tmp_menu.Append(wx.ID_EXIT, _("E&xit"), _("Exit program"), wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, _("&File"))
        wxglade_tmp_menu = wx.Menu()
        m_clear = wxglade_tmp_menu.Append(wx.ID_CLEAR, _("&Clear All"), _("Clear all fields"), wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Edit"))

        wxglade_tmp_menu = wx.Menu()
        m_readme = wxglade_tmp_menu.Append(wx.ID_HELP, _("&Readme"), _("Instructions on Using This Program"), wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Help"))
        
        self.SetMenuBar(self.frame_1_menubar)
        self.Bind(wx.EVT_MENU, self.OnLoad, m_load)
        self.Bind(wx.EVT_MENU, self.OnSave, m_saveas)
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        self.Bind(wx.EVT_MENU, self.OnClear, m_clear)
        self.Bind(wx.EVT_MENU, self.OnReadme, m_readme)
        # Menu Bar end

        maxlength = 30
        maxword = 0
        
        self.statusbar = self.CreateStatusBar(1, 0)
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_1.SetMinSize((750,650))
        self.label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Activity Book Generator for Seniors with Anomic Aphasia"))
        self.static_line_3 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        self.module = wx.StaticText(self.panel_1, wx.ID_ANY, _("Module Name: "))
        self.text_module = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.panel_module_1 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.panel_module_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Word to Learn"))
        self.label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Description of Word"))
        self.label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Photo (if applicable)"))
        self.label_14 = wx.StaticText(self.panel_1, wx.ID_ANY, _("1)"))
        self.text_ctrl_5 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_5.SetMaxLength(maxword)
        self.text_ctrl_15 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_15.SetMaxLength(maxlength)


        FILEMASK = "Image Files (*.jpeg)|*.jpg;*.jpeg;*.jpe;"\
                   "|All Files (*.*)|*.*;"
        
        self.button_3 = fbb.FileBrowseButton(
                self.panel_1,
                labelText = "Image:",
                fileMask = FILEMASK,
                fileMode = wx.OPEN | wx.FILE_MUST_EXIST,
            )
        
        self.label_15 = wx.StaticText(self.panel_1, wx.ID_ANY, _("2)"))
        self.text_ctrl_6 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_6.SetMaxLength(maxword)
        self.text_ctrl_16 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_16.SetMaxLength(maxlength)
        
        self.button_4 = fbb.FileBrowseButton(
                self.panel_1,
                labelText = "Image:",
                fileMask = FILEMASK,
                fileMode = wx.OPEN | wx.FILE_MUST_EXIST,
            )
        
        self.label_16 = wx.StaticText(self.panel_1, wx.ID_ANY, _("3)"))
        self.text_ctrl_7 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_7.SetMaxLength(maxword)
        self.text_ctrl_17 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_17.SetMaxLength(maxlength)
        
        self.button_5 = fbb.FileBrowseButton(
                self.panel_1,
                labelText = "Image:",
                fileMask = FILEMASK,
                fileMode = wx.OPEN | wx.FILE_MUST_EXIST,
            )
        
        self.label_17 = wx.StaticText(self.panel_1, wx.ID_ANY, _("4)"))
        self.text_ctrl_8 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_8.SetMaxLength(maxword)
        self.text_ctrl_18 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_18.SetMaxLength(maxlength)
        
        self.button_6 = fbb.FileBrowseButton(
                self.panel_1,
                labelText = "Image:",
                fileMask = FILEMASK,
                fileMode = wx.OPEN | wx.FILE_MUST_EXIST,
            )
        
        self.label_18 = wx.StaticText(self.panel_1, wx.ID_ANY, _("5)"))
        self.text_ctrl_9 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_9.SetMaxLength(maxword)
        self.text_ctrl_19 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_19.SetMaxLength(maxlength)
        self.panel_3 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_19 = wx.StaticText(self.panel_1, wx.ID_ANY, _("6)"))
        self.text_ctrl_10 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_10.SetMaxLength(maxword)
        self.text_ctrl_20 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_20.SetMaxLength(maxlength)
        self.panel_4 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_20 = wx.StaticText(self.panel_1, wx.ID_ANY, _("7)"))
        self.text_ctrl_11 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_11.SetMaxLength(maxword)
        self.text_ctrl_21 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_21.SetMaxLength(maxlength)
        self.panel_5 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_21 = wx.StaticText(self.panel_1, wx.ID_ANY, _("8)"))
        self.text_ctrl_12 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_12.SetMaxLength(maxword)
        self.text_ctrl_22 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_22.SetMaxLength(maxlength)
        self.panel_6 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_22 = wx.StaticText(self.panel_1, wx.ID_ANY, _("9)"))
        self.text_ctrl_13 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_13.SetMaxLength(maxword)
        self.text_ctrl_23 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_23.SetMaxLength(maxlength)
        self.panel_7 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_24 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Challenge Word"))
        self.label_25 = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.label_23 = wx.StaticText(self.panel_1, wx.ID_ANY, _("10)"))
        self.text_ctrl_14 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_14.SetMaxLength(maxword)
        self.text_ctrl_24 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_24.SetMaxLength(maxlength)
        self.panel_8 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.panel_11 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.panel_12 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.panel_13 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.static_line_4 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        self.checkbox = wx.CheckBox(self.panel_1, wx.ID_ANY, _("Create With Cover Pages"))
        self.checkbox.SetToolTipString("Generates First Pages (Cover page + advisories) of Activity Book")
        self.static_line_5 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        self.label_26 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Programming and Design: Emerson Grabke\nActivity Module Layout: Sowmya Tata\nIdeation: Ringo Cheung and Yutao Feng"), style=wx.ALIGN_CENTRE)
        self.static_line_6 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, _("Generate!"))
        self.button_1.SetToolTipString("Generates Activity Book Module based on form input")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def generator(self, button):
        retthing = self.OnFileSaveAs()
        if (not retthing):
            return        
        try:
            self.generate()
        except:
            self.OnInitFail()
            return
        
        try:
            self.PDFCreator()
        except:
            self.OnFailure()
            return
        self.OnComplete()
        #os.system("start \"" + str(outputPDFName) + "\"") #- Doesn't work on weird filenames
        return

    def generate(self): #Generates input, then runs pdf creation
        global word
        global imgpath
        global numwords
        global covervalue
        global outputPDFName
        global modulename
        global numnumword

        word = [[str(self.text_ctrl_5.GetValue()), str(self.text_ctrl_15.GetValue())],
                [str(self.text_ctrl_6.GetValue()), str(self.text_ctrl_16.GetValue())],
                [str(self.text_ctrl_7.GetValue()), str(self.text_ctrl_17.GetValue())],
                [str(self.text_ctrl_8.GetValue()), str(self.text_ctrl_18.GetValue())],
                [str(self.text_ctrl_9.GetValue()), str(self.text_ctrl_19.GetValue())],
                [str(self.text_ctrl_10.GetValue()), str(self.text_ctrl_20.GetValue())],
                [str(self.text_ctrl_11.GetValue()), str(self.text_ctrl_21.GetValue())],
                [str(self.text_ctrl_12.GetValue()), str(self.text_ctrl_22.GetValue())],
                [str(self.text_ctrl_13.GetValue()), str(self.text_ctrl_23.GetValue())],
                [str(self.text_ctrl_14.GetValue()), str(self.text_ctrl_24.GetValue())]]
        imgpath = [str(self.button_3.GetValue()),
                   str(self.button_4.GetValue()),
                   str(self.button_5.GetValue()),
                   str(self.button_6.GetValue())]
        modulename = self.text_module.GetValue()
        numwords = [0,0,0,0,0,0,0,0,0,0] #Note: 0, no word, 1 word, 2, picture
        covervalue = self.checkbox.GetValue()
        self.word_list = ["" for x in range(8)]
        self.all_words = ["" for y in range(10)]
        numnumword = 0
        for i in range(10):
            if (word[i][0] != ""):
                if(word[i][1] == ""):
                    emptyresult = self.EmptyDescription() #Warning for if a description is empty
                    if emptyresult != wx.ID_OK:
                        return
                else:
                    if (i >= 8):
                        self.all_words[i] = word[i][0]
                        numwords[i] = 1
                        continue #Bypasses challenge words
                    numwords[i] = 1
                    self.word_list[i] = word[i][0]
                    self.all_words[i] = word[i][0]
                    #print self.word_list[i] #Debug
                    numnumword += 1
                    if (i <=3 and imgpath[i] != ""):
                        numwords[i] = 2

        b = Crossword(10, 10, '-', 5000, word)
        b.compute_crossword(4)
        b.word_bank()

        global crossword
        global cross_legend
        crossword = b.display()
        cross_legend = b.legend()
        return

    def PDFCreator(self):
        global word
        global imgpath
        global numwords
        global covervalue
        global outputPDFName
        global modulename
        global c
        global numnumword

        pagecounter = [0,0,0,0,0] # 1: Draw picture. 2: Write word. 3: Challenge Words.
        
        packet = StringIO.StringIO()
        output = str(outputPDFName)
        out = open(output, 'wb')

        width, height = letter
        height, width = letter
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFillColorRGB(0.355,0.605,0.832)
        c.setFont('Times-Bold', 40)
        c.drawString(1*inch, 7*inch + 20, modulename.upper())
        c.showPage()
        #-- Word->Picture
        i = 0
        c.setFillColorRGB(0,0,0)
        az = 0
        i = 0
        counter = 0
        while (1):
            c.setFont('Times-Roman', 24)
            while ((i + az) < 8 and self.word_list[i + az] == ""):
                az += 1
            if ((i + az) >= 8 or self.word_list[i + az] == ""):
                break
            c.drawString(1.5*inch + 5, 8*inch + 5, self.word_list[i + az])
            counter += 1
            az += 1
            while ((i + az) < 8 and self.word_list[i + az] == ""):
                az += 1
            if ((i + az) >= 8 or self.word_list[i + az] == ""):
                break
            c.drawString(1.5*inch + 5, 4*inch - 3, self.word_list[i + az])
            counter += 1
            c.showPage()
            pagecounter[0] += 1
            i += 1
            
        if (counter%2 != 0):
            c.setFont('Times-Roman', 24)
            c.setFillColorRGB(1,1,1)
            c.rect(x=0*inch,y=0*inch,width=8.5*inch,height=4.5*inch, stroke = 0, fill = 1)
            c.showPage()
            pagecounter[0] += 1
            
        counter = 0
        for i in range(4):
            if (numwords[i] == 2):
                filepath = imgpath[i]
                if (counter%2 == 0):
                    self.get_image(filepath, 3.5*inch, 2.65*inch).drawOn(c, 0.57*inch, 5.65*inch)
                else:
                    self.get_image(filepath, 3.5*inch, 2.65*inch).drawOn(c, 0.57*inch, 2.0625*inch)
                    pagecounter[1] += 1
                    c.showPage()
                counter += 1
        if (counter%2 != 0):
            c.setFillColorRGB(1,1,1)
            c.rect(x=0*inch,y=0*inch,width=8.5*inch,height=5.5*inch, stroke=0, fill = 1)
            pagecounter[1] += 1
            c.showPage() #Newpage
            
        if (numwords[8] != 0):
            c.setFont('Times-Roman', 24)
            c.setFillColorRGB(0,0,0)
            c.drawString(1.5*inch + 8, 8*inch - 2, self.all_words[8])
            pagecounter[2] += 1
            c.showPage()
        if (numwords[9] != 0):
            c.setFont('Times-Roman', 24)
            c.setFillColorRGB(0,0,0)
            c.drawString(1.5*inch + 8, 8*inch - 2, self.all_words[9])
            pagecounter[2] += 1
            c.showPage()

        global crossword
        global cross_legend

        iterateh = 0
        c.setFillColorRGB(0,0,0)
        crosslines = crossword.strip('\n').split('\n')
        for line in crosslines:
            startw = inch
            starth = 8*inch
            iteratew = 0
            array = line.strip('\n').split(' ')
            for element in array:
                if (element == array[-1]):
                    continue
                if (element == '-'):
                    c.rect(x=startw + iteratew,y=starth - iterateh,width=0.5*inch,height=0.5*inch, fill = 1)
                else:
                    c.rect(x=startw + iteratew,y=starth - iterateh,width=0.5*inch,height=0.5*inch, fill = 0)
                    if (element != 'x'):
                        c.setFont('Times-Roman', 16)
                        c.drawString(startw + iteratew + 2, starth - iterateh + 2, element)
                iteratew += 0.5*inch
            iterateh += 0.5*inch

        starthd = 2.5*inch
        iterhd = 0
        startha = 2.5*inch
        iterha = 0
        lines = cross_legend.strip('\n').split('\n')
        c.setFont('Times-Roman', 18)
        for line in lines:
            array = line.split('*')
            if (array[1] == 'down'):
                c.drawString(0.75*inch, starthd - iterhd, array[0] + '. ' + array[2])
                iterhd += 0.4*inch
            else:
                c.drawString(4.5*inch - 12, startha - iterha, array[0] + '. ' + array[2])
                iterha += 0.4*inch
        
        c.showPage()                
        
        random.seed()
        grid = make_grid("easy", self.all_words)

        grid.to_pdf()
        c.save()

        #After it's all said and done
        new_pdf = pdf.PdfFileReader(packet)
        outputs = pdf.PdfFileWriter()
        thing = StringIO.StringIO(LoadResource(0, u'TEMPLATE', 1))
        template = pdf.PdfFileReader(thing)
        if (covervalue):
            teehee = StringIO.StringIO(LoadResource(0, u'COVER', 1))
            cover_pdf = pdf.PdfFileReader(teehee)
            for page in range(cover_pdf.getNumPages()):
                outputs.addPage(cover_pdf.getPage(page))

        # Module Name
        index = 0
        page1 = duplicate(template.getPage(0))
        page2 = new_pdf.getPage(index)
        page1.mergePage(page2)
        outputs.addPage(page1)
        index += 1
        
        # Draw picture
        for page in range(pagecounter[0]):
            page1 = duplicate(template.getPage(1))
            page2 = new_pdf.getPage(index)
            page1.mergePage(page2)
            outputs.addPage(page1)
            index += 1
        # Write word
        for page in range(pagecounter[1]):
            page1 = duplicate(template.getPage(2))
            page2 = new_pdf.getPage(index)
            page1.mergePage(page2)
            outputs.addPage(page1)
            index += 1
        # Challenge word
        for page in range(pagecounter[2]):
            page1 = duplicate(template.getPage(3))
            page2 = new_pdf.getPage(index)
            page1.mergePage(page2)
            outputs.addPage(page1)
            index += 1
        # Crossword
        page1 = template.getPage(4)
        page2 = new_pdf.getPage(index)
        page1.mergePage(page2)
        outputs.addPage(page1)
        index += 1
        # Wordsearch
        page1 = template.getPage(5)
        page2 = new_pdf.getPage(index)
        page1.mergePage(page2)
        outputs.addPage(page1)
        # Final thing
        outputs.addPage(template.getPage(6))
        
        outputs.write(out)
        out.close()
        if (covervalue):
            teehee.close()
        thing.close()

    def get_image(self, path, maxwidth=1*cm, maxheight=1*cm):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        width = iw
        height = ih
        if (maxwidth * aspect <= maxheight):
            return Image(path, width=maxwidth, height=(maxwidth * aspect))
        else:
            return Image(path, width=(maxheight / float(aspect)), height=maxheight)

    def OnFileSaveAs(self):
        """ File|SaveAs event - Prompt for File Name. """
        global outputPDFName
        ret = False
        dlg = wx.FileDialog(self, "Save As", "", "",
                           "PDF Files (*.pdf)|*.pdf|All Files|*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            outputPDFName = dirName+"\\"+fileName
            ret = True
        dlg.Destroy()
        return ret
    
    def EmptyDescription(self):
        dlg = wx.MessageDialog(self,
            "Some defined words don't have descriptions.\nDo you want to continue?\n(Note that these words will be disregarded in the activity book module)",
            "Warning: Empty Descriptions", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        emptyresult = dlg.ShowModal()
        dlg.Destroy()
        return emptyresult

    def OnSave(self, button):
        dlg = wx.FileDialog(self, "Save Inputs As", "", "",
                           "Input files (*.put)|*.put|All Files|*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            output = dirName+"\\"+fileName
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        outputty = open(output,"w")
        words = [[str(self.text_ctrl_5.GetValue()), str(self.text_ctrl_15.GetValue())],
                [str(self.text_ctrl_6.GetValue()), str(self.text_ctrl_16.GetValue())],
                [str(self.text_ctrl_7.GetValue()), str(self.text_ctrl_17.GetValue())],
                [str(self.text_ctrl_8.GetValue()), str(self.text_ctrl_18.GetValue())],
                [str(self.text_ctrl_9.GetValue()), str(self.text_ctrl_19.GetValue())],
                [str(self.text_ctrl_10.GetValue()), str(self.text_ctrl_20.GetValue())],
                [str(self.text_ctrl_11.GetValue()), str(self.text_ctrl_21.GetValue())],
                [str(self.text_ctrl_12.GetValue()), str(self.text_ctrl_22.GetValue())],
                [str(self.text_ctrl_13.GetValue()), str(self.text_ctrl_23.GetValue())],
                [str(self.text_ctrl_14.GetValue()), str(self.text_ctrl_24.GetValue())]]
        imgpaths = [str(self.button_3.GetValue()),
                   str(self.button_4.GetValue()),
                   str(self.button_5.GetValue()),
                   str(self.button_6.GetValue())]
        modulenames = self.text_module.GetValue()
        coverval = self.checkbox.GetValue()
        outputty.write(modulenames + '\n')
        outputty.write(str(coverval) + '\n')
        for i in range(10):
            newline = ''
            newline += words[i][0] + "+-" + words[i][1]
            if (i < 4):
                newline += "+-" + imgpaths[i]
            newline += '\n'
            outputty.write(newline)
        outputty.close()
        return

    def OnLoad(self, button):
        dlg = wx.FileDialog(self, "Load Inputs From", "", "",
                           "Input files (*.put)|*.put|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            inputty = dirName+"\\"+fileName
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        put = open(inputty, "r")
        words = []
        imgpaths = []
        module = put.readline().strip('\n')
        coverval = put.readline().strip('\n')
        i = 0
        for line in put:
            array = line.strip('\n').split('+-')
            words.append([array[0],array[1]])
            if (i < 4):
                imgpaths.append(array[2])
            i += 1
        self.text_ctrl_5.SetValue(words[0][0])
        self.text_ctrl_6.SetValue(words[1][0])
        self.text_ctrl_7.SetValue(words[2][0])
        self.text_ctrl_8.SetValue(words[3][0])
        self.text_ctrl_9.SetValue(words[4][0])
        self.text_ctrl_10.SetValue(words[5][0])
        self.text_ctrl_11.SetValue(words[6][0])
        self.text_ctrl_12.SetValue(words[7][0])
        self.text_ctrl_13.SetValue(words[8][0])
        self.text_ctrl_14.SetValue(words[9][0])
        
        self.text_ctrl_15.SetValue(words[0][1])
        self.text_ctrl_16.SetValue(words[1][1])
        self.text_ctrl_17.SetValue(words[2][1])
        self.text_ctrl_18.SetValue(words[3][1])
        self.text_ctrl_19.SetValue(words[4][1])
        self.text_ctrl_20.SetValue(words[5][1])
        self.text_ctrl_21.SetValue(words[6][1])
        self.text_ctrl_22.SetValue(words[7][1])
        self.text_ctrl_23.SetValue(words[8][1])
        self.text_ctrl_24.SetValue(words[9][1])
        self.text_module.SetValue(module)
        self.button_3.SetValue(imgpaths[0])
        self.button_4.SetValue(imgpaths[1])
        self.button_5.SetValue(imgpaths[2])
        self.button_6.SetValue(imgpaths[3])
        if (coverval == "False"):
            self.checkbox.SetValue(False)
        else:
            self.checkbox.SetValue(True)
        return

    def OnClear(self, button):
        self.text_ctrl_5.SetValue("")
        self.text_ctrl_6.SetValue("")
        self.text_ctrl_7.SetValue("")
        self.text_ctrl_8.SetValue("")
        self.text_ctrl_9.SetValue("")
        self.text_ctrl_10.SetValue("")
        self.text_ctrl_11.SetValue("")
        self.text_ctrl_12.SetValue("")
        self.text_ctrl_13.SetValue("")
        self.text_ctrl_14.SetValue("")
        self.text_ctrl_15.SetValue("")
        self.text_ctrl_16.SetValue("")
        self.text_ctrl_17.SetValue("")
        self.text_ctrl_18.SetValue("")
        self.text_ctrl_19.SetValue("")
        self.text_ctrl_20.SetValue("")
        self.text_ctrl_21.SetValue("")
        self.text_ctrl_22.SetValue("")
        self.text_ctrl_23.SetValue("")
        self.text_ctrl_24.SetValue("")
        self.text_module.SetValue("")
        self.button_3.SetValue("")
        self.button_4.SetValue("")
        self.button_5.SetValue("")
        self.button_6.SetValue("")
        self.checkbox.SetValue(False)

    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnComplete(self):
        dlg = wx.MessageDialog(self,
            "Activity book module generated.\nHave a nice day!",
            "Creation Completed", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnFailure(self):
        dlg = wx.MessageDialog(self,
            "Creation failed while creating PDF\nPlease recheck input file formats,\nAnd if overwriting a PDF, ensure it is closed first.\nThen try again.",
            "Creation Failed", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnInitFail(self):
        dlg = wx.MessageDialog(self,
            "Creation failed while gathering input\nPlease ensure only ASCII-compliant characters are being inputted\nThen try again.",
            "Creation Failed", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self,
            "This application was created by:\n\nEmerson Grabke, Ringo Cheung, Sowmya Tata and Yutao (Dexter) Feng,\nFirst year Engineering Science Students at the University of Toronto!\n\nThanks to Praxis, and Python for the tools required to create this\n\nSpecial thanks to:\nPYPDF (Copyright 2006, Mathieu Fenniak, Copyright 2007, Ashish Kulkarni),\nBryan Helmig for the Crossword algorithm (Copyright 2010, Bryan Helmig)\nAnd rboulton (through GitHub) for the Wordsearch algorithm!\n\nIn accordance with copyrights, this software is free to use and distribute",
            "About This Program", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnReadme(self, event):
        dlg = wx.MessageDialog(self,
'''Activity Book Module Generator for Seniors with Anomic Aphasia

This module was created by University of Toronto Engineering Science students.

Programming and Design: Emerson Grabke
Activity Module Layout: Sowmya Tata
Ideation: Ringo Cheung & Yutao Feng.

The intention of (and instructions for) this product:

1) Once a week, after performing exercises with volunteers, friends or a spouse, said person would input up to 10 words (and their descriptions) and up to 4 pictures.

2) If this is the first module in the senior (or group of senior)'s collection, check the "Create With Cover Pages" box.

3) Click generate.

4) Save a PDF of that week's module for a senior(s).

5) Print PDF for the senior(s).

6) They work on it at home.

7) Repeat.

###################
####--WARNING--####
###################

Please enforce that "Challenge Words" are only to be embarked on with someone else.

"Challenge words" should be chosen carefully with the senior's safety in mind. 

NOTE: "Challenge Word", when referenced, refers to a word that the senior would have to go out into the world to find and take a photo of. Words inputted below the "Challenge Word" indicator in the Generator are interpreted to be "Challenge Words" by the Module, and will be reflected in the generation of PDFs.''', "Instructions About This Program", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("Activity Book Generator for Seniors with Anomic Aphasia"))
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        rwar = 205
        statusbar_fields = [_("Program to Generate Activity Book")]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.label_1.SetFont(wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.label_2.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.label_3.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.label_4.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.label_14.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_5.SetMinSize((100, 26))
        self.text_ctrl_5.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_15.SetMinSize((rwar, 26))
        self.text_ctrl_15.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_15.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_6.SetMinSize((100, 26))
        self.text_ctrl_6.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_16.SetMinSize((rwar, 26))
        self.text_ctrl_16.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        
        self.text_module.SetMinSize((185, 26))
        self.text_module.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.module.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Times New Roman"))
        
        self.label_16.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_7.SetMinSize((100, 26))
        self.text_ctrl_7.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_17.SetMinSize((rwar, 26))
        self.text_ctrl_17.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_17.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_8.SetMinSize((100, 26))
        self.text_ctrl_8.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_18.SetMinSize((rwar, 26))
        self.text_ctrl_18.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_18.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_9.SetMinSize((100, 26))
        self.text_ctrl_9.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_19.SetMinSize((rwar, 26))
        self.text_ctrl_19.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_19.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_10.SetMinSize((100, 26))
        self.text_ctrl_10.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_20.SetMinSize((rwar, 26))
        self.text_ctrl_20.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_20.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_11.SetMinSize((100, 26))
        self.text_ctrl_11.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_21.SetMinSize((rwar, 26))
        self.text_ctrl_21.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_21.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_12.SetMinSize((100, 26))
        self.text_ctrl_12.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_22.SetMinSize((rwar, 26))
        self.text_ctrl_22.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_22.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_13.SetMinSize((100, 26))
        self.text_ctrl_13.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_23.SetMinSize((rwar, 26))
        self.text_ctrl_23.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.label_24.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.label_24.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 1, "Times New Roman"))
        self.label_23.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.text_ctrl_14.SetMinSize((100, 26))
        self.text_ctrl_14.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.text_ctrl_24.SetMinSize((rwar, 26))
        self.text_ctrl_24.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.checkbox.SetMinSize((200, 50))
        self.checkbox.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Times New Roman"))
        self.static_line_5.SetMinSize((2, 50))
        self.label_26.SetMinSize((400, 50))
        self.label_26.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.static_line_6.SetMinSize((2, 50))
        self.button_1.SetMinSize((150, 50))
        self.button_1.SetFont(wx.Font(20, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Times New Roman"))
        self.button_3.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.button_4.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.button_5.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        self.button_6.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Calibri"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(13, 3, 15, 15)
        sizer_module = wx.BoxSizer(wx.HORIZONTAL)
        sizer_module_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_module_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        #--
        sizer_module.Add(self.module, 0, 0, 0)
        sizer_module.Add(self.text_module, 0, 0, 0)
        grid_sizer_1.Add(sizer_module, 0, 0, 0)
        grid_sizer_1.Add(self.panel_module_1, 0, 0, 0)
        grid_sizer_1.Add(self.panel_module_2, 0, 0, 0)
        sizer_3.Add(self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(self.static_line_3, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_2, 0, 0, 0)
        grid_sizer_1.Add(self.label_3, 0, 0, 0)
        grid_sizer_1.Add(self.label_4, 0, 0, 0)
        sizer_4.Add(self.label_14, 0, 0, 0)
        sizer_4.Add(self.text_ctrl_5, 0, 0, 0)
        grid_sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_15, 0, 0, 0)
        grid_sizer_1.Add(self.button_3, 1, wx.EXPAND, 0)
        sizer_5.Add(self.label_15, 0, 0, 0)
        sizer_5.Add(self.text_ctrl_6, 0, 0, 0)
        grid_sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_16, 0, 0, 0)
        grid_sizer_1.Add(self.button_4, 1, wx.EXPAND, 0)
        sizer_6.Add(self.label_16, 0, 0, 0)
        sizer_6.Add(self.text_ctrl_7, 0, 0, 0)
        grid_sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_17, 0, 0, 0)
        grid_sizer_1.Add(self.button_5, 1, wx.EXPAND, 0)
        sizer_7.Add(self.label_17, 0, 0, 0)
        sizer_7.Add(self.text_ctrl_8, 0, 0, 0)
        grid_sizer_1.Add(sizer_7, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_18, 0, 0, 0)
        grid_sizer_1.Add(self.button_6, 1, wx.EXPAND, 0)
        sizer_8.Add(self.label_18, 0, 0, 0)
        sizer_8.Add(self.text_ctrl_9, 0, 0, 0)
        grid_sizer_1.Add(sizer_8, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_19, 0, 0, 0)
        grid_sizer_1.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_9.Add(self.label_19, 0, 0, 0)
        sizer_9.Add(self.text_ctrl_10, 0, 0, 0)
        grid_sizer_1.Add(sizer_9, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_20, 0, 0, 0)
        grid_sizer_1.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_10.Add(self.label_20, 0, 0, 0)
        sizer_10.Add(self.text_ctrl_11, 0, 0, 0)
        grid_sizer_1.Add(sizer_10, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_21, 0, 0, 0)
        grid_sizer_1.Add(self.panel_5, 1, wx.EXPAND, 0)
        sizer_11.Add(self.label_21, 0, 0, 0)
        sizer_11.Add(self.text_ctrl_12, 0, 0, 0)
        grid_sizer_1.Add(sizer_11, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_22, 0, 0, 0)
        grid_sizer_1.Add(self.panel_6, 1, wx.EXPAND, 0)
        sizer_12.Add(self.label_22, 0, 0, 0)
        sizer_12.Add(self.text_ctrl_13, 0, 0, 0)
        grid_sizer_1.Add(self.label_24, 0, 0, 0)
        grid_sizer_1.Add(self.label_25, 0, 0, 0)
        grid_sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_12, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_23, 0, 0, 0)
        grid_sizer_1.Add(self.panel_7, 1, wx.EXPAND, 0)
        sizer_13.Add(self.label_23, 0, 0, 0)
        sizer_13.Add(self.text_ctrl_14, 0, 0, 0)
        grid_sizer_1.Add(sizer_13, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.text_ctrl_24, 0, 0, 0)
        grid_sizer_1.Add(self.panel_8, 1, wx.EXPAND, 0)
        #grid_sizer_1.Add(self.panel_11, 1, wx.EXPAND, 0)
        #grid_sizer_1.Add(self.panel_12, 1, wx.EXPAND, 0)
        #grid_sizer_1.Add(self.panel_13, 1, wx.EXPAND, 0)
        sizer_3.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_4, 0, wx.EXPAND, 0)
        sizer_15.Add(self.checkbox, 0, 0, 5)
        sizer_15.Add(self.static_line_5, 0, wx.EXPAND, 0)
        sizer_15.Add(self.label_26, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_15.Add(self.static_line_6, 0, wx.EXPAND, 0)
        sizer_15.Add(self.button_1, 0, 0, 5)
        sizer_3.Add(sizer_15, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_3)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
        self.Bind(wx.EVT_BUTTON,self.generator,self.button_1)
        

# end of class MyFrame
class MyDisplay(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers() - deprecated
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyDisplay

#---------------CROSSWORD-----------------
class Crossword(object):
    def __init__(self, cols, rows, empty = '-', maxloops = 2000, available_words=[]):
        self.cols = cols
        self.rows = rows
        self.empty = empty
        self.maxloops = maxloops
        self.available_words = available_words
        self.randomize_word_list()
        self.current_word_list = []
        self.debug = 0
        self.clear_grid()

    def clear_grid(self): # initialize grid and fill with empty character
        self.grid = []
        for i in range(self.rows):
            ea_row = []
            for j in range(self.cols):
                ea_row.append(self.empty)
            self.grid.append(ea_row)

    def randomize_word_list(self): # also resets words and sorts by length
        temp_list = []
        for word in self.available_words:
            if isinstance(word, Word):
                temp_list.append(Word(word.word, word.clue))
            else:
                temp_list.append(Word(word[0], word[1]))
        random.shuffle(temp_list) # randomize word list
        temp_list.sort(key=lambda i: len(i.word), reverse=True) # sort by length
        self.available_words = temp_list

    def compute_crossword(self, time_permitted = 1.00, spins=2):
        time_permitted = float(time_permitted)

        count = 0
        copy = Crossword(self.cols, self.rows, self.empty, self.maxloops, self.available_words)

        start_full = float(time.time())
        while (float(time.time()) - start_full) < time_permitted or count == 0: # only run for x seconds
            self.debug += 1
            copy.current_word_list = []
            copy.clear_grid()
            copy.randomize_word_list()
            x = 0
            while x < spins: # spins; 2 seems to be plenty
                for word in copy.available_words:
                    if word not in copy.current_word_list:
                        copy.fit_and_add(word)
                x += 1
            #print copy.solution()
            #print len(copy.current_word_list), len(self.current_word_list), self.debug
            # buffer the best crossword by comparing placed words
            if len(copy.current_word_list) > len(self.current_word_list):
                self.current_word_list = copy.current_word_list
                self.grid = copy.grid
            count += 1
        return

    def suggest_coord(self, word):
        count = 0
        coordlist = []
        glc = -1
        for given_letter in word.word: # cycle through letters in word
            glc += 1
            rowc = 0
            for row in self.grid: # cycle through rows
                rowc += 1
                colc = 0
                for cell in row: # cycle through  letters in rows
                    colc += 1
                    if given_letter == cell: # check match letter in word to letters in row
                        try: # suggest vertical placement 
                            if rowc - glc > 0: # make sure we're not suggesting a starting point off the grid
                                if ((rowc - glc) + word.length) <= self.rows: # make sure word doesn't go off of grid
                                    coordlist.append([colc, rowc - glc, 1, colc + (rowc - glc), 0])
                        except: pass
                        try: # suggest horizontal placement 
                            if colc - glc > 0: # make sure we're not suggesting a starting point off the grid
                                if ((colc - glc) + word.length) <= self.cols: # make sure word doesn't go off of grid
                                    coordlist.append([colc - glc, rowc, 0, rowc + (colc - glc), 0])
                        except: pass
        # example: coordlist[0] = [col, row, vertical, col + row, score]
        #print word.word
        #print coordlist
        new_coordlist = self.sort_coordlist(coordlist, word)
        #print new_coordlist
        return new_coordlist

    def sort_coordlist(self, coordlist, word): # give each coordinate a score, then sort
        new_coordlist = []
        for coord in coordlist:
            col, row, vertical = coord[0], coord[1], coord[2]
            coord[4] = self.check_fit_score(col, row, vertical, word) # checking scores
            if coord[4]: # 0 scores are filtered
                new_coordlist.append(coord)
        random.shuffle(new_coordlist) # randomize coord list; why not?
        new_coordlist.sort(key=lambda i: i[4], reverse=True) # put the best scores first
        return new_coordlist

    def fit_and_add(self, word): # doesn't really check fit except for the first word; otherwise just adds if score is good
        fit = False
        count = 0
        coordlist = self.suggest_coord(word)

        while not fit and count < self.maxloops:

            if len(self.current_word_list) == 0: # this is the first word: the seed
                # top left seed of longest word yields best results (maybe override)
                vertical, col, row = random.randrange(0, 2), 1, 1
                ''' 
                # optional center seed method, slower and less keyword placement
                if vertical:
                    col = int(round((self.cols + 1)/2, 0))
                    row = int(round((self.rows + 1)/2, 0)) - int(round((word.length + 1)/2, 0))
                else:
                    col = int(round((self.cols + 1)/2, 0)) - int(round((word.length + 1)/2, 0))
                    row = int(round((self.rows + 1)/2, 0))
                # completely random seed method
                col = random.randrange(1, self.cols + 1)
                row = random.randrange(1, self.rows + 1)
                '''

                if self.check_fit_score(col, row, vertical, word): 
                    fit = True
                    self.set_word(col, row, vertical, word, force=True)
            else: # a subsquent words have scores calculated
                try: 
                    col, row, vertical = coordlist[count][0], coordlist[count][1], coordlist[count][2]
                except IndexError: return # no more cordinates, stop trying to fit

                if coordlist[count][4]: # already filtered these out, but double check
                    fit = True 
                    self.set_word(col, row, vertical, word, force=True)

            count += 1
        return

    def check_fit_score(self, col, row, vertical, word):
        '''
        And return score (0 signifies no fit). 1 means a fit, 2+ means a cross.

        The more crosses the better.
        '''
        if col < 1 or row < 1:
            return 0

        count, score = 1, 1 # give score a standard value of 1, will override with 0 if collisions detected
        for letter in word.word:            
            try:
                active_cell = self.get_cell(col, row)
            except IndexError:
                return 0

            if active_cell == self.empty or active_cell == letter:
                pass
            else:
                return 0

            if active_cell == letter:
                score += 1

            if vertical:
                # check surroundings
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col+1, row): # check right cell
                        return 0

                    if not self.check_if_cell_clear(col-1, row): # check left cell
                        return 0

                if count == 1: # check top cell only on first letter
                    if not self.check_if_cell_clear(col, row-1):
                        return 0

                if count == len(word.word): # check bottom cell only on last letter
                    if not self.check_if_cell_clear(col, row+1): 
                        return 0
            else: # else horizontal
                # check surroundings
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col, row-1): # check top cell
                        return 0

                    if not self.check_if_cell_clear(col, row+1): # check bottom cell
                        return 0

                if count == 1: # check left cell only on first letter
                    if not self.check_if_cell_clear(col-1, row):
                        return 0

                if count == len(word.word): # check right cell only on last letter
                    if not self.check_if_cell_clear(col+1, row):
                        return 0


            if vertical: # progress to next letter and position
                row += 1
            else: # else horizontal
                col += 1

            count += 1

        return score

    def set_word(self, col, row, vertical, word, force=False): # also adds word to word list
        if force:
            word.col = col
            word.row = row
            word.vertical = vertical
            self.current_word_list.append(word)

            for letter in word.word:
                self.set_cell(col, row, letter)
                if vertical:
                    row += 1
                else:
                    col += 1
        return

    def set_cell(self, col, row, value):
        self.grid[row-1][col-1] = value

    def get_cell(self, col, row):
        return self.grid[row-1][col-1]

    def check_if_cell_clear(self, col, row):
        try:
            cell = self.get_cell(col, row)
            if cell == self.empty: 
                return True
        except IndexError:
            pass
        return False

    def solution(self): # return solution grid
        outStr = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                outStr += '%s ' % c
            outStr += '\n'
        return outStr

    def word_find(self): # return solution grid
        outStr = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                if c == self.empty:
                    outStr += '%s ' % string.ascii_lowercase[random.randint(0,len(string.ascii_lowercase)-1)]
                else:
                    outStr += '%s ' % c
            outStr += '\n'
        return outStr

    def order_number_words(self): # orders words and applies numbering system to them
        self.current_word_list.sort(key=lambda i: (i.col + i.row))
        count, icount = 1, 1
        for word in self.current_word_list:
            word.number = count
            if icount < len(self.current_word_list):
                if word.col == self.current_word_list[icount].col and word.row == self.current_word_list[icount].row:
                    pass
                else:
                    count += 1
            icount += 1

    def display(self, order=True): # return (and order/number wordlist) the grid minus the words adding the numbers
        outStr = ""
        if order:
            self.order_number_words()

        copy = self

        for word in self.current_word_list:
            copy.set_cell(word.col, word.row, word.number)

        for r in range(copy.rows):
            for c in copy.grid[r]:
                outStr += '%s ' % c
            outStr += '\n'

        outStr = re.sub(r'[a-z]', 'x', outStr)
        return outStr

    def word_bank(self): 
        outStr = ''
        temp_list = duplicate(self.current_word_list)
        random.shuffle(temp_list) # randomize word list
        for word in temp_list:
            outStr += '%s\n' % word.word
        return outStr

    def legend(self): # must order first
        outStr = ''
        for word in self.current_word_list:
            outStr += '%d*%s*%s\n' % (word.number, word.down_across(), word.clue )
        return outStr

    def word_legend(self):
        outStr = ''
        for word in self.current_word_list:
            outStr += '%s\n' % (word.word)
        return outStr

class Word(object):
    def __init__(self, word=None, clue=None):
        self.word = re.sub(r'\s', '', word.lower())
        self.clue = clue
        self.length = len(self.word)
      # the below are set when placed on board
        self.row = None
        self.col = None
        self.vertical = None
        self.number = None

    def down_across(self): # return down or across
        if self.vertical: 
            return 'down'
        else: 
            return 'across'

        def __repr__(self):
            return self.word

### end class, start execution

#!/usr/bin/env python

# Directions are:
# +. left to right
# -. right to left
# .+ top to bottom
# .- bottom to top

##def read_words(filename):
##    words = set()
##    fd = open(filename)
##    try:
##        for line in fd.readlines():
##            if "'" in line:
##                continue
##            line = line.strip().lower()
##            if len(line) > 3 and len(line) < 7:
##                words.add(line)
##    finally:
##        fd.close()
##    return words

all_words = ["bird","word","is",'the','rwar']

all_directions = ('+-', '+.', '++', '.+', '.-', '--', '-.', '-+')

styles = {
    'easy': ('10x10', ('+.', '.+', '.-', '-.')),
    'standard': ('15x15', ('+-', '+.', '++', '.+', '.-', '-.')),
    'hard': ('20x20', all_directions),
}

dirconv = {
    '-': -1,
    '.': 0,
    '+': 1,
}

letters = "abcdefghijklmnopqrstuvwxyz"
letters = letters.upper()

class Grid(object):
    def __init__(self, wid, hgt):
        self.wid = wid
        self.hgt = hgt
        self.data = ['.'] * (wid * hgt)
        self.used = [' '] * (wid * hgt)
        self.words = []
        self.listy = []

    def to_text(self):
        result = []
        for row in xrange(self.hgt):
            result.append(''.join(self.data[row * self.wid :
                                  (row + 1) * self.wid]))
        return '\n'.join(result)
        
    def used_to_text(self):
        result = []
        for row in xrange(self.hgt):
            result.append(''.join(self.used[row * self.wid :
                                  (row + 1) * self.wid]))
        return '\n'.join(result)

    def to_pdf(self ):
        global c
        
        pagesize = letter
        c.setFont('Times-Roman', 24)
        margin = 50
        printwid, printhgt = map(lambda x: x - margin * 2, pagesize)
        
        gx = margin
        gy = 8*inch
        gdx = printwid / self.wid
        gdy = printhgt / self.hgt
        for y in xrange(self.hgt):
            cy = gy - y * gdy/2
            for x in xrange(self.wid):
                cx = gdx + gx + x * gdx/2
                p = x + self.wid * y
                d = self.data[p]
                c.drawString(cx, cy, d)

        i = 0

        c.setFont('Times-Roman', 36)
        c.setFillColorRGB(0,0.2,0.4)
        c.drawString(2*gdx, gy - self.hgt * gdy/2 - gdy/2 - 10, "Words to find")
        c.setStrokeColorRGB(0,0.2,0.4)
        c.line(2*gdx, gy - self.hgt * gdy/2 - gdy/2 - 4 - 10, 2*gdx + len("Words to find")*16,gy - self.hgt * gdy/2 - gdy/2 - 4 - 10)

        index = 0
        for word in self.listy:
            index += 1
            if (index <= 5):
                i += 24
                hh = gy - self.hgt * gdy/2 - gdy/2 - 20 - i
                ww = 2*gdx
                c.setFont('Times-Roman', 18)
                c.setFillColorRGB(0,0,0)
                c.drawString(ww, hh, word)
            else:
                i += 24
                hh = gy - self.hgt * gdy/2 - gdy/2 - 20 - i
                ww = 2*gdx + 3.5*inch
                c.setFont('Times-Roman', 18)
                c.setFillColorRGB(0,0,0)
                c.drawString(ww, hh, word)
            if (index == 5):
                i = 0
        c.showPage()
        #c.save()
        return

    def pick_word_pos(self, wordlen, directions):
        xd, yd = random.choice(directions)
        minx = (wordlen - 1, 0, 0)[xd + 1]
        maxx = (self.wid - 1, self.wid - 1, self.wid - wordlen)[xd + 1]
        miny = (wordlen - 1, 0, 0)[yd + 1]
        maxy = (self.hgt - 1, self.hgt - 1, self.hgt - wordlen)[yd + 1]
        x = random.randint(minx, maxx)
        y = random.randint(miny, maxy)
        return x, y, xd, yd

    def write_word(self, word, ox, oy, xd, yd):
        x, y = ox, oy
        for c in word:
            p = x + self.wid * y
            e = self.data[p]
            if e != '.' and e != c:
                return False
            x += xd
            y += yd

        x, y = ox, oy
        for c in word:
            p = x + self.wid * y
            self.data[p] = c
            self.used[p] = '.'
            x += xd
            y += yd

        return True

    def place_words(self, words, directions, tries=100):
        # Sort words into descending order of length
        words = list(words)
        words.sort(key = lambda x: len(x), reverse = True)

        for word in words:
            wordlen = len(word)
            while True:
                x, y, xd, yd = self.pick_word_pos(wordlen, directions)
                if self.write_word( word.upper(), x, y, xd, yd):
                    self.words.append((word.upper(), x, y, xd, yd))
                    self.listy.append(word.upper())
                    break
                tries -= 1
                if tries <= 0:
                    return False
        return True

    def fill_in_letters(self):
        for p in xrange(self.wid * self.hgt):
            if self.data[p] == '.':
                self.data[p] = random.choice(letters)

    def remove_bad_words(self):
        return True

def make_grid(stylep="easy", words=[], tries=100):
    # Parse and validate the style parameter.
    size, directions = styles.get(stylep, (stylep, all_directions))
    size = size.split('x')
    if len(size) != 2:
        raise ValueError("Invalid style parameter: %s" % stylep)
    try:
        wid, hgt = map(int, size)
    except ValueError:
        raise ValueError("Invalid style parameter: %s" % stylep)

    directions = [(dirconv[direction[0]], dirconv[direction[1]])
                  for direction in directions]

    while True:
        while True:
            grid = Grid(wid, hgt)
            if grid.place_words(words, directions):
                break
            tries -= 1
            if tries <= 0:
                return None

        grid.fill_in_letters()
        if grid.remove_bad_words():
            return grid

        tries -= 1
        if tries <= 0:
            return None

#start_full = float(time.time())

if __name__ == "__main__":
    gettext.install("display") # replace with the appropriate catalog name

    display = MyDisplay(0)
    display.MainLoop()
