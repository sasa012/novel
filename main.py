import requests
from bs4 import BeautifulSoup
import configparser
from wxpusher import WxPusher
import os

# 设置请求头部信息，伪装成浏览器发起请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 读取配置文件中的最新章节id
config = configparser.ConfigParser()
config.read('config.ini')
latest_chapter_id = config.getint('book', 'latest_chapter_id')


# 访问网页并读取最新章节id
url = 'https://www.qidian.com/book/1021624434/'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
latest_chapter_url = soup.find('a', class_='book-latest-chapter')['href']
latest_chapter_id_new = int(latest_chapter_url.split('/')[-2])

# 比较最新章节id并输出结果
if latest_chapter_id_new == latest_chapter_id:
    print('还没更新')
else:
    print('章节更新了')
    WxPusher.send_message('小说更新了！',
                      uids=[f"{os.environ['WX_UID']}"],
                      token=f"{os.environ['WX_TOKEN']}")
    config.set('book', 'latest_chapter_id', str(latest_chapter_id_new))
    with open('config.ini', 'w') as f:
        config.write(f)
