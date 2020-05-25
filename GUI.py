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
    
from tkcalendar import Calendar, DateEntry

#import os
import re
import string
#importing libraries for pdf extraction
# Base library: pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


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

def nextFunction():
    canvas.pack_forget() 
    canvas2.pack(fill=BOTH,expand=YES)

def prevFunction1():
    canvas2.pack_forget()
    canvas.pack(fill=BOTH,expand=YES)

def nextFunction2():
    canvas2.pack_forget()
    if(CheckVar1.get()==1): 
        canvas3.pack(fill=BOTH,expand=YES)
    elif(CheckVar2.get()==1):
        canvas4.pack(fill=BOTH,expand=YES)
    elif(CheckVar3.get()==1):
        canvas5.pack(fill=BOTH,expand=YES)
    elif(CheckVar4.get()==1):
        canvas6.pack(fill=BOTH,expand=YES)
        
def prevFunction2():
    canvas3.pack_forget()
    canvas2.pack(fill=BOTH,expand=YES)
    
def nextFunction3():
    canvas3.pack_forget()  
    if(CheckVar2.get()==1):
        canvas4.pack(fill=BOTH,expand=YES)
    elif(CheckVar3.get()==1):
        canvas5.pack(fill=BOTH,expand=YES)
    elif(CheckVar4.get()==1):
        canvas6.pack(fill=BOTH,expand=YES)
    else:
        canvas7.pack(fill=BOTH,expand=YES)

def prevFunction3():
    canvas4.pack_forget()
    if CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)
        
def nextFunction4():
    canvas4.pack_forget() 
    if(CheckVar3.get()==1):
        canvas5.pack(fill=BOTH,expand=YES)
    elif(CheckVar4.get()==1):
        canvas6.pack(fill=BOTH,expand=YES)
    else:
        canvas7.pack(fill=BOTH,expand=YES)

def prevFunction4():
    canvas5.pack_forget()
    if CheckVar2.get()==1:
        canvas4.pack(fill=BOTH,expand=YES)
    elif CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)

def nextFunction5():
    canvas5.pack_forget()
    if(CheckVar4.get()==1):
        canvas6.pack(fill=BOTH,expand=YES)
    else:
        canvas7.pack(fill=BOTH,expand=YES)

def prevFunction5():
    canvas6.pack_forget()
    if CheckVar3.get()==1:
        canvas5.pack(fill=BOTH,expand=YES)
    elif CheckVar2.get()==1:
        canvas4.pack(fill=BOTH,expand=YES)
    elif CheckVar1.get()==1:
        canvas3.pack(fill=BOTH,expand=YES)
    else:
        canvas2.pack(fill=BOTH,expand=YES)

def nextFunction6():
    canvas6.pack_forget()
    canvas7.pack(fill=BOTH, expand=YES)

def prevFunction6():
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
    
def writeToFile(textBox):
    file = open('Summarized text.txt','w')
    file.write(textBox.get("1.0","end") + '\n')
    file.close()

def disable_b1():
    if(textBox1.get("1.0","end")=='\n' or textBox1.get("1.0","end")=="Enter the keywords to be searched (in every new line)....\n"):
        nextButton.config(state=DISABLED)
        main.after(10, disable_b1)
    else:
        nextButton.config(state=NORMAL)
        main.after(10, disable_b1)
    #print(textBox1.get("1.0","end"))
    #main.after(10, disable_b1)

def disable_b2():
    if(CheckVar1.get()==0 and CheckVar2.get()==0 and CheckVar3.get()==0 and CheckVar4.get()==0):
        nextButton2.config(state=DISABLED)
        main.after(10, disable_b2)
    else:
        nextButton2.config(state=NORMAL)
        main.after(10, disable_b2)
        
def disable_b3():
    if(E1.get().rstrip()=='' or E1.get().rstrip()=='Browse File Directory....'):
        extrtbt.config(state=DISABLED)
        nextButton3.config(state=DISABLED)
        main.after(10, disable_b3)
    else:
        extrtbt.config(state=NORMAL)
        nextButton3.config(state=NORMAL)
        main.after(10, disable_b3)
        
def disable_b4():
    if(E2.get().rstrip()=='' or E2.get().rstrip()=='Browse File Directory....'):
        extrtbt1.config(state=DISABLED)
        nextButton4.config(state=DISABLED)
        main.after(10, disable_b4)
    else:
        extrtbt1.config(state=NORMAL)
        nextButton4.config(state=NORMAL)
        main.after(10, disable_b4)
    
def disable_b5():
    if((var.get()==1 and (E3.get().rstrip()=='' or E3.get().rstrip()=='Enter the URL here.....' or E4.get().rstrip()=='' or E5.get().rstrip()=='')) or (var.get()==2 and E6.get().rstrip()=='') or var.get()==0):
        nextButton5.config(state=DISABLED)
        main.after(10, disable_b5)
    else:
        nextButton5.config(state=NORMAL)
        main.after(10, disable_b5)

def disable_b6():
    if((var1.get()==1 and ((var2.get()==1 and (textBox8.get("1.0","end").rstrip()=='' or textBox8.get("1.0","end").rstrip()=='Enter the token here....' or E7.get().rstrip()=='Enter the Screen Name here....' or E8.get().rstrip()=='' or cal.get_date()=='')) or (var2.get()==2 and (textBox8.get("1.0","end").rstrip()=='' or textBox8.get("1.0","end").rstrip()=='Enter the token here....' or cal.get_date()=='')) or var2.get()==0)) or (var1.get()==2 and (E9.get().rstrip()=='' or E9.get().rstrip()=='Enter the link here....')) or var1.get()==0):
        nextButton6.config(state=DISABLED)
        main.after(10, disable_b6)
    else:
        nextButton6.config(state=NORMAL)
        main.after(10, disable_b6)

def fileDialog(state1):
    E1.delete(0, "end")
    E1.config(fg = state1.normal_color, font=state1.normal_font)
    state1.with_placeholder=False
    
    filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File", filetypes =(("Text files","*.txt"), ("all files", "*.*")))
    E1.insert(INSERT,filename)

def fileDialog1(state2):
    E2.delete(0, "end")
    E2.config(fg = state2.normal_color, font=state2.normal_font)
    state2.with_placeholder=False
    
    filename = filedialog.askopenfilename(initialdir =  "~", title = "Select A File",filetypes =(("PDF files","*.pdf"), ("all files", "*.*")))
    E2.insert(INSERT,filename)

def extract():
    canvas3.config(cursor="watch")
    l7.place(relx=.1,rely=.4)
    f = open(E1.get().rstrip(),'r', encoding='utf-8')
    data=f.readlines()
    char_list = [data[i][j] for i in range(len(data)) for j in range(len(data[i])) if ord(data[i][j]) in range(65536)]
    data1=''
    for j in char_list:
        data1=data1+j
    textBox4.place(relx=.1,rely=.5,relwidth=0.8,relheight=0.3)
    textBox4.config(state=NORMAL)
    textBox4.delete("1.0", "end")
    textBox4.insert(INSERT,data1)
    textBox4.config(state=DISABLED)
    canvas3.config(cursor="")

def extract1():
    canvas4.config(cursor="watch")
    l10.place(relx=.1,rely=.4)
    doc = pdf_to_text(E2.get().rstrip())  
    doc = ' '.join(doc)
    textBox6.place(relx=.1,rely=.5,relwidth=0.8,relheight=0.3)
    textBox6.config(state=NORMAL)
    textBox6.delete("1.0", "end")
    textBox6.insert(INSERT,doc)
    textBox6.config(state=DISABLED)
    canvas4.config(cursor="")

def sel():
    l17.place_forget()
    l18.place_forget()
    E6.place_forget()
    l13.place(relx=.1,rely=.2)
    
    # line6=canvas5.create_line(70,98,88,98)
    # line7=canvas5.create_line(70,98,70,350)
    # line8=canvas5.create_line(70,350,698,350)
    # line9=canvas5.create_line(698,350,698,98)
    # line10=canvas5.create_line(698,98,140,98)
    
    l14.place(relx=.1,rely=.3)
    E3.place(relx=.1,rely=.35,relwidth=0.8,relheight=0.056)
    
    l15.place(relx=.1,rely=.48)
    E4.place(relx=.5,rely=.48,relwidth=0.1,relheight=0.056)
    l16.place(relx=.1,rely=.65)
    E5.place(relx=.5,rely=.65,relwidth=0.1,relheight=0.056)

def sel1():
    l13.place_forget()
    l14.place_forget()
    E3.place_forget()
    l15.place_forget()
    E4.place_forget()
    l16.place_forget()
    E5.place_forget()
    l17.place(relx=.1,rely=.2)
    l18.place(relx=.1,rely=.48)
    E6.place(relx=.5,rely=.48,relwidth=0.1,relheight=0.056)
    
    # line11=canvas5.create_line(70,98,88,98)
    # line12=canvas5.create_line(70,98,70,350)
    # line13=canvas5.create_line(70,350,698,350)
    # line14=canvas5.create_line(698,350,698,98)
    # line15=canvas5.create_line(698,98,140,98)

def sel2():
    l28.place_forget()
    l29.place_forget()
    E9.place_forget()
    l22.place(relx=.1,rely=.235)
    """line21=canvas6.create_line(70,115,88,115)
    line22=canvas6.create_line(70,115,70,350)
    line23=canvas6.create_line(70,350,698,350)
    line24=canvas6.create_line(698,350,698,115)
    line25=canvas6.create_line(698,115,140,115)"""
    
    l23.place(relx=.1,rely=.32)
    #textBox8.delete("1.0", "end")
    
    
    textBox8.place(relx=.52,rely=.285,relwidth=0.378,relheight=0.12)
    #add_placeholder_to(textBox8, 'Enter the token here....')
    
    l24.place(relx=.1,rely=.42)
    
    l26.place(relx=.1,rely=.6)
    E8.place(relx=.777,rely=.6,relwidth=0.122,relheight=0.056)
    l27.place(relx=.1,rely=.7)
    cal.place(relx=.7762,rely=.7)
    R5.place(relx=.7,rely=.42,relwidth=0.1,relheight=0.06)
    R6.place(relx=.8,rely=.42,relwidth=0.1,relheight=0.06)

def sel3():
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
    
    l28.place(relx=.1,rely=.235)
    
    """line26=canvas6.create_line(70,115,88,115)
    line27=canvas6.create_line(70,115,70,350)
    line28=canvas6.create_line(70,350,698,350)
    line29=canvas6.create_line(698,350,698,115)
    line30=canvas6.create_line(698,115,140,115)"""
    
    l29.place(relx=.1,rely=.5)
    E9.place(relx=.48,rely=.5,relwidth=0.42,relheight=0.056)
    #E9.delete(0, "end")
    #add_placeholder_to1(E9, 'Enter the link here....')
    
def sel4():
    #print(textBox8.get("1.0","end"))
    l25.place(relx=.1,rely=.5)
    E7.place(relx=.52,rely=.5,relwidth=0.378,relheight=0.056)
    #E7.delete(0, "end")
    #add_placeholder_to1(E7, 'Enter the Screen Name here....')
    
def sel5():
    l25.place_forget()
    E7.place_forget()

def close():
    main.destroy()
    
    
main = tk.Tk()
main.resizable(False, False)
screenWidth = main.winfo_screenwidth()
screenHeight = main.winfo_screenheight()

windowWidth = screenWidth//2
windowHeight = screenHeight//2

positionRight = int(screenWidth//2 - windowWidth//2)
positionDown = int(screenHeight//2 - windowHeight//2)

main.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
print("Width",windowWidth,"Height",windowHeight)
main.title("Smart Summarizer")

frame = tk.Frame(main)
frame.pack(fill = BOTH, expand = YES)
canvas = tk.Canvas(frame, highlightthickness = 0) 

l2 = Label(canvas, text="Welcome to Smart Summarizer...",font = ('times new roman',20,'bold','italic'))
l2.place(relx = .25)

l1 = Label(canvas, text="Enter the search keywords/terms: ",font = ('Verdana',12))
l1.place(relx=.1, rely = .1)

textBox1 = scrolledtext.ScrolledText(canvas,wrap=NONE)
textBox1.place(relx = .1, rely = .200, relheight =.6, relwidth = .80)

xscrollbar = Scrollbar(canvas, orient=HORIZONTAL,cursor="arrow")
xscrollbar.place(relx = .1, rely = .800, relwidth = .80)

textBox1.config(xscrollcommand=xscrollbar.set)
xscrollbar.config(command=textBox1.xview)
add_placeholder_to(textBox1, 'Enter the keywords to be searched (in every new line)....')
canvas1 = tk.Canvas(frame,highlightthickness = 0) 

#txt=""
textBox2 = scrolledtext.ScrolledText(canvas1,wrap=WORD)
textBox2.place(relx = .1, rely = .200, relheight =.6, relwidth = .80)
l3 = Label(canvas1, text="Summarized Text:",font = ('Verdana',12))
l3.place(relx=0.07,rely=0.1)
canvas2 = tk.Canvas(frame,highlightthickness = 0) 

nextButton = tk.Button(canvas, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction())
disable_b1()
nextButton.place(relx = .75, rely = .9, relwidth = .1)

clbt1 = tk.Button(canvas, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt1.place(relx = .875, rely = .9, relwidth = .1)

change_color(nextButton)
canvas.pack(fill=BOTH,expand=YES)

textBox2.config(state=DISABLED)
dwnButton = tk.Button(canvas1, text = 'Download summarized text',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: writeToFile(textBox1))
dwnButton.place(relx = .32, rely = .86, relwidth = .32)
change_color(dwnButton)


l4 = Label(canvas2, text="Extract data from:",font = ('Verdana',12))
l4.place(relx=.11,rely=.15)

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
c1 = Checkbutton(canvas2, text = "Text file",font = ('Arial',11), variable = CheckVar1,onvalue = 1, offvalue = 0,anchor = W)
c2 = Checkbutton(canvas2, text = "PDF Document",font = ('Arial',11), variable = CheckVar2,onvalue = 1, offvalue = 0,anchor = W)
c3 = Checkbutton(canvas2, text = "URL/Website",font = ('Arial',11), variable = CheckVar3,onvalue = 1, offvalue = 0,anchor = W)
c4 = Checkbutton(canvas2, text = "Social Media",font = ('Arial',11), variable = CheckVar4,onvalue = 1, offvalue = 0,anchor = W)
c1.place(relx=.15,rely=.23, relheight = .1, relwidth = .5)
c2.place(relx=.15,rely=.33, relheight = .1, relwidth = .5)
c3.place(relx=.15,rely=.43, relheight = .1, relwidth = .5)
c4.place(relx=.15,rely=.53, relheight = .1, relwidth = .5)

# line1=canvas2.create_line(80,77,90,77)
# line2=canvas2.create_line(80,77,80,350)
# line3=canvas2.create_line(80,350,688,350)
# line4=canvas2.create_line(688,350,688,77)
# line5=canvas2.create_line(688,77,240,77)

#print(CheckVar1.get())

backButton1 = tk.Button(canvas2, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction1())
backButton1.place(relx = .625, rely = .9, relwidth = .1)


nextButton2 = tk.Button(canvas2, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction2())
disable_b2()
nextButton2.place(relx = .75, rely = .9, relwidth = .1)

clbt2 = tk.Button(canvas2, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt2.place(relx = .875, rely = .9, relwidth = .1)

####### Text File ######

canvas3 = tk.Canvas(frame,highlightthickness = 0) 
l5 = Label(canvas3, text="Extraction from Text File",font = ('Verdana',12))
l5.place(relx=.25,rely=.05, relwidth = .5)

l6 = Label(canvas3, text="Text file location: ",font = ('Verdana',10))
l6.place(relx=.1,rely=.1,relheight = .1)

E1 = tk.Entry(canvas3)
#textBox3 = tk.Text(canvas3,wrap=NONE,fg="black")
#textBox3.place(relx=.12,rely=.195,relwidth=0.72,relheight=0.056)
E1.place(relx=.1,rely=.2,relwidth=0.65,relheight=0.06)
state1=add_placeholder_to1(E1, 'Browse File Directory....')

brbt = tk.Button(canvas3, text = 'Browse',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=10,command = lambda: fileDialog(state1))
brbt.place(relx=.8,rely=.2,relwidth=0.1,relheight=0.06)

l7 = Label(canvas3, text="Extracted Data: ",font = ('Verdana',10))

textBox4 = scrolledtext.ScrolledText(canvas3,wrap=WORD,fg="black")
extrtbt = tk.Button(canvas3, text = 'Preview',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=14,command = lambda: extract())

extrtbt.place(relx=.41,rely=.3)

backButton2 = tk.Button(canvas3, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction2())
backButton2.place(relx = .625, rely = .9, relwidth = .1)


nextButton3 = tk.Button(canvas3, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction3())
disable_b3()
nextButton3.place(relx = .75, rely = .9, relwidth = .1)

clbt3 = tk.Button(canvas3, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt3.place(relx = .875, rely = .9, relwidth = .1)


############ PDF File ############


canvas4 = tk.Canvas(frame,highlightthickness = 0) 
l8 = Label(canvas4, text="Extraction from PDF Document",font = ('Verdana',12))
l8.place(relx=.25,rely=.05,relwidth  = .5)

l9 = Label(canvas4, text="PDF file location: ",font = ('Verdana',10))
l9.place(relx=.1,rely=.1,relheight = .1)

E2 = tk.Entry(canvas4)
#textBox5 = tk.Text(canvas4,wrap=NONE,fg="black")
#textBox5.place(relx=.12,rely=.195,relwidth=0.72,relheight=0.056)
E2.place(relx=.1,rely=.2,relwidth=0.65,relheight=0.06)
state2=add_placeholder_to(E2, 'Browse File Directory....')

brbt1 = tk.Button(canvas4, text = 'Browse',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=10,command = lambda: fileDialog1(state2))
brbt1.place(relx=.8,rely=.2,relwidth=0.1,relheight=0.06)

l10 = Label(canvas4, text="Extracted Data: ",font = ('Verdana',10))

textBox6 = scrolledtext.ScrolledText(canvas4,wrap=WORD,fg="black")

extrtbt1 = tk.Button(canvas4, text = 'Preview',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",width=14,command = lambda: extract1())
extrtbt1.place(relx=.41,rely=.3)

backButton2 = tk.Button(canvas4, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction3())
backButton2.place(relx = .625, rely = .9, relwidth = .1)

nextButton4 = tk.Button(canvas4, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction4())
disable_b4()
nextButton4.place(relx = .75, rely = .9, relwidth = .1)

clbt4 = tk.Button(canvas4, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt4.place(relx = .875, rely = .9, relwidth = .1)


############## URL / Wikipedia ###########

canvas5 = tk.Canvas(frame,highlightthickness = 0) 

l11 = Label(canvas5, text="Extraction from URL/Website",font = ('Verdana',12))
l11.place(relx=.25,rely=.05,relwidth  = .5)

l12 = Label(canvas5, text="Select the desired option: ",font = ('Verdana',11))
l12.place(relx=.1,rely=.12)

l13 = Label(canvas5, text="For URL",font = ('Verdana',11))

l14 = Label(canvas5, text="Enter the URL: ",font = ('Verdana',10))

#textBox7 = tk.Text(canvas5,wrap=NONE,fg="black")
#textBox7.place(relx=.19,rely=.285,relwidth=0.6,relheight=0.056)
E3 = tk.Entry(canvas5)
add_placeholder_to1(E3, 'Enter the URL here.....')
#depthbox = Spinbox(canvas5, from_=0,justify=CENTER)
#depthbox.place(relx=.5,rely=.35,relwidth=0.1,relheight=0.056)
l15 = Label(canvas5, text="Depth: ",font = ('Verdana',10))

E4 = tk.Entry(canvas5,justify=CENTER)

l16 = Label(canvas5, text="Number of words to generate: ",font = ('Verdana',10))

E5 = tk.Entry(canvas5,justify=CENTER)

l17 = Label(canvas5, text="For Wikipedia",font = ('Verdana',11))

l18 = Label(canvas5, text="Number of words to generate: ",font = ('Verdana',10))

E6 = tk.Entry(canvas5,justify=CENTER)

var = IntVar()
R1 = Radiobutton(canvas5, text="URL", variable=var, value=1,command=sel,font=('Verdana',11))
R1.place(relx=.45,rely=.12,relwidth=0.07,relheight=0.06)

R2 = Radiobutton(canvas5, text="Wikipedia", variable=var, value=2,command=sel1,font=('Verdana',11))
R2.place(relx=.68,rely=.12,relwidth=0.14,relheight=0.06)

backButton3 = tk.Button(canvas5, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction4())
backButton3.place(relx = .625, rely = .9, relwidth = .1)

nextButton5 = tk.Button(canvas5, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction5())
disable_b5()
nextButton5.place(relx = .75, rely = .9, relwidth = .1)

clbt5 = tk.Button(canvas5, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt5.place(relx = .875, rely = .9, relwidth = .1)


############# social media ################

canvas6 = tk.Canvas(frame,highlightthickness = 0) 
l19 = Label(canvas6, text="Extraction from Social Media",font = ('Verdana',12))
l19.place(relx=.34,rely=.05)

l20 = Label(canvas6, text="Select the desired option: ",font = ('Verdana',11))
l20.place(relx=.1,rely=.11)

"""line16=canvas6.create_line(70,60,88,60)
line17=canvas6.create_line(70,60,70,100)
line18=canvas6.create_line(70,100,698,100)
line19=canvas6.create_line(698,100,698,60)
line20=canvas6.create_line(698,60,140,60)"""

l21 = Label(canvas6, text="Extract data from: ",font = ('Verdana',10))
l21.place(relx=.1,rely=.16)

l22 = Label(canvas6, text="For Facebook posts and Twitter tweets",font = ('Verdana',11))

l23 = Label(canvas6, text="Access Token for Facebook Graph API Explorer: ",font = ('Verdana',10))

textBox8 = scrolledtext.ScrolledText(canvas6,wrap=WORD,fg="black")
add_placeholder_to2(textBox8, 'Enter the token here....')
#E7 = tk.Entry(canvas6)
#E7.place(relx=.52,rely=.32,relwidth=0.378,relheight=0.056)
#E7.place(relx=.1,rely=.37,relwidth=0.8,relheight=0.056)
l24 = Label(canvas6, text="Do you want to extract tweets of a specific user/company handle?",font = ('Verdana',10))


l25 = Label(canvas6, text="Screen Name of the Twitter handle: ",font = ('Verdana',10))


E7 = tk.Entry(canvas6,justify=CENTER)
add_placeholder_to1(E7, 'Enter the Screen Name here....')

l26 = Label(canvas6, text="Number of facebook posts and tweets required for the data extraction: ",font = ('Verdana',10))


E8 = tk.Entry(canvas6,justify=CENTER)


l27 = Label(canvas6, text="Date from when the tweets and facebook posts were made: ",font = ('Verdana',10))


cal = DateEntry(canvas6, width=12, background='darkblue',date_pattern='yyyy-MM-dd',foreground='white', borderwidth=2)

var2 = IntVar()
R5 = Radiobutton(canvas6, text="Yes", variable=var2, value=1,command=sel4,font=('Verdana',10))

R6 = Radiobutton(canvas6, text="No", variable=var2, value=2,command=sel5,font=('Verdana',10))

l28 = Label(canvas6, text="For RSS Feeds",font = ('Verdana',11))

l29 = Label(canvas6, text="Link for the xml format of RSS Feeds: ",font = ('Verdana',10))


E9 = tk.Entry(canvas6)
add_placeholder_to1(E9, 'Enter the link here....')
var1 = IntVar()
R3 = Radiobutton(canvas6, text="Facebook posts and Twitter tweets", variable=var1, value=1,command=sel2,font=('Verdana',10))
R3.place(relx=.35,rely=.16,relwidth=0.4,relheight=0.06)

R4 = Radiobutton(canvas6, text="RSS Feeds", variable=var1, value=2,command=sel3,font=('Verdana',10))
R4.place(relx=.73,rely=.16,relwidth=0.14,relheight=0.06)

backButton4 = tk.Button(canvas6, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction5())
backButton4.place(relx = .625, rely = .9, relwidth = .1)

nextButton6 = tk.Button(canvas6, text = 'Next',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: nextFunction6())
disable_b6()
nextButton6.place(relx = .75, rely = .9, relwidth = .1)

clbt6 = tk.Button(canvas6, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt6.place(relx = .875, rely = .9, relwidth = .1)


################### Result ###################

canvas7 = tk.Canvas(frame,highlightthickness = 0) 
l30 = Label(canvas7, text="Summary",font = ('Verdana',12))
l30.place(relx=.25,rely=.05,relwidth  = .5)

l31 = Label(canvas7, text="Portion still pending",font = ('Verdana',10))
l31.place(relx=.1,rely=.1,relheight = .1)

backButton5 = tk.Button(canvas7, text = 'Back',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: prevFunction6())
backButton5.place(relx = .75, rely = .9, relwidth = .1)

clbt6 = tk.Button(canvas7, text = 'Close',activeforeground='white',activebackground='black', font = ('Verdana',9),cursor="hand2",command = lambda: close())
clbt6.place(relx = .875, rely = .9, relwidth = .1)


main.mainloop()