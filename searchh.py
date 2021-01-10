import csv
import pandas as pd
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Search
def search(rootdir, Query, index_name, endpoint, key, fnames, vertical):
    field_names = ['FileName', 'FilePath', 'Score']
    # Create a client
    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                          index_name=index_name,
                          credential=credential)
    results = client.search(search_text=Query)
    df = pd.read_csv('/home/yaswant/Documents/EY_Hackathon/IntentBased/FilesTracker/{}.csv'.format(vertical))
    r = []

    for result in results:
        if result['FileName'] in fnames:
            d = {'FileName' : result['FileName'], 'FilePath' : result['FilePath'], 'Score' : result['@search.score']}
            r.append(d)
            if df.loc[df['FileName'] == str(result['FileName']), 'Intent'].isnull().any():
                df.loc[df['FileName'] == str(result['FileName']), 'Intent'] = str(Query)
            else:
                df.loc[df['FileName'] == str(result['FileName']), 'Intent'] = df.loc[df['FileName'] == str(result['FileName']), 'Intent'] + "," + str(Query)
    df.to_csv('/home/yaswant/Documents/EY_Hackathon/IntentBased/FilesTracker/{}.csv'.format(vertical), index = False) 
    with open(rootdir + 'result.csv', 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = field_names) 
        writer.writeheader() 
        writer.writerows(r)

    return rootdir + 'result.csv'
