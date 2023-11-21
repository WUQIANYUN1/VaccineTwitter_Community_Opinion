import requests
import pandas as pd
import time
import json
from time import sleep
import random
import numpy as np
import datetime
from datetime import datetime, timedelta
import jieba
import re
import collections

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

bearer_token=''
search_url = "https://api.twitter.com/2/tweets/search/all"

start_time='2020-01-01T00:00:00Z'
end_time='2022-06-01T00:00:00Z'
        
verified={True:1,False:0}

query_params = {'query': 'ワクチン lang:ja','max_results':500,
                'start_time':start_time,'end_time':end_time,
                'tweet.fields': 'author_id,created_at,public_metrics,entities',
                'expansions':'author_id','user.fields':'id,created_at,description,name,username,location,verified,referenced_tweets'} #context_annotations
json_response = connect_to_endpoint(search_url, query_params)
next_token=json_response['meta']['next_token']
while len(next_token)>0:
    sleep(5)
    try:
        query_params = {'query': 'ワクチン lang:ja','max_results':500,
                'next_token':next_token,
                'start_time':start_time,'end_time':end_time,
                'tweet.fields': 'author_id,created_at,public_metrics,entities',
                'expansions':'author_id','user.fields':'id,created_at,description,name,username,location,verified'}

        json_response = connect_to_endpoint(search_url, query_params)
        N=update_SQL(json_response,N)
        next_token=json_response['meta']['next_token']
    except:
        next_token=""
        break


