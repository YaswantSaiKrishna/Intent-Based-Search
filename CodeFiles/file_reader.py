import os
import string
import textract
import pandas as pd

def Read_Files(rootdir, learning = 'active', vertical = None):
    paths = []          # File path.
    fname = []          # File name.
    cl_text = []        # Cleaned Text.
    user_fnames = []    # User File Names.
    index_fnames = []   # File Names to be indexed.
    for subdir, dirs, files in os.walk(rootdir): # Walking through folders & subfolders in the root directory.
        for filee in files:
            try:
                if learning=='active' and vertical != None: # Active
                    df = pd.read_csv('TrackerFiles/{}.csv'.format(vertical))
                    user_fnames.append(str(filee))
                    if df['FileName'].where(df['FileName'] == str(filee)).any():
                        pass
                    else:
                        index_fnames.append(str(filee))
                        df = df.append({'FileName' : str(filee), 'FilePath' : str(os.path.join(subdir, filee))}, ignore_index=True)
                        text = textract.process(os.path.join(subdir, filee)).decode("utf-8") ## Extract the text from the files and decode the byte string to text.
                        paths.append(os.path.join(subdir, filee)) # Append the path of the file to path variable.
                        fname.append(str(filee)) # Append the filename to the filename variable.
                        text = str(text).strip(' ')
                        cleaned_text = ''.join([char for char in text if char not in string.punctuation and char != '\n'])
                        cl_text.append(cleaned_text)
                    df.to_csv('TrackerFiles/{}.csv'.format(vertical), index = False)
                else: # Passive
                    text = textract.process(os.path.join(subdir, filee)).decode("utf-8") ## Extract the text from the files and decode the byte string to text.
                    paths.append(os.path.join(subdir, filee)) # Append the path of the file to path variable.
                    fname.append(str(filee)) # Append the filename to the filename variable.
                    text = str(text).strip(' ')
                    cleaned_text = ''.join([char for char in text if char not in string.punctuation and char != '\n'])
                    cl_text.append(cleaned_text)
            except: 
                print(" The file : {} is not extracted due to unicode errors".format(os.path.join(subdir, filee)))
    return {"FileName" : fname, "FilePath" : paths, "Text" : cl_text}, user_fnames
