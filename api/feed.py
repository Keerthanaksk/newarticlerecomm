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

    # remove white space
    df['topic'] = df['topic'].str.strip()

    # convert cliked to boolean
    df['clicked'].loc[df['clicked'] == 'Yes'] = True
    df['clicked'].loc[df['clicked'] == 'No'] = False

    # convert liked to boolean
    df['liked'] = df['liked'].astype(bool)

    # add clicks and loves cols
    df['clicks'] = 0
    df['loves'] = 0

    print(df.columns)

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