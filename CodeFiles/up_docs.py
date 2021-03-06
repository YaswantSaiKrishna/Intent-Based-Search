import string
import pandas as pd
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Upload Documents to Index
def upload_docs(Data_Frame, index_name, endpoint, key):
    dataframe2 = list(Data_Frame.to_dict('records'))
    # Create a client
    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                          index_name=index_name,
                          credential=credential)
    df = pd.read_csv('TrackerFiles/{}.csv'.format(index_name))
    i = df.shape[0] + 1
    for e in dataframe2:
        DOCUMENT = {
                    'Id' : str(i),
                    'FileName': e['FileName'],
                    'FilePath': e['FilePath'],
                    'KeyPhrases': e['KeyPhrases'],
                    'People' : e['people'],
                    'Organisation' : e['org'],
                    'Location' : e['loc'],
                    }
        i+=1
        result = client.upload_documents(documents=[DOCUMENT]) # documents = [document1,...,documentN]
