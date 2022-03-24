import requests
import pandas as pd

def get_all_pages(url, liste=[]):
    '''return database items'''
    response_ = requests.get(url)
    response_ = response_.json()
    liste.append(response_['items'])
    if response_['hasMore'] != True:
        return liste
    else:
        liste.append(response_['items'])
        for elem in response_['links']:
            for k, v in elem.items():
                if v == 'next':
                    new_url = elem['href']
        return get_all_pages(new_url, liste)

def to_data_frame(url_result):
    output = pd.DataFrame()
    for lists in url_result:
        for dicti in lists:
            output = output.append(dicti, ignore_index=True)
    return output
