import os
from pprint import pprint
import sys
import pandas as pd
import datetime as dt
from pymongo import MongoClient
from api.core.security import get_password_hash

def db_reset(url):
    '''
        Repopulate articles and users in local db

        Command:
            py setup_utils.py db-reset mongodb://localurl:here
    '''
    
    def transform_data(path):
        '''
            Clean, modify, add columns in recos data
        '''

        df = pd.read_excel(path)    
        
        # drop cols
        df.drop(["clicked"], axis=1, inplace=True)
        df.drop(["liked"], axis=1, inplace=True)
        df.drop(["comments"], axis=1, inplace=True)

        # remove white space
        df['topic'] = df['topic'].str.strip()
        df['link'] = df['link'].str.strip()
        df['summary'] = df['summary'].str.strip()

        # drop duplicates
        dups = df.duplicated(subset=['link'])
        for k,v in dups.items():
            if v:
                df.drop(k, inplace=True)
        
        df['total_loves'] = 0
        df['total_clicks'] = 0

        return df



    def recos_data(df):
        # add date
        df['date_recommended'] = dt.datetime.now(dt.timezone.utc)

        # loved col
        df['loved'] = False
        
        # clicks col
        df['clicks'] = 0

        df.drop(["topic"], axis=1, inplace=True)
        df.drop(["title"], axis=1, inplace=True)
        df.drop(["summary"], axis=1, inplace=True)
        df.drop(["total_loves"], axis=1, inplace=True)
        df.drop(["total_clicks"], axis=1, inplace=True)

        data = df.to_dict(orient='records')

        return data
    
    
    
    def user_data(email, recos):
        
        pw = get_password_hash('test')

        data = {
            'email': email,
            'password': pw,
            'recommendations': recos
        }
        
        return data



    def insert_articles(data):
        data = data.to_dict(orient='records')
        collection = db.articles
        result = collection.insert_many(data)



    def insert_users(data):
        collection = db.users
        
        users = ['home@lander.com', 'omni@man.com', 'not@shy.com', 'kwang@ya.com']
        
        for u in users:
            recos = recos_data(data.sample(n=15))
            
            if u == 'kwang@ya.com':
                # no interaction
                collection.insert_one(user_data(u, []))
            else:
                recos = recos_data(data.sample(n=15))
                collection.insert_one(user_data(u, recos))


    print('Resetting db...')

    client = MongoClient(url)
    client.drop_database('unionbank')
    
    db = client['unionbank']
    
    data = transform_data('all_recommendations.xlsx')
    
    insert_articles(data)
    insert_users(data)

    print('DB reset done!')



def export_requirements():
    '''
        Generate requirements.txt file
        
        Command:
            py setup_utils.py export-requirements
    '''
    print("Exporting requirements.txt...")
    os.system("poetry export -f requirements.txt --output requirements.txt --without-hashes")
    print("Export done!")



command = sys.argv[1]

if command == 'db-reset':
    db_reset(sys.argv[2])
elif command == 'export-requirements':
    export_requirements()
