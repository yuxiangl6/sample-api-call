#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Sample Crowdtangle API call using requests, BUT yet to resolve exceeding rate limit error

import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta
import time
import os
from os import path

#Parameters setup
baseurl = 'https://api.crowdtangle.com/posts'
parameters = {
    'token': 'your-token',
    'count': '100',
    'sortBy': 'date',
    'timeframe': '24 HOUR'
}

#Using GET via requests to extract data
r = requests.get(baseurl,params=parameters)
r_url=r.url


# In[ ]:


while r_url is not None:
    
    time.sleep(5)
    r_json_data = requests.get(r_url).json()
    
    if r_json_data['status']==200:
        if 'nextPage' in (r_json_data['result']['pagination']).keys():
            r_url = r_json_data['result']['pagination']['nextPage']
        else:
            r_url = None
    else:
        print(r_json_data)
        time.sleep(10)
        continue
        
    posts = r_json_data['result']['posts']
    
    #Flatten (unnest) the posts data using json_normalize
    flat_json=pd.json_normalize(posts,sep='_')
    df=pd.DataFrame(flat_json, columns=['platformId','platform','date','account_id','account_handle','link'
                                       ,'message','postUrl','score','updated'])

