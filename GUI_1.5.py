try:
    import Tkinter as tk
    from Tkinter import *
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import *
    from tkinter import scrolledtext
    from tkinter import filedialog
    from tkinter import ttk
    from tkinter import messagebox
    
import wikipedia
from tkcalendar import Calendar, DateEntry
import multiprocessing 
import multiprocessing.pool
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from multiprocessing import Pool
import subprocess
import re
import os 
import time
import string
#importing libraries for pdf extraction
# Base library: pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, val):
        pass
    
class NoDaemonProcessPool(multiprocessing.pool.Pool):

    def Process(self, *args, **kwds):
        proc = super(NoDaemonProcessPool, self).Process(*args, **kwds)
        proc.__class__ = NoDaemonProcess

        return proc
    
def writeToFile(summary,name):
    file = open(name,'wb')
    file.write(summary)
    file.close()
    
def closeWindow(labl,top):
    labl.destroy()
    top.destroy()

def checkfile(path):
    isFile = os.path.isfile(path)
    return isFile

def checknumber(n):
    return n.isdigit()

def validateurl(url):
    validate = URLValidator()
    try:
        validate(url)
        return "String is a valid URL"
    except ValidationError as exception:
        return "String is not valid URL"

def depthvalidate(n):
    if(n.isdigit()):
        if(int(n)<=5):
            return "valid"
        else:
            return "depth should be less than or equal to 5"
    else:
        return "depth should be a number"
    
def showSummary(docType,summary):
    if docType=='text':
        txtTop = Toplevel()
        txtTop.title("Text File Summary")
        txtTop.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        txtLabl = LabelFrame(txtTop, text="Text File Summary",font = ('times new roman',20,'bold','italic'))
        txtLabl.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        summaryBox1 = scrolledtext.ScrolledText(txtLabl,wrap=WORD)
        summaryBox1.config(state=NORMAL)
        summaryBox1.delete("1.0", "end")
        summaryBox1.insert("1.0",summary)
        summaryBox1.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)

        summaryBox1.config(state=DISABLED)
        
        closebtn1 = Button(txtTop, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(txtLabl,txtTop))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)
        
    elif docType =='pdf':
        pdfTop = Toplevel()
        pdfTop.title("PDF File Summary")
        pdfTop.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        pdfLabl = LabelFrame(pdfTop, text="PDF File Summary",font = ('times new roman',20,'bold','italic'))
        pdfLabl.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        
        summaryBox2 = scrolledtext.ScrolledText(pdfLabl,wrap=WORD)
        summaryBox2.config(state=NORMAL)
        summaryBox2.delete("1.0", "end")
        summaryBox2.insert("1.0",summary)
        summaryBox2.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)
        summaryBox2.config(state=DISABLED)
        
        closebtn1 = Button(pdfTop, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(pdfLabl,pdfTop))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)
        
    elif docType=='url':
        urlTop = Toplevel()
        urlTop.title("URL Summary")
        urlTop.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        urlLabl = LabelFrame(urlTop, text="URL Summary",font = ('times new roman',20,'bold','italic'))
        urlLabl.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        
        summaryBox3 = scrolledtext.ScrolledText(urlLabl,wrap=WORD)
        summaryBox3.config(state=NORMAL)
        summaryBox3.delete("1.0", "end")
        summaryBox3.insert("1.0",summary)
        summaryBox3.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)
        summaryBox3.config(state=DISABLED)
        
        closebtn1 = Button(urlTop, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(urlLabl,urlTop))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)
    
    elif docType=='wiki':
        wikiTop = Toplevel()
        wikiTop.title("Wikipedia Summary")
        wikiTop.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        wikiLabl = LabelFrame(wikiTop, text="Wikipedia Summary",font = ('times new roman',20,'bold','italic'))
        wikiLabl.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        
        summaryBox4 = scrolledtext.ScrolledText(wikiLabl,wrap=WORD)
        summaryBox4.config(state=NORMAL)
        summaryBox4.delete("1.0", "end")
        summaryBox4.insert("1.0",summary)
        summaryBox4.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)
        summaryBox4.config(state=DISABLED)
        
        closebtn1 = Button(wikiTop, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(wikiLabl,wikiTop))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)
    
    elif docType=='fbtw1':
        socTop1 = Toplevel()
        socTop1.title("Social Media Summary")
        socTop1.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        socLabl1 = LabelFrame(socTop1, text="Social Media Summary",font = ('times new roman',20,'bold','italic'))
        socLabl1.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        
        summaryBox5 = scrolledtext.ScrolledText(socLabl1,wrap=WORD)
        summaryBox5.config(state=NORMAL)
        summaryBox5.delete("1.0", "end")
        summaryBox5.insert("1.0",summary)
        summaryBox5.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)
        summaryBox5.config(state=DISABLED)
        
        closebtn1 = Button(socTop1, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(socLabl1,socTop1))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)

    elif docType=='fbtw2':
        socTop2 = Toplevel()
        socTop2.title("Social Media Summary")
        socTop2.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        socLabl2 = LabelFrame(socTop2, text="Social Media Summary",font = ('times new roman',20,'bold','italic'))
        socLabl2.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        
        summaryBox6 = scrolledtext.ScrolledText(socLabl2,wrap=WORD)
        summaryBox6.config(state=NORMAL)
        summaryBox6.delete("1.0", "end")
        summaryBox6.insert("1.0",summary)
        summaryBox6.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)
        summaryBox6.config(state=DISABLED)
        
        closebtn1 = Button(socTop2, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(socLabl2,socTop2))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)
    
    elif docType=='rss':
        socTop3 = Toplevel()
        socTop3.title("Social Media Summary")
        socTop3.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
        socLabl3 = LabelFrame(socTop3, text="Social Media Summary",font = ('times new roman',20,'bold','italic'))
        socLabl3.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.8)
        
        summaryBox7 = scrolledtext.ScrolledText(socLabl3,wrap=WORD)
        summaryBox7.config(state=NORMAL)
        summaryBox7.delete("1.0", "end")
        summaryBox7.insert("1.0",summary)
        summaryBox7.place(relx = .05, rely = .05, relheight =.9, relwidth = .9)
        summaryBox7.config(state=DISABLED)
        
        closebtn1 = Button(socTop3, text = "Close",font = ('Arial',11),cursor="hand2",command = lambda: closeWindow(socLabl3,socTop3))
        closebtn1.place(relx = 0.4,rely = 0.9, relwidth = 0.2, relheight = .075)
        
def process_summary(doc_type,path,keywords,sent,depth,noword):
    if doc_type == 'text':
        return subprocess.check_output(['python','using_doc.py',path,keywords,sent])
    elif doc_type=='pdf':
        return subprocess.check_output(['python','using_pdf.py',path,keywords,sent])
    elif doc_type=='url':
        return subprocess.check_output(['python','using_url_wiki.py',path,keywords,depth,noword,'1'])
    elif doc_type=='wiki':
        return subprocess.check_output(['python','using_url_wiki.py',path,keywords,depth,noword,'2'])
    elif doc_type=='fbtw1':
        return subprocess.check_output(['python','using_social.py',path,keywords,sent,depth,noword,'1'])
    elif doc_type=='fbtw2':
        return subprocess.check_output(['python','using_social.py',path,keywords,sent,depth,noword,'2'])
    elif doc_type=='rss':
        return subprocess.check_output(['python','using_social.py',path,keywords,sent,depth,noword,'3'])
    
    
def display_options(CheckVar1,CheckVar2,CheckVar3,CheckVar4,E1,E2,E10,E11,E3,var,l,var1,textBox8,E8,cal,E7,E9,var2,key,a,E6,E4,E5):
   
    p=multiprocessing.Pool(processes=4)
    start = time.time()
  
    if CheckVar1==1:
        
        text_sum = p.apply_async(process_summary,('text',E1,l,E10,'0','0'))
       
    if CheckVar2==1:
      
        pdf_sum = p.apply_async(process_summary,('pdf',E2,l,E11,'0','0'))
        
        
    if CheckVar3==1:
        if(var==1):
           
            url_sum1 = p.apply_async(process_summary,('url',E3,l,'0',E4,E5))
            
        elif(var==2):
           
            url_sum2 = p.apply_async(process_summary,('wiki','',key,'0','0',E6))
         
    
    if CheckVar4==1:
        if(var1==1):
           
            if(var2==1):
               
                soc_sum1 = p.apply_async(process_summary,('fbtw1',textBox8,l,E8,cal,E7))
                
            
            elif(var2==2):
                soc_sum2 = p.apply_async(process_summary,('fbtw2',textBox8,l,E8,cal,''))
               
        
        elif(var1==2):
            soc_sum3 = p.apply_async(process_summary,('rss',E9,l,'0','0',''))
         
    while True:
        try:
            if CheckVar1==1:
                a['text']=text_sum.get(timeout=5)
            if CheckVar2==1:
                a['pdf']=pdf_sum.get(timeout=8)
            if CheckVar3==1:
                if var==1:
                    a['url']=url_sum1.get(timeout=60)
                else:
                    a['url']=url_sum2.get(timeout=60)
            if CheckVar4==1:
                if var1==1:
                    if var2==1:
                        a['soc']=soc_sum1.get(timeout = 20)
                    elif var2==2:
                        a['soc']=soc_sum2.get(timeout = 20)
                else:
                    a['soc']=soc_sum3.get(timeout = 20)
            break
        except:
            for worker in p._pool:
                if worker.is_alive():
                    if time.time()-start >=300:
                        worker.terminate()
    p.close()
    p.join()
  
    return a
    
def multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5):
    time.sleep(2)
    a=dict()
    l30 = LabelFrame(canvas7, text="Result Summaries",font = ('Verdana',12))
    l30.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.85)
    proces_labl = Label(canvas7, text="processing")
    proces_labl.place(relx = 0.25, rely = .5)
    if len(SumRes)!=0:
        for label,vbtn,dbtn in SumRes:
            label.place_forget()
            vbtn.place_forget()
            dbtn.place_forget()
        SumRes.clear()
    l=textBox1.get("1.0","end")
    #sent1 = E10.get().rstrip()
    p1=NoDaemonProcessPool(1)
    start = time.time()
    summ = p1.apply_async(display_options,(CheckVar1.get(),CheckVar2.get(),CheckVar3.get(),CheckVar4.get(),E1.get().rstrip(),E2.get().rstrip(),E10.get().rstrip(),E11.get().rstrip(),E3.get().rstrip(),var.get(),l,var1.get(),textBox8.get("1.0","end").strip(),E8.get().rstrip(),cal.get_date().strftime('%Y-%m-%d'),E7.get().rstrip(),E9.get().rstrip(),var2.get(),key.get(),a,E6.get().rstrip(),E4.get().rstrip(),E5.get().rstrip()))
    p1.close()
    p1.join()
    
    k = summ.get()
    if CheckVar1.get()==1:
        sumlab1 = Label(l30, text = "Text file Summarization: ",font = ('Verdana',12))
        vbtn1 = Button(l30, text = "View",font = ('Arial',11),activeforeground='white',activebackground='black',cursor="hand2",command = lambda: showSummary('text',k['text']))
        dbtn1 = Button(l30, text = "Download",cursor="hand2",activeforeground='white',activebackground='black',font = ('Arial',11),command = lambda: writeToFile(text_sum.get(),"Text file Summarized Text.txt"))
        SumRes.append([sumlab1,vbtn1,dbtn1])
    
    if CheckVar2.get()==1:
        sumlab2 = Label(l30, text = "PDF file Summarization: ",font = ('Verdana',12))
        vbtn2 = Button(l30, text = "View",font = ('Arial',11),cursor="hand2",activeforeground='white',activebackground='black',command = lambda: showSummary('pdf',k['pdf']))
        dbtn2 = Button(l30, text = "Download",cursor="hand2",activeforeground='white',activebackground='black',font = ('Arial',11),command = lambda: writeToFile(pdf_sum.get(),"PDF file Summarized Text.txt"))
        SumRes.append([sumlab2,vbtn2,dbtn2])
        
    if CheckVar3.get()==1:
        if(var.get()==1):
           
            sumlab31 = Label(l30, text = "URL Summarization: ",font = ('Verdana',12))
            vbtn31 = Button(l30, text = "View",font = ('Arial',11),cursor="hand2",activeforeground='white',activebackground='black',command = lambda: showSummary('url',k['url']))
            dbtn31 = Button(l30, text = "Download",cursor="hand2",activeforeground='white',activebackground='black',font = ('Arial',11),command = lambda: writeToFile(url_sum1.get(),"URL Summarized Text.txt"))
            SumRes.append([sumlab31,vbtn31,dbtn31])
        elif(var.get()==2):
            
            sumlab32 = Label(l30, text = "Wikipedia Summarization: ",font = ('Verdana',12))
            vbtn32 = Button(l30, text = "View",font = ('Arial',11),activeforeground='white',activebackground='black',cursor="hand2",command = lambda: showSummary('wiki',k['url']))
            dbtn32 = Button(l30, text = "Download",cursor="hand2",activeforeground='white',activebackground='black',font = ('Arial',11),command = lambda: writeToFile(url_sum2.get(),"Wikipedia Summarized Text.txt"))
            SumRes.append([sumlab32,vbtn32,dbtn32])
    
    if CheckVar4.get()==1:
        if(var1.get()==1):
           
            if(var2.get()==1):
             
                sumlab41 = Label(l30, text = "Social Media Summarization: ",font = ('Verdana',12))
                vbtn41 = Button(l30, text = "View",font = ('Arial',11),activeforeground='white',activebackground='black',cursor="hand2",command = lambda: showSummary('fbtw1',k['soc']))
                dbtn41 = Button(l30, text = "Download",activeforeground='white',activebackground='black',font = ('Arial',11),cursor="hand2",command = lambda: writeToFile(soc_sum1.get(),"Facebook Posts and Twitter Tweets Summarized Text.txt"))
                SumRes.append([sumlab41,vbtn41,dbtn41])
            
            elif(var2.get()==2):
              
                sumlab42 = Label(l30, text = "Social Media Summarization: ",font = ('Verdana',12))
                vbtn42 = Button(l30, text = "View",cursor="hand2",font = ('Arial',11),activeforeground='white',activebackground='black',command = lambda: showSummary('fbtw2',k['soc']))
                dbtn42 = Button(l30, text = "Download",cursor="hand2",activeforeground='white',activebackground='black',font = ('Arial',11),command = lambda: writeToFile(soc_sum2.get(),"Facebook Posts and Twitter Tweets Summarized Text.txt"))
                SumRes.append([sumlab42,vbtn42,dbtn42])
        
        elif(var1.get()==2):
           
            sumlab43 = Label(l30, text = "Social Media Summarization: ",font = ('Verdana',12))
            vbtn43 = Button(l30, text = "View",cursor="hand2",font = ('Arial',11),activeforeground='white',activebackground='black',command = lambda: showSummary('rss',k['soc']))
            dbtn43 = Button(l30, text = "Download",cursor="hand2",activeforeground='white',activebackground='black',font = ('Arial',11),command = lambda: writeToFile(soc_sum3.get(),"RSS Feeds Summarized Text.txt"))
            SumRes.append([sumlab43,vbtn43,dbtn43])
    
    proces_labl.place_forget()
    y = .1
    for label,vbtn,dbtn in SumRes:
        label.place(relx=.05,rely = y)
        vbtn.place(relx=.5,rely = y, relwidth = .1)
        dbtn.place(relx=.65,rely = y, relwidth = .15)
        y+=.1
    canvas8.pack_forget()
    canvas7.pack(fill=BOTH,expand=YES)
    
class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.with_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete("1.0", "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get("end") == '':
            entry.insert("1.0", state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.with_placeholder = True

    entry.insert(INSERT, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

def pdf_to_text(path):
    text=[]
    resrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(resrcmgr, device)
    
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    for page in PDFPage.get_pages(fp,(0,1)):
        interpreter.process_page(page)
        layout = device.get_result()
        for ele in layout:
            #extracting text paragraph wise
            if isinstance(ele, LTTextBox):
                t = ele.get_text()
                if not t.isspace() and not len(t)==0:
                    text.append(t)
    fp.close()
    device.close()
    
    return text

def add_placeholder_to1(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.with_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.with_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

def add_placeholder_to2(scrolledText, placeholder, color="grey", font=None):
    normal_color = scrolledText.cget("fg")
    normal_font = scrolledText.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.with_placeholder=True

    def on_focusin(event, entry=scrolledText, state=state):
        if state.with_placeholder:
            entry.delete("1.0", "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
            state.with_placeholder = False

    def on_focusout(event, entry=scrolledText, state=state):
        if len(entry.get("1.0","end"))==1 and entry.get("1.0","end").isspace():
            entry.insert("1.0", state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            state.with_placeholder = True

    scrolledText.insert(INSERT, placeholder)
    scrolledText.config(fg = color, font=font)

    scrolledText.bind('<FocusIn>', on_focusin, add="+")
    scrolledText.bind('<FocusOut>', on_focusout, add="+")
    
    scrolledText.placeholder_state = state

    return state

def change_color(nextButton):
    def change_color1():
        current_color = nextButton1.cget("fg")
        next_color = "black" if current_color == "red" else "red"
        nextButton1.config(fg=next_color)
        main.after(1000, change_color1)
    nextButton1=nextButton
    change_color1()

def nextFunction(canvas,canvas2,textBox1,var,l17):
    global keys,options,key
    keys = textBox1.get("1.0","end")
    keys = [opt_key for opt_key in keys.split("\n") if len(opt_key)>0]
    fin_keys=[]
    for k in keys:
        wiki_pages = wikipedia.search(k,results=5)
        if k in wiki_pages:
            fin_keys.append(k)
        else:
           if len(wiki_pages)>0:
               fin_keys+=wiki_pages
    fin_keys=list(set(fin_keys))
    key.set(fin_keys[0])
    options = OptionMenu(l17, key,*fin_keys)
    options.place(relx=.5, rely = .25)
    canvas.pack_forget() 
    canvas2.pack(fill=BOTH,expand=YES)

def prevFunction1(canvas2,canvas):
    canvas2.pack_forget()
    canvas.pack(fill=BOTH,expand=YES)

def nextFunction2(canvas2,canvas3,canvas4,canvas5,canvas6,CheckVar1,CheckVar2,CheckVar3,CheckVar4):
    canvas2.pack_forget()
    if(CheckVar1.get()==1): 
        canvas3.pack(fill=BOTH,expand=YES)
    elif(CheckVar2.get()==1):
        canvas4.pack(fill=BOTH,expand=YES)
    elif(CheckVar3.get()==1):
        canvas5.pack(fill=BOTH,expand=YES)
    elif(CheckVar4.get()==1):
        canvas6.pack(fill=BOTH,expand=YES)
        
def prevFunction2(canvas3,canvas2):
    canvas3.pack_forget()
    canvas2.pack(fill=BOTH,expand=YES)
    
def nextFunction3(canvas3,canvas4,canvas5,canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5):
    if(checkfile(E1.get().rstrip())):
        if(checknumber(E10.get().rstrip())):
            canvas3.pack_forget()  
            if(CheckVar2.get()==1):
                canvas4.pack(fill=BOTH,expand=YES)
            elif(CheckVar3.get()==1):
                canvas5.pack(fill=BOTH,expand=YES)
            elif(CheckVar4.get()==1):
                canvas6.pack(fill=BOTH,expand=YES)
            else:
                canvas8.pack(fill=BOTH,expand=YES)
                multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5)
        else:
            messagebox.showinfo("Invalid entry", "The given number of sentences required in the summary is invalid!!  The number should be an integer.")
    else:
        messagebox.showinfo("File error", "The given file path does not exist!!")
    

def prevFunction3(canvas4,canvas2,CheckVar1):
    canvas4.pack_forget()
    if CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)
        
def nextFunction4(canvas4,canvas5,canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5):
    if(checkfile(E2.get().rstrip())):
        if(checknumber(E11.get().rstrip())):
            canvas4.pack_forget() 
            if(CheckVar3.get()==1):
                canvas5.pack(fill=BOTH,expand=YES)
            elif(CheckVar4.get()==1):
                canvas6.pack(fill=BOTH,expand=YES)
            else:
                canvas8.pack(fill=BOTH,expand=YES)
                multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5)
        else:
            messagebox.showinfo("Invalid entry", "The given number of sentences required in the summary is invalid!!  The number should be an integer.")
    else:
        messagebox.showinfo("File error", "The given file path does not exist!!")


def prevFunction4(canvas5,canvas4,canvas3,canvas2,CheckVar2,CheckVar1):
    canvas5.pack_forget()
    if CheckVar2.get()==1:
        canvas4.pack(fill=BOTH,expand=YES)
    elif CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)

def nextFunction5(canvas5,canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5):
    if(var.get()==1):
        m = validateurl(E3.get().rstrip())
        if(m=="String is a valid URL"):
            if(depthvalidate(E4.get().rstrip())=="valid"):
                if(checknumber(E5.get().rstrip())):
                    canvas5.pack_forget()
                    if(CheckVar4.get()==1):
                        canvas6.pack(fill=BOTH,expand=YES)
                    else:
                        canvas8.pack(fill=BOTH,expand=YES)
                        multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5)
                else:
                    messagebox.showinfo("Invalid entry", "The given number of words required in the summary is invalid!!  The number should be an integer.")
            elif(depthvalidate(E4.get().rstrip())=="depth should be less than or equal to 5"):
                messagebox.showinfo("Invalid entry", "The depth should be less than or equal to 5.")
            elif(depthvalidate(E4.get().rstrip())=="depth should be a number"):
                messagebox.showinfo("Invalid entry", "The given depth is invalid!!  The depth should be an integer.")
        elif(m=="String is not valid URL"):
            messagebox.showinfo("Invalid entry", "The given URL/Website is invalid!!  Please enter a valid URL/Website.")
    elif(var.get()==2):
        if(checknumber(E6.get().rstrip())):
            canvas5.pack_forget()
            if(CheckVar4.get()==1):
                canvas6.pack(fill=BOTH,expand=YES)
            else:
                canvas8.pack(fill=BOTH,expand=YES)
                multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5)
        else:
            messagebox.showinfo("Invalid entry", "The given number of words required in the summary is invalid!!  The number should be an integer.")
                
def prevFunction5(canvas6,canvas5,canvas4,canvas3,canvas2,CheckVar3,CheckVar2,CheckVar1):
    canvas6.pack_forget()
    if CheckVar3.get()==1:
        canvas5.pack(fill=BOTH,expand=YES)
    elif CheckVar2.get()==1:
        canvas4.pack(fill=BOTH,expand=YES)
    elif CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)

def nextFunction6(canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5):
    if(var1.get()==1):
        if(checknumber(E8.get().rstrip())):
            canvas6.pack_forget()
            canvas8.pack(fill=BOTH, expand=YES)
            multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5)
        else:
            messagebox.showinfo("Invalid entry", "The given number of facebook posts or tweets required for the data extraction is invalid!!  The number should be an integer.")
    elif(var1.get()==2):
        r = validateurl(E9.get().rstrip())
        if(r=="String is a valid URL"):
            canvas6.pack_forget()
            canvas8.pack(fill=BOTH, expand=YES)
            multiprocess(canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5)
        elif(r=="String is not valid URL"):
            messagebox.showinfo("Invalid entry", "The given link for the xml format of RSS Feeds is invalid!!  Please enter a valid link.")

def prevFunction6(canvas7,canvas6,canvas5,canvas4,canvas3,canvas2,CheckVar4,CheckVar3,CheckVar2,CheckVar1):
    canvas7.pack_forget()
    if CheckVar4.get()==1:
        canvas6.pack(fill=BOTH,expand=YES)
    elif CheckVar3.get()==1:
        canvas5.pack(fill=BOTH,expand=YES)
    elif CheckVar2.get()==1:
        canvas4.pack(fill=BOTH,expand=YES)
    elif CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)

def disable_b1(textBox1,nextButton,main):
    def disable_b11():
        if(textBox1.get("1.0","end")=='\n' or textBox1.get("1.0","end")=="Enter the keywords to be searched (in every new line)....\n"):
            nextButton.config(state=DISABLED)
            main.after(10, disable_b11)
        else:
            nextButton.config(state=NORMAL)
            main.after(10, disable_b11)

    disable_b11()

def disable_b2(CheckVar1,CheckVar2,CheckVar3,CheckVar4,nextButton2,main):
    def disable_b21():
        if(CheckVar1.get()==0 and CheckVar2.get()==0 and CheckVar3.get()==0 and CheckVar4.get()==0):
            nextButton2.config(state=DISABLED)
            main.after(10, disable_b21)
        else:
            nextButton2.config(state=NORMAL)
            main.after(10, disable_b21)
    disable_b21()
        
def disable_b3(E1,E10,nextButton3,extrtbt,main):
    def disable_b31():
        if(E1.get().rstrip()=='' or E1.get().rstrip()=='Browse File Directory....' or E10.get().rstrip()==''):
            nextButton3.config(state=DISABLED)
            extrtbt.config(state=DISABLED)
            if(E1.get().rstrip()!='' and E1.get().rstrip()!='Browse File Directory....'):
                extrtbt.config(state=NORMAL)
            main.after(10, disable_b31)
        else:
            extrtbt.config(state=NORMAL)
            nextButton3.config(state=NORMAL)
            main.after(10, disable_b31)
    disable_b31()
        
def disable_b4(E2,E11,extrtbt1,nextButton4,main):
    def disable_b41():
        if(E2.get().rstrip()=='' or E2.get().rstrip()=='Browse File Directory....' or E11.get().rstrip()==''):
            extrtbt1.config(state=DISABLED)
            nextButton4.config(state=DISABLED)
            if(E2.get().rstrip()!='' and E2.get().rstrip()!='Browse File Directory....'):
                extrtbt1.config(state=NORMAL)
            main.after(10, disable_b41)
        else:
            extrtbt1.config(state=NORMAL)
            nextButton4.config(state=NORMAL)
            main.after(10, disable_b41)
    disable_b41()
    
def disable_b5(var,E3,E4,E5,E6,nextButton5,main):
    def disable_b51():
        if((var.get()==1 and (E3.get().rstrip()=='' or E3.get().rstrip()=='Enter the URL here.....' or E4.get().rstrip()=='' or E5.get().rstrip()=='')) or (var.get()==2 and E6.get().rstrip()=='') or var.get()==0):
            nextButton5.config(state=DISABLED)
            main.after(10, disable_b51)
        else:
            nextButton5.config(state=NORMAL)
            main.after(10, disable_b51)
    disable_b51()

def disable_b6(var1,var2,textBox8,E7,E8,cal,E9,nextButton6,main):
    def disable_b61():
        if((var1.get()==1 and ((var2.get()==1 and (textBox8.get("1.0","end").rstrip()=='' or textBox8.get("1.0","end").rstrip()=='Enter the token here....' or E7.get().rstrip()=='Enter the Screen Name here....' or E8.get().rstrip()=='' or cal.get_date()=='')) or (var2.get()==2 and (textBox8.get("1.0","end").rstrip()=='' or textBox8.get("1.0","end").rstrip()=='Enter the token here....' or E8.get().rstrip()=='' or cal.get_date()=='')) or var2.get()==0)) or (var1.get()==2 and (E9.get().rstrip()=='' or E9.get().rstrip()=='Enter the link here....')) or var1.get()==0):
            nextButton6.config(state=DISABLED)
            main.after(10, disable_b61)
        else:
            nextButton6.config(state=NORMAL)
            main.after(10, disable_b61)
    disable_b61()

def fileDialog(state1,E1):
    E1.delete(0, "end")
    E1.config(fg = state1.normal_color, font=state1.normal_font)
    state1.with_placeholder=False
    
    filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File", filetypes =(("Text files","*.txt"), ("all files", "*.*")))
    E1.insert(INSERT,filename)

def fileDialog1(state2,E2):
    E2.delete(0, "end")
    E2.config(fg = state2.normal_color, font=state2.normal_font)
    state2.with_placeholder=False
    
    filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File",filetypes =(("PDF files","*.pdf"), ("all files", "*.*")))
    E2.insert(INSERT,filename)

def extract(canvas3,l7,textBox4,E1):
    if(checkfile(E1.get().rstrip())):
        canvas3.config(cursor="watch")
        l7.place(relx=.05,rely=.38)
        f = open(E1.get().rstrip(),'r', encoding='utf-8')
        data=f.readlines()
        char_list = [data[i][j] for i in range(len(data)) for j in range(len(data[i])) if ord(data[i][j]) in range(65536)]
        data1=''
        for j in char_list:
            data1=data1+j
        textBox4.place(relx=.05,rely=.46,relwidth=0.9,relheight=0.49)
        textBox4.config(state=NORMAL)
        textBox4.delete("1.0", "end")
        textBox4.insert(INSERT,data1)
        textBox4.config(state=DISABLED)
        canvas3.config(cursor="")
    else:
        messagebox.showinfo("File error", "The given file path does not exist!!")

def extract1(canvas4,l10,E2,textBox6):
    canvas4.config(cursor="watch")
    l10.place(relx=.05,rely=.38)
    doc = pdf_to_text(E2.get().rstrip())  
    doc = ' '.join(doc)
    textBox6.place(relx=.05,rely=.46,relwidth=0.9,relheight=0.49)
    textBox6.config(state=NORMAL)
    textBox6.delete("1.0", "end")
    textBox6.insert(INSERT,doc)
    textBox6.config(state=DISABLED)
    canvas4.config(cursor="")

def sel(l17,l18,E6,l13,l14,E3,l15,E4,l16,E5):
    l17.place_forget()
    l18.place_forget()
    E6.place_forget()
    l13.place(relx=.05,rely=.2,relwidth = .9, relheight = .75)
    
    l14.place(relx=.05,rely=.05)
    E3.place(relx=.25,rely=.05, relheight = .1,relwidth = .7)
    
    l15.place(relx=.05,rely=.4)
    E4.place(relx=.5,rely=.4,relwidth=0.1,relheight=0.1)
    l16.place(relx=.05,rely=.6)
    E5.place(relx=.5,rely=.6,relwidth=0.1,relheight=0.1)

def sel1(l13,l14,E3,l15,E4,l16,E5,l17,l18,E6,key,l21,keys):
    l13.place_forget()
    l14.place_forget()
    E3.place_forget()
    l15.place_forget()
    E4.place_forget()
    l16.place_forget()
    E5.place_forget()
    l17.place(relx=.05,rely=.2,relwidth = .9, relheight = .75)
    
    key.set(keys[0])
    l21.place(relx=.05,rely=.25)
    l18.place(relx=.05,rely=.48)
    E6.place(relx=.5,rely=.48,relwidth=0.1,relheight=0.1)
    
    
def sel2(l28,l29,E9,l22,l23,textBox8,l24,l26,E8,l27,cal,R5,R6):
    l28.place_forget()
    l29.place_forget()
    E9.place_forget()
    l22.place(relx=.05,rely=.2,relwidth = .9, relheight = .75)
    l23.place(relx=.05,rely=.01)
    
    textBox8.place(relx=.05,rely=.1,relwidth=0.9,relheight=0.15)
    l24.place(relx=.05,rely=.3)
    
    l26.place(relx=.05,rely=.6)
    E8.place(relx=.777,rely=.625,relwidth=0.2,relheight=0.1)
    l27.place(relx=.05,rely=.8)
    cal.place(relx=.7762,rely=.8)
    R5.place(relx=.75,rely=.3,relwidth=0.1,relheight=0.1)
    R6.place(relx=.85,rely=.3,relwidth=0.1,relheight=0.1)

def sel3(l22,l23,textBox8,l24,l26,E8,l27,cal,R5,R6,l28,l29,E9):
    l22.place_forget()
    l23.place_forget()
    textBox8.place_forget()
    l24.place_forget()
    l26.place_forget()
    E8.place_forget()
    l27.place_forget()
    cal.place_forget()
    R5.place_forget()
    R6.place_forget()
    
    l28.place(relx=.05,rely=.2,relwidth = .9, relheight = .75)
    
    l29.place(relx=.05,rely=.3)
    E9.place(relx=.05,rely=.5,relwidth=0.9,relheight=0.1)
    
def sel4(l25,E7):
    l25.place(relx=.05,rely=.45)
    E7.place(relx=.5,rely=.45,relwidth=0.45,relheight=0.1)
    
def sel5(l25,E7):
    l25.place_forget()
    E7.place_forget()

def close(main):
    main.destroy()
    
if __name__ == "__main__":
    main = tk.Tk()
    main.resizable(False, False)
    screenWidth = main.winfo_screenwidth()
    screenHeight = main.winfo_screenheight()
    
    windowWidth = screenWidth//2
    windowHeight = screenHeight//2
    
    positionRight = int(screenWidth//2 - windowWidth//2)
    positionDown = int(screenHeight//2 - windowHeight//2)
    
    main.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
    #print("Width",windowWidth,"Height",windowHeight)
    main.title("Smart Summarizer")
    
    frame = tk.Frame(main)
    frame.pack(fill = BOTH, expand = YES)
    
    
    canvas3 = tk.Canvas(frame,highlightthickness = 0) 
    canvas4 = tk.Canvas(frame,highlightthickness = 0) 
    canvas5 = tk.Canvas(frame,highlightthickness = 0) 
    canvas6 = tk.Canvas(frame,highlightthickness = 0) 
    canvas7 = tk.Canvas(frame,highlightthickness = 0) 
    canvas8 = tk.Canvas(frame,highlightthickness = 0) 
    l11 = LabelFrame(canvas5, text="Extraction from URL/Website",font = ('Verdana',12))
    l17 = LabelFrame(l11, text="For Wikipedia",font = ('Verdana',11))
    
    
    canvas = tk.Canvas(frame, highlightthickness = 0) 
    
    l2 = Label(canvas, text="Welcome to Smart Summarizer...",font = ('times new roman',20,'bold','italic'))
    l2.place(relx = .25)
    
    l1 = LabelFrame(canvas, text="Enter the search keywords/terms: ",font = ('Verdana',12))
    l1.place(relx=.1, rely = .1,relwidth = 0.8,relheight =  0.8)
    
    textBox1 = scrolledtext.ScrolledText(l1,wrap=NONE)
    textBox1.place(relx = .05, rely = .05, relheight =.8, relwidth = .9)
    
    xscrollbar = Scrollbar(l1, orient=HORIZONTAL,cursor="arrow")
    xscrollbar.place(relx = .05, rely = .85, relwidth = .90)
    
    textBox1.config(xscrollcommand=xscrollbar.set)
    xscrollbar.config(command=textBox1.xview)
    add_placeholder_to2(textBox1, 'Enter the keywords to be searched (in every new line)....')
    canvas1 = tk.Canvas(frame,highlightthickness = 0) 
    
    canvas2 = tk.Canvas(frame,highlightthickness = 0) 
    var = IntVar()
    nextButton = tk.Button(canvas, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction(canvas,canvas2,textBox1,var,l17))
    disable_b1(textBox1,nextButton,main)
    nextButton.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt1 = tk.Button(canvas, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt1.place(relx = .875, rely = .9, relwidth = .1)
    
    change_color(nextButton)
    canvas.pack(fill=BOTH,expand=YES)
    
    
    l4 = LabelFrame(canvas2, text="Extract data from:",font = ('Verdana',12))
    l4.place(relx=.1,rely=.1,relwidth=.8,relheight=.8)
    
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    CheckVar4 = IntVar()
    c1 = Checkbutton(l4, text = "Text file",font = ('Arial',11), variable = CheckVar1,onvalue = 1, offvalue = 0,anchor = W)
    c2 = Checkbutton(l4, text = "PDF Document",font = ('Arial',11), variable = CheckVar2,onvalue = 1, offvalue = 0,anchor = W)
    c3 = Checkbutton(l4, text = "URL/Website",font = ('Arial',11), variable = CheckVar3,onvalue = 1, offvalue = 0,anchor = W)
    c4 = Checkbutton(l4, text = "Social Media",font = ('Arial',11), variable = CheckVar4,onvalue = 1, offvalue = 0,anchor = W)
    c1.place(relx=.1,rely=.1, relheight = .2, relwidth = .5)
    c2.place(relx=.1,rely=.3, relheight = .2, relwidth = .5)
    c3.place(relx=.1,rely=.5, relheight = .2, relwidth = .5)
    c4.place(relx=.1,rely=.7, relheight = .2, relwidth = .5)

    backButton1 = tk.Button(canvas2, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction1(canvas2,canvas))
    backButton1.place(relx = .625, rely = .9, relwidth = .1)
    
    
    nextButton2 = tk.Button(canvas2, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction2(canvas2,canvas3,canvas4,canvas5,canvas6,CheckVar1,CheckVar2,CheckVar3,CheckVar4))
    disable_b2(CheckVar1,CheckVar2,CheckVar3,CheckVar4,nextButton2,main)
    nextButton2.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt2 = tk.Button(canvas2, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt2.place(relx = .875, rely = .9, relwidth = .1)
    
    
    ########## Declaration of variables ###########
    
    l5 = LabelFrame(canvas3, text="Extraction from Text File",font = ('Verdana',12))
    l6 = LabelFrame(l5, text="Text file location: ",font = ('Verdana',10))
    E1 = tk.Entry(l6)
    l32 = Label(l5, text="Number of sentences required in the summary: ",font = ('Verdana',10))
    E10 = tk.Entry(l5,justify=CENTER)
    l7 = Label(l5, text="Extracted Data: ",font = ('Verdana',10))
    
    l8 = LabelFrame(canvas4, text="Extraction from PDF Document",font = ('Verdana',12))
    l9 = LabelFrame(l8, text="PDF file location: ",font = ('Verdana',10))
    E2 = tk.Entry(l9)
    l33 = Label(l8, text="Number of sentences required in the summary: ",font = ('Verdana',10))
    E11 = tk.Entry(l8,justify=CENTER)
    l10 = Label(l8, text="Extracted Data: ",font = ('Verdana',10))
    textBox6 = scrolledtext.ScrolledText(l8,wrap=WORD,fg="black")
    
    l12 = LabelFrame(l11, text="Select the desired option: ",font = ('Verdana',11))
    l13 = LabelFrame(l11, text="For URL",font = ('Verdana',11))
    l14 = Label(l13, text="Enter the URL: ",font = ('Verdana',10))
    E3 = tk.Entry(l13)
    l15 = Label(l13, text="Depth: ",font = ('Verdana',10))
    E4 = tk.Entry(l13,justify=CENTER)
    l16 = Label(l13, text="Number of words to generate: ",font = ('Verdana',10))
    E5 = tk.Entry(l13,justify=CENTER)
    
    key = StringVar(l17)
    l21 = Label(l17, text="Select one keyword from list: ",font = ('Verdana',10))
    l18 = Label(l17, text="Number of words to generate: ",font = ('Verdana',10))
    E6 = tk.Entry(l17,justify=CENTER)
    
    l19 = LabelFrame(canvas6, text="Extraction from Social Media",font = ('Verdana',12))
    var1 = IntVar()
    var2 = IntVar()
    
    l20 = LabelFrame(l19, text="Select the desired option: ",font = ('Verdana',11))
    l22 = LabelFrame(l19, text="For Facebook posts and Twitter tweets",font = ('Verdana',11))
    l23 = Label(l22, text="Access Token for Facebook Graph API Explorer: ",font = ('Verdana',10))
    textBox8 = scrolledtext.ScrolledText(l22,wrap=WORD,fg="black")
    l24 = Label(l22, text="Do you want to extract tweets of a specific user/company?",font = ('Verdana',10))
    l25 = Label(l22, text="Screen Name of the Twitter handle: ",font = ('Verdana',10))
    E7 = tk.Entry(l22)
    l26 = Label(l22, text="Number of facebook posts or tweets required\n for the data extraction: ",font = ('Verdana',10))
    E8 = tk.Entry(l22,justify=CENTER)
    l27 = Label(l22, text="Date from when the tweets and facebook posts were made: ",font = ('Verdana',10))
    l28 = LabelFrame(l19, text="For RSS Feeds",font = ('Verdana',11))
    l29 = Label(l28, text="Link for the xml format of RSS Feeds: ",font = ('Verdana',10))
    E9 = tk.Entry(l28)
    
    SumRes=[]
    
    
    ########## Text File ###########
    
    
    l5.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.85)
    
    l6.place(relx=.05,rely=.05,relwidth = .9, relheight = .15)
    
    
    E1.place(relx=.01,rely=.1, relwidth=0.79, relheight = 0.8)
    state1=add_placeholder_to1(E1, 'Browse File Directory....')
    
    brbt = tk.Button(l6, text = 'Browse',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=10,command = lambda: fileDialog(state1,E1))
    brbt.place(relx=.85,rely=0.1, relwidth=0.14, relheight=0.8)
    
    l32.place(relx=.05,rely=.3,relheight=0.075)
    
    
    E10.place(relx=.54,rely=.3,relwidth=0.1,relheight=0.075)
    
    
    
    textBox4 = scrolledtext.ScrolledText(l5,wrap=WORD,fg="black")
    extrtbt = tk.Button(l5, text = 'Preview',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=14,command = lambda: extract(l5,l7,textBox4,E1))
    
    extrtbt.place(relx=.41,rely=.2)
    
    backButton2 = tk.Button(canvas3, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction2(canvas3,canvas2))
    backButton2.place(relx = .625, rely = .9, relwidth = .1)
    
    nextButton3 = tk.Button(canvas3, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction3(canvas3,canvas4,canvas5,canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5))
    disable_b3(E1,E10,nextButton3,extrtbt,main)
    nextButton3.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt3 = tk.Button(canvas3, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt3.place(relx = .875, rely = .9, relwidth = .1)
    
    
    ############ PDF File ############
    
    l8.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.85)
    
    l9.place(relx=.05,rely=.05,relwidth = .9, relheight = .15)
    
    E2.place(relx=.01,rely=.1, relwidth=0.79, relheight = 0.8)
    state2=add_placeholder_to1(E2, 'Browse File Directory....')
    
    brbt1 = tk.Button(l9, text = 'Browse',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=10,command = lambda: fileDialog1(state2,E2))
    brbt1.place(relx=.85,rely=0.1, relwidth=0.14, relheight=0.8)
    
    l33.place(relx=.05,rely=.3,relheight=0.075)
    
    E11.place(relx=.54,rely=.3,relwidth=0.1,relheight=0.075)
    
    extrtbt1 = tk.Button(l8, text = 'Preview',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=14,command = lambda: extract1(canvas4,l10,E2,textBox6))
    extrtbt1.place(relx=.41,rely=.2)
    
    backButton2 = tk.Button(canvas4, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction3(canvas4,canvas2,CheckVar1))
    backButton2.place(relx = .625, rely = .9, relwidth = .1)
    
    nextButton4 = tk.Button(canvas4, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction4(canvas4,canvas5,canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5))
    disable_b4(E2,E11,extrtbt1,nextButton4,main)
    nextButton4.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt4 = tk.Button(canvas4, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt4.place(relx = .875, rely = .9, relwidth = .1)
    
    
    ############## URL / Wikipedia ###########
        
    l11.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.85)
    
    l12.place(relx=.05,rely=.05,relwidth = .9, relheight = .15)
    
    add_placeholder_to1(E3, 'Enter the URL here.....')
    
    R1 = Radiobutton(l12, text="URL", variable=var, value=1,command=lambda: sel(l17,l18,E6,l13,l14,E3,l15,E4,l16,E5),font=('Verdana',11))
    R1.place(relx=.1,rely=.05, relheight=.9)
    
    R2 = Radiobutton(l12, text="Wikipedia", variable=var, value=2,command=lambda: sel1(l13,l14,E3,l15,E4,l16,E5,l17,l18,E6,key,l21,keys),font=('Verdana',11))
    R2.place(relx=.5,rely=.05, relheight=.9)
    
    backButton3 = tk.Button(canvas5, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction4(canvas5,canvas4,canvas3,canvas2,CheckVar2,CheckVar1))
    backButton3.place(relx = .625, rely = .9, relwidth = .1)
    
    nextButton5 = tk.Button(canvas5, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction5(canvas5,canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5))
    disable_b5(var,E3,E4,E5,E6,nextButton5,main)
    nextButton5.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt5 = tk.Button(canvas5, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt5.place(relx = .875, rely = .9, relwidth = .1)
    
    
    ############# social media ################
    
    l19.place(relx=0.05,rely=0.05, relwidth = .9, relheight=0.85)
    
    l20.place(relx=.05,rely=.05,relwidth = .9, relheight = .15)
    
    add_placeholder_to2(textBox8, 'Enter the token here....')
    
    add_placeholder_to1(E7, 'Enter the Screen Name here....')
    
    cal = DateEntry(l22, width=12, background='darkblue',date_pattern='yyyy-MM-dd',foreground='white', borderwidth=2)
    
   
    R5 = Radiobutton(l22, text="Yes", variable=var2, value=1,command=lambda: sel4(l25,E7),font=('Verdana',10))
    
    R6 = Radiobutton(l22, text="No", variable=var2, value=2,command=lambda: sel5(l25,E7),font=('Verdana',10))
    
    add_placeholder_to1(E9, 'Enter the link here....')
    
    R3 = Radiobutton(l20, text="Facebook posts and Twitter tweets", variable=var1, value=1,command=lambda: sel2(l28,l29,E9,l22,l23,textBox8,l24,l26,E8,l27,cal,R5,R6),font=('Verdana',10))
    R3.place(relx=.05,rely=.05, relheight=.9)
    
    R4 = Radiobutton(l20, text="RSS Feeds", variable=var1, value=2,command=lambda: sel3(l22,l23,textBox8,l24,l26,E8,l27,cal,R5,R6,l28,l29,E9),font=('Verdana',10))
    R4.place(relx=.7,rely=.05, relheight=.9)
    
    backButton4 = tk.Button(canvas6, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction5(canvas6,canvas5,canvas4,canvas3,canvas2,CheckVar3,CheckVar2,CheckVar1))
    backButton4.place(relx = .625, rely = .9, relwidth = .1)
    
    nextButton6 = tk.Button(canvas6, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction6(canvas6,canvas7,canvas8,CheckVar1,CheckVar2,CheckVar3,CheckVar4,SumRes,E1,E2,E10,E11,E3,var,textBox1,var1,textBox8,E8,cal,E7,E9,var2,key,E6,E4,E5))
    disable_b6(var1,var2,textBox8,E7,E8,cal,E9,nextButton6,main)
    nextButton6.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt6 = tk.Button(canvas6, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt6.place(relx = .875, rely = .9, relwidth = .1)
    
    ################### Processing ################
    
    process_labl = Label(canvas8, text = 'processing')
    process_labl.pack()
    
    ################### Result ###################
    
    
    backButton5 = tk.Button(canvas7, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction6(canvas7,canvas6,canvas5,canvas4,canvas3,canvas2,CheckVar4,CheckVar3,CheckVar2,CheckVar1))
    backButton5.place(relx = .75, rely = .9, relwidth = .1)
    
    clbt6 = tk.Button(canvas7, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close(main))
    clbt6.place(relx = .875, rely = .9, relwidth = .1)
    
    
    main.mainloop()