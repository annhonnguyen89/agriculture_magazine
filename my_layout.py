# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 23:15:30 2018

@author: Thinkpad
"""

import tkinter
from time import sleep
 
textFont1 = ("Arial", 10, "bold italic")
textFont2 = ("Arial", 16, "bold")
textFont3 = ("Arial", 8, "bold")
 
class LabelWidget(tkinter.Entry):
    def __init__(self, master, x, y, text, col):
        self.text = tkinter.StringVar()
        self.text.set(text)
        tkinter.Entry.__init__(self, master=master)
        self.config(relief="ridge", font=textFont1,
                    bg=col, fg="#000000fff", 
                    readonlybackground="#ffffff000",
                    justify='center',width=8,
                    textvariable=self.text,
                    state="readonly")
        self.grid(column=x, row=y)

class MessageWidget(tkinter.Message):
    def __init__(self, master, x, y, text, col):
        self.text = tkinter.StringVar()
        self.text.set(text)
        tkinter.Message.__init__(self, master = master)
        self.config(font=textFont1,
                    bg=col, fg="#000000fff", 
                    justify='center',width=50,
                    textvariable=self.text)
        self.grid(column = x, row = y)
 
class EntryWidget(tkinter.Entry):
    def __init__(self, master, x, y):
        tkinter.Entry.__init__(self, master=master)
        self.value = tkinter.StringVar()
        self.config(textvariable=self.value, width=8,
                    relief="ridge", font=textFont1,
                    bg="#ddddddddd", fg="#000000000",
                    justify='center')
        self.grid(column=x, row=y)
        self.value.set("")
 
class EntryGrid(tkinter.Tk):
    ''' Dialog box with Entry widgets arranged in columns and rows.'''
    def __init__(self, colList, rowList, df_data, title="Entry Grid"):
        self.cols = colList[:]
        self.colList = colList[:]
        self.colList.insert(0, "")
        self.rowList = rowList
        self.dataDf = df_data
        tkinter.Tk.__init__(self)
        self.title(title)
 
        self.mainFrame = tkinter.Frame(self)
        self.mainFrame.config(padx='3.0m', pady='3.0m')
        self.mainFrame.grid()
        self.make_header()
        #self.display_data()
        self.display_data_message()
        self.mainloop()
        
    def display_data_message(self, color = "#ffffff000"):
        self.hdrDict = {}
        for i, cont in enumerate(self.dataDf["title"]):
            def handler(event, col = 1, row=i+1, text = cont):
                return self.__headerhandler(col, row, text)            
            w = MessageWidget(self.mainFrame, 1, i+1, cont, color)
            self.hdrDict[(1, i+1)] = w
        
        for i, cont in enumerate(self.dataDf["summary"]):
            def handler(event, col = 2, row=i+1, text = cont):
                return self.__headerhandler(col, row, text)            
            w = MessageWidget(self.mainFrame, 2, i+1, cont, color)
            self.hdrDict[(2, i+1)] = w
            
        for i, cont in enumerate(self.dataDf["summary"]):
            def handler(event, col = 3, row=i+1, text = cont):
                return self.__headerhandler(col, row, text)
            w = MessageWidget(self.mainFrame, 3, i+1, cont, color)
            self.hdrDict[(3, i+1)] = w
        
        return(0)
        
    def make_header(self, col = "#ffffff000"):
        self.hdrDict = {}
        for i, label in enumerate(self.colList):
            def handler(event, col=i, row=0, text=label):
                return self.__headerhandler(col, row, text)
            w = LabelWidget(self.mainFrame, i, 0, label, col)
            self.hdrDict[(i,0)] = w
            w.bind(sequence="<KeyRelease>", func=handler)
 
        for i, label in enumerate(self.rowList):
            def handler(event, col=0, row=i+1, text=label):
                return self.__headerhandler(col, row, text)
            w = LabelWidget(self.mainFrame, 0, i+1, label, col)
            self.hdrDict[(0,i+1)] = w
            w.bind(sequence="<KeyRelease>", func=handler)
 
    def __entryhandler(self, col, row):
        s = self.gridDict[(col,row)].get()
        if s.upper().strip() == "EXIT":
            self.destroy()
        elif s.upper().strip() == "DEMO":
            self.demo()
        elif s.strip():
            print (s)
 
    def demo(self):
        ''' enter a number into each Entry field '''
        for i in range(len(self.cols)):
            for j in range(len(self.rowList)):
                sleep(0.25)
                self.set(i,j,"")
                self.update_idletasks()
                sleep(0.1)
                self.set(i,j,i+1+j)
                self.update_idletasks()
    
    def __headerhandler(self, col, row, text):
        ''' has no effect when Entry state=readonly '''
        self.hdrDict[(col,row)].text.set(text)
 
    def get(self, x, y):
        return self.gridDict[(x,y)].get()
 
    def set(self, x, y, v):
        self.gridDict[(x,y)].set(v)
        return v
'''
if __name__ == "__main__":
    cols = ['Title', 'Summary', 'Link']
    rows = ['1', '2', '3']
    title_list = ["t1", "t2", "t3"]
    summary_list = ["s1", "s2", "s3"]
    link_list = ["l1", "l2", "l3"]
    
    df_data = {'title': title_list, 'summary': summary_list, 'link': link_list}
    app = EntryGrid(cols, rows, df_data)
    app.demo()
'''


    