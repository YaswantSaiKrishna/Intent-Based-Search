import tkinter as tk 
from tkinter import ttk 
from tkinter import Button
import pandas as pd
from file_reader import Read_Files
from ner import NER
from textrank import TextRank4Keyword
from indexx import create_index
from up_docs import upload_docs
from searchh import search
from classifier_ft import classifier

class view:
    def __init__(self, window):
        self.window = window 
        self.window.title('EY GDS DEMO') 
        self.window.geometry('500x250')

        ttk.Label(self.window, 
                  text = "Team Raga", 
                  foreground ="black", 
                  font = ("Times New Roman", 15)).grid(row = 0, column = 1)

        ttk.Label(self.window, 
                  text = "Select the Vertical", 
                  font = ("Times New Roman", 10)).grid(column = 0, row = 5, padx = 5, pady = 10) 
                                                          
        # Combobox creation 
        n = tk.StringVar() 
        self.vertical = ttk.Combobox(self.window, width = 16, textvariable = n) 
                                                                                    
        # Adding combobox drop down list 
        self.vertical['values'] = ('Finance',   
                                   'Delivery', 
                                   'Default') 
                                                                                                                                                                                                              
        self.vertical.grid(column = 1, row = 5) 
        self.vertical.current()

        # declaring string variable for storing folderpath
        self.name_var=tk.StringVar() 

        # creating a label for folder_path using widget Label 
        self.name_label = ttk.Label(self.window, 
                                    text = 'Folder Path', 
                                    font=('Times New Roman', 10, 'normal'))

        # creating a entry for input name using widget Entry 
        self.name_entry = ttk.Entry(self.window, 
                                    textvariable = self.name_var,
                                    font=('Times New Roman',10,'normal')) 

        # placing the label and entry in the required position using grid method 
        self.name_label.grid(row=6,column=0,padx = 5, pady = 10) 
        self.name_entry.grid(row=6,column=1,padx = 5, pady = 10)

        # label1 
        ttk.Label(self.window, 
                  text = "Available Keywords", 
                  font = ("Times New Roman", 10)).grid(column = 0, row = 7, padx = 5, pady = 10)

        # Combobox creation 
        m = tk.StringVar() 
        self.classes = ttk.Combobox(self.window, 
                                    width = 16, 
                                    textvariable = m)

        # Adding combobox drop down list 
        self.classes['values'] = ('None',
                                  'Criminal Procedure',
                                  'Civil Rights',
                                  'First Amendment',
                                  'Due Process',
                                  'Privacy',
                                  'Attorneys',
                                  'Unions',
                                  'Economic Activity',
                                  'Judicial Power',
                                  'Federalism',
                                  'Interstate Relations',
                                  'Federal Taxation',
                                  'Miscellaneous',
                                  'Private Action',
                                  'All')
        self.classes.grid(column = 1, row = 7) 
        self.classes.current()

        self.name_var1=tk.StringVar()
        # creating a label for name using widget Label 
        self.name_label1 = ttk.Label(self.window, 
                                    text = 'Custom Keyword', 
                                    font=('Times New Roman', 10, 'normal'))

        # creating a entry for input name using widget Entry 
        self.name_entry1 = ttk.Entry(self.window, 
                                    textvariable = self.name_var1,
                                    font=('Times New Roman',10,'normal')) 

        # placing the label and entry in the required position using grid method 
        self.name_label1.grid(row=8,column=0,padx = 5, pady = 10) 
        self.name_entry1.grid(row=8,column=1,padx = 5, pady = 10)

        # Create a Button 
        self.btn = Button(self.window, text = 'search', 
                          bd = '2', command = self.dispmsg)  
        self.btn.grid(row=9, column=1, padx = 5, pady = 10)
        
    def dispmsg(self):
        name_label2 = ttk.Label(self.window, 
                                text = "File with the queried intents is downloaded at " + str(self.name_var.get()), 
                                font=('Times New Roman', 10, 'normal'))
        name_label2.grid(row=10,column=1,padx = 5, pady = 10)

        if str(self.name_var1.get()) != '':
            learning = 'active'
            Data,UserFnames =  Read_Files(str(self.name_var.get()), learning=learning, vertical= str(self.vertical.get()).lower())
            Data_Frame = pd.DataFrame(Data, columns = ['FileName', 'FilePath', 'Text'])
            Data_Frame = NER(Data_Frame)
            kf = []
            for ind in Data_Frame.index:
                text = Data_Frame['Text'][ind]
                tr4w = TextRank4Keyword()
                tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
                kf.append(tr4w.get_keywords(100))
            Data_Frame['KeyPhrases'] = kf
            name = str(self.vertical.get()).lower()
            endpoint = "https://<EndPoint>.search.windows.net"
            key = "<Cognitive search key>"
            if name == 'default':
                create_index(name, endpoint, key)
            upload_docs(Data_Frame=Data_Frame, index_name= name, endpoint=endpoint, key=key)
            result = search(rootdir=str(self.name_var.get()), 
                            Query=str(self.name_var1.get()), index_name=name, 
                            endpoint=endpoint, key= key, fnames = UserFnames, 
                            vertical=str(self.vertical.get()).lower())
            if name == 'default':
                from azure.search.documents.indexes import SearchIndexClient
                from azure.core.credentials import AzureKeyCredential
                client = SearchIndexClient(endpoint, AzureKeyCredential(key))
                client.delete_index(name)
        elif str(self.name_var1.get()) == '' and str(self.classes.get()) != 'None':
            learning = 'passive'
            Data,UserFnames =  Read_Files(str(self.name_var.get()), learning=learning, vertical= None)
            Data_Frame  =  pd.DataFrame(Data, columns = ['FileName', 'FilePath', 'Text'])
            result = classifier(dataframe=Data_Frame, classs=str(self.classes.get()), rootdir=str(self.name_var.get()))
        else:
            pass


# Creating tkinter window 
window = tk.Tk()
a = view(window) 
window.mainloop()    
