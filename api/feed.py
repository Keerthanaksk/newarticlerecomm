import pandas as pd
from pymongo import MongoClient

# from pprint import pprint
def transform_data(path):
    '''
        Clean, modify, add columns in recos data
    '''

    df = pd.read_excel(path)

    # rename cols
    df = df.rename(columns={'Clicked (Yes/No)':'clicked','Liked (Yes/No)':'liked', 'Comments':'comments'})

    # drop null
    df.drop(["comments"], axis=1, inplace=True)

    # convert cliked to 1 or 0
    df['clicked'].loc[df['clicked'] == 'Yes'] = 1
    df['clicked'].loc[df['clicked'] == 'No'] = 0

    # add clicks and loves cols
    df['clicks'] = 0
    df['loves'] = 0

    # convert to key-val records
    data = df.to_dict(orient='records')
    
    return data

data = transform_data('recommendations.xlsx')

# obtain article collection
client = MongoClient('localhost', 27017)
db = client.unionbank
articles = db.articles

# insert articles
result = articles.insert_many(data)