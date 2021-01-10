import spacy
import en_core_web_sm

# NER
def NER(Data_Frame):
    people = []
    organizations = []
    locations = []
    nlp = en_core_web_sm.load()
    for ind in Data_Frame.index:
        l = []
        o = []
        p = []
        doc = nlp(Data_Frame['Text'][ind])
        for X in doc.ents:
            if X.label_ == 'NORP' or X.label_ == 'GPE':
                l.append(X.text)
            elif X.label_ == 'ORG':
                o.append(X.text)
            elif X.label_ == 'PERSON':
                p.append(X.text)
            else:
                pass
        people.append(p)
        organizations.append(o)
        locations.append(l)
    Data_Frame['people'] = people
    Data_Frame['org'] = organizations
    Data_Frame['loc'] = locations

    return Data_Frame