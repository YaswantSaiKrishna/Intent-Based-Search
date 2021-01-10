import csv
import fasttext

def classifier(dataframe, classs, rootdir):
    labels  = { '__label__1'  : 'Criminal Procedure',
                '__label__2'  : 'Civil Rights',
                '__label__3'  : 'First Amendment',
                '__label__4'  : 'Due Process',
                '__label__5'  : 'Privacy',
                '__label__6'  : 'Attorneys',
                '__label__7'  : 'Unions',
                '__label__8'  : 'Economic Activity',
                '__label__9'  : 'Judicial Power',
                '__label__10' : 'Federalism',
                '__label__11' : 'Interstate Relations',
                '__label__12' : 'Federal Taxation',
                '__label__13' : 'Miscellaneous',
                '__label__14' : 'Private Action',
                '__label__15' : 'Others'}
    model = fasttext.load_model("/home/yaswant/Documents/EY_Hackathon/FastTextModels/fasttext_supreme.bin")
    field_names = ['FileName', 'FilePath', 'Intent']
    r = []
    for ind in dataframe.index:
        prediction = model.predict(dataframe['Text'][ind])[0][0]
        if classs == 'All':
            d = {'FileName' : dataframe['FileName'][ind], 'FilePath' : dataframe['FilePath'][ind],
                 'Intent' : labels[prediction]}
            r.append(d)
        else:
            if labels[prediction] == classs:
                d = {'FileName' : dataframe['FileName'][ind], 'FilePath' : dataframe['FilePath'][ind],
                     'Intent' : classs}
                r.append(d)
            else:
                pass
    with open(rootdir + 'result.csv', 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = field_names) 
        writer.writeheader() 
        writer.writerows(r)

    return rootdir + 'result.csv'        