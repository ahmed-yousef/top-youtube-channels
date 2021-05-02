import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

search_url='https://www.youtube.com/results?search_query={0}&sp={1}'.format(input('Please enter search query\n'),'CAMSAggF')
about_url='https://www.youtube.com%s/about'
DRIVER_PATH = os.getcwd()+'\\chromedriver.exe'

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
driver2 = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
driver.get(search_url)
html = driver.find_element_by_tag_name('html')
pages=0

while pages < 1:
    html.send_keys(Keys.END)
    time.sleep(2.5)
    pages+=1
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
names = soup.find_all('ytd-video-renderer',class_='ytd-item-section-renderer')
links=[]
add=0

for i in names:
    #get video link
    video_link = i.find_all('a')[0]['href']


    #get video views
    video_views = i.find_all('div',id='metadata-line')[0].find_all('span')[0].text[:-6]
    if video_views[-1] == 'K':
        video_views = float(video_views[:-1])*1000
    elif video_views[-1] == 'M':
        video_views = float(video_views[:-1])*1000000

    #get video channel
    video_channel = i.find_all('div',id='channel-info')[0].find_all('a')[0]['href']

    #get channel name
    channel_name = i.find_all('yt-formatted-string',class_='ytd-channel-name')[0].find_all('a')[0].text
    
    #get channel stats
    print(about_url%video_channel)
    driver2.get(about_url%video_channel)
    channel = driver2.page_source
    soup2 = BeautifulSoup(channel,'html.parser')

    #get channel views
    get_channel_views = float(soup2.find_all('div',id='right-column')[0].find_all(class_='ytd-channel-about-metadata-renderer')[2].text[:-6].replace(',',''))
    #get subscribers numbers
    get_sub_num = soup2.find_all('yt-formatted-string',id='subscriber-count')[0].text[:-12]
    try:
        if get_sub_num[-1] == 'K':
            get_sub_num = float(get_sub_num[:-1])*1000
        elif get_sub_num[-1] == 'M':
            get_sub_num = float(get_sub_num[:-1])*1000000
    except:
        get_sub_num=0
            
    #get inception date
    inception_date = soup2.find_all('div',id='right-column')[0].find_all('span')[1].text



    
    try:
        links.append([channel_name,video_link,video_views,video_channel,get_channel_views,get_sub_num,inception_date])
    except:
        pass
    add+=1
print(len(links))