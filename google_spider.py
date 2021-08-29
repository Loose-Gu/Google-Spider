import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib3
import time


urllib3.disable_warnings() 
years= range(2009,2021) # the year you want to search
requests.adapters.DEFAULT_RETRIES = 5

def search(year,ename,cname):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}
    # tbm is the param that control the theme of the search
    r= requests.get("https://www.google.com/search",params={'tbm':'nws',\
            'q':ename+" OR "+cname+" after:"+str(year)+"-01-01"+" before:"+str(year)+"-12-31"},\
                headers=headers,verify=False)
    return r

def loc_num(r):
    soup=BeautifulSoup(r.text,'html.parser')
    text=soup.find(id="result-stats")
    if text:
        text=text.get_text()
        text = text.replace(',','')
        result_stats = re.search('[1-9]\d*',text).group()
    else:
        result_stats = 0
    return result_stats

    

    


if __name__ == "__main__":

    df = pd.read_excel('result.xlsx') #open file as pd

    for item in df.iterrows(): # iteration by row
        index = item[0]
        row = item[1] # the tuple
        cname = row['①去后缀']
        ename = row['②保留后缀']
        for year in years:
            try:
                request = search(year,ename,cname)
                result_stats=loc_num(request) # get result by bs and re
                df.loc[index,year] = int(result_stats)
                print(cname+' '+ename+'  '+str(year)+'  '+str(result_stats))
            except:
                print("error")
        time.sleep(index%10) # sleep for some time
    df.to_excel('result.xlsx')

    for item in df.iterrows(): # iteration by row
        index = item[0]
        row = item[1] # the tuple
        cname = row['①去后缀']
        ename = row['②保留后缀']
        for year in years:
            if pd.isnull(df.loc[index,year]) == True: # check for nan and retry
                try:
                    request = search(year,ename,cname)
                    result_stats=loc_num(request) # get result by bs and re
                    df.loc[index,year] = int(result_stats)
                    print(cname+' '+ename+'  '+str(year)+'  '+str(result_stats))
                except:
                    print("error")
    df.to_excel('result.xlsx')

    
    






        

    
