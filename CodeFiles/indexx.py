# Azure Search Imports.
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (ComplexField, 
                                                   CorsOptions, 
                                                   SearchIndex, 
                                                   ScoringProfile, 
                                                   SearchFieldDataType, 
                                                   SimpleField, 
                                                   SearchableField)

def create_index(name, endpoint, key):
    # Create a service client
    client = SearchIndexClient(endpoint, AzureKeyCredential(key))

    fields = [SimpleField(name='Id', type=SearchFieldDataType.String, key=True),
              SearchableField(name='FileName', type=SearchFieldDataType.String),
              SimpleField(name='FilePath', type=SearchFieldDataType.String),
              SearchableField(name='KeyPhrases', collection=True, type=SearchFieldDataType.String, analyzer_name="en.lucene"),
              SearchableField(name='People', collection=True, type=SearchFieldDataType.String),
              SearchableField(name='Organisation', collection=True, type=SearchFieldDataType.String),
              SearchableField(name='Location', collection=True, type=SearchFieldDataType.String)]
    
    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles = []

    index = SearchIndex(name=name,
                        fields=fields,
                        scoring_profiles=scoring_profiles,
                        cors_options=cors_options)

    result = client.create_index(index)
