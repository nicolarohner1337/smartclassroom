import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_all_pages(url, df=pd.DataFrame()):
    '''return database items'''
    response_ = requests.get(url)
    response_ = response_.json()

   #append list of dicts to dataframe
    dfNew = pd.DataFrame(response_['items'])
    df = df.append(dfNew,ignore_index=True)

    if not response_['hasMore']:
        return df
    else:
        for elem in response_['links']:
            for k, v in elem.items():
                if v == 'next':
                    new_url = elem['href']
        return get_all_pages(new_url, df)

def to_data_frame(url_result):
    output = pd.DataFrame()
    for lists in url_result:
        for dicti in lists:
            output = output.append(dicti, ignore_index=True)
    return output

def overview(df, col):
    f, axs = plt.subplots(1,2, figsize=(9,6), gridspec_kw=dict(width_ratios=[15,10]))
    sns.boxplot(df[col], ax=axs[0])
    sns.distplot(df[col], ax=axs[1])
    return plt.show()
