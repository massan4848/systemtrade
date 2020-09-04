from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import talib
import matplotlib.pyplot as plt

##べージのhtmlの取得
stock_number = 1570 #好きな銘柄コード
url = 'https://kabuoji3.com/stock/{}/'.format(stock_number)
### 重要 https://non-dimension.com/solution-403forbidden/
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44"
}
soup = BeautifulSoup(requests.get(url,headers = headers).content,'html.parser')

## 株価データをデータフレーム化
tag_tr = soup.find_all('tr')
head = [h.text for h in tag_tr[0].find_all('th')]

### get data
data = []
for i in range(1,len(tag_tr)):
    data.append([d.text for d in tag_tr[i].find_all('td')])
df = pd.DataFrame(data,columns = head)

## テキストデータを数値、タイムスタンプに変換
col = ['始値','高値','安値','終値','出来高','終値調整']
for c in col:
    df[c] = df[c].astype(float)

## テクニカル指標の取得
date = df['日付']
close = df['終値']

sma25 = talib.SMA(close,timeperiod=25)
sma75 = talib.SMA(close,timeperiod=75)
stochRSI_k, stochRSI_d = talib.STOCHRSI(close,timeperiod=14,fastk_period=5,fastd_period=3,fastd_matype=0)

m25 = sma25.values[0]
m75 = sma75.values[0]
sk = stochRSI_k.values[0]
sd = stochRSI_d.values[0]
ratio = m25/m75

if ratio > 1.02 and sd <20:
    print("buy")
elif ratio < 0.98 or sd >80:
    print("sell")
else:
    print("No signal")
