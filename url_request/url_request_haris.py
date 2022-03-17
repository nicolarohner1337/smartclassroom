import requests
import pandas as pd

url = 'https://glusfqycvwrucp9-db202202211424.adb.eu-zurich-1.oraclecloudapps.com/ords/sensor_datalake1/sens/insert/'

response_ = requests.get(url)
response_ = response_.json()
print(response_.keys())

def get_all_pages(url, liste=[]):
    '''return database items'''
    response_ = requests.get(url)
    response_ = response_.json()
    if response_['hasMore'] != True:
        #liste.append(response_['items'])
        return liste
    else:
        liste.append(response_['items'])
        for elem in response_['links']:
            for k, v in elem.items():
                if v == 'next':
                    new_url = elem['href']
        return get_all_pages(new_url, liste)
result = get_all_pages(url)
print(result)

