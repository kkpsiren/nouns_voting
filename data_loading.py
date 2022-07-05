import requests
import json
import time
import os
import pandas as pd 
import streamlit as st

test=False
if test:
    from dotenv import load_dotenv
    load_dotenv()

class Flipsider:
    def __init__(self, API_KEY, TTL_MINUTES=120):
        self.API_KEY = API_KEY
        self.TTL_MINUTES = TTL_MINUTES

    def create_query(self, SQL_QUERY):
        r = requests.post(
            'https://node-api.flipsidecrypto.com/queries', 
            data=json.dumps({
                "sql": SQL_QUERY,
                "ttlMinutes": self.TTL_MINUTES
            }),
            headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": self.API_KEY},
        )
        if r.status_code != 200:
            raise Exception("Error creating query, got response: " + r.text + "with status code: " + str(r.status_code))

        return json.loads(r.text)    


    def get_query_results(self, token):
        r = requests.get(
            'https://node-api.flipsidecrypto.com/queries/' + token, 
            headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": self.API_KEY}
        )
        if r.status_code != 200:
            raise Exception("Error getting query results, got response: " + r.text + "with status code: " + str(r.status_code))
        
        data = json.loads(r.text)
        if data['status'] == 'running':
            time.sleep(10)
            return self.get_query_results(token)

        return data

    def run(self, SQL_QUERY):
        query = self.create_query(SQL_QUERY)
        token = query.get('token')
        data = self.get_query_results(token)
        df = pd.DataFrame(data['results'],columns = data['columnLabels'])
        return df

@st.cache(allow_output_mutation=True)
def load_queries(QUERY):
    bot = Flipsider(os.getenv('API_KEY'))
    df = bot.run(QUERY)
    return df
