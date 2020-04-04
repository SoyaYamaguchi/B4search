#この方法だと口コミの個別ページまで行って口コミを取得するためアクセスが多い

from selenium import webdriver #Selenium Webdriverをインポートして
import requests
from bs4 import BeautifulSoup
import time
import csv
import re


driver = webdriver.Chrome("/usr/local/bin/chromedriver") #Chromeを動かすドライバを読み込み
# 要素が表示されるまで10秒待機する設定
driver.implicitly_wait(10)
#口コミのリスト表示のURL
driver.get("https://tabelog.com/tokyo/A1324/A132402/13209621/dtlrvwlst/") 
review_list=[]
#口コミの数を記録
reviews = driver.find_elements_by_css_selector('.rvw-item.js-rvw-item-clickable-area')

#無駄なタグを除去する関数
def format(arg1):
    return re.sub('<[^>]+>|\[|\]|\\n','',str(arg1))

for i in range(10):
    rev = driver.find_elements_by_css_selector('.rvw-item.js-rvw-item-clickable-area')
    rev[i].click()
    #口コミの個別ページへ
    #カレントページのURLを取得
    cur_url = driver.current_url
    #カレントページのURLを表示
    r = requests.get(cur_url)
    soup = BeautifulSoup(r.content, "html.parser")
    #店の名前
    shop =soup.select('h2.display-name > a')
    #口コミのタイトル
    title = soup.select('p.rvw-item__title')
    #口コミの内容
    review = soup.select('div.rvw-item__rvw-comment > p')

    review_list.append([cur_url, format(str(shop)), format(str(title)), format(str(review))])
    driver.back()
    time.sleep(0.5)
driver.quit()

#CSVとして出力
with open('csv1.csv','w') as csv_file:
    fieldnames = ['cur_url','shop','title','review']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for a in review_list:
        writer.writerow({'cur_url':a[0],'shop': a[1], 'title': a[2], 'review':a[3]})
    
print(len(reviews))
for a in review_list:
    print(a)

