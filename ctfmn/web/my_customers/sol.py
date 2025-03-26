url = 'http://139.162.5.230:10312/user/'

import requests


for i in range(5000):
    res = requests.get(url+str(i))
    if 'HZ' in res:
        print(res)
        break
