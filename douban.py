import jieba
import requests
import pandas as pd
import time
import random
from lxml import etree
import codecs
import csv

from wordcloud import WordCloud
import PIL
import matplotlib.pyplot as plt
import numpy as np



def start_spider():
    base_url = 'https://movie.douban.com/subject/26100958/comments'
    start_url = base_url + '?start=0'

    number = 1
    html = request_get(start_url)

    while html.status_code == 200:
        # 获取下一页的 url
        selector = etree.HTML(html.text)
        nextpage = selector.xpath("//div[@id='paginator']/a[@class='next']/@href")
        nextpage = nextpage[0]
        next_url = base_url + nextpage
        # 获取评论
        comments = selector.xpath("//div[@class='comment']")
        marvelthree = []
        for each in comments:
            marvelthree.append(get_comments(each))

        data = pd.DataFrame(marvelthree)
        # 写入csv文件,'a+'是追加模式
        try:
            if number == 1:
                csv_headers = ['用户', '是否看过', '五星评分', '评论时间', '有用数', '评论内容']
                data.to_csv('./Marvel3_yingpping.csv', header=csv_headers, index=False, mode='a+', encoding='utf-8')
            else:
                data.to_csv('./Marvel3_yingpping.csv', header=False, index=False, mode='a+', encoding='utf-8')
        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

        data = []

        html = request_get(next_url)

def request_get(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    timeout = 3

    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    ]

    header = {
        'User-agent': random.choice(UserAgent_List),
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/26100958/?from=showing',
    }

    session = requests.Session()

    cookie = {
        'cookie':'bid=E5bYIGnWtNE; gr_user_id=ed90e589-b905-477c-b3e7-e57008590217; __utmc=30149280; _vwo_uuid_v2=DCD2E95E0533104A85C37CBDF0DC6BE01|ec780445f2e4241c537594c0b3ece184; douban-fav-remind=1; __utmv=30149280.16452; ll="118124"; viewed="2178200_1217343_1858576_30314653_26176870_3852290_3108799_10798475"; __utmc=223695111; ct=y; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1556175414%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D%25E5%25A4%258D%25E4%25BB%2587%25E8%2580%2585%25E8%2581%2594%25E7%259B%259F4%22%5D; _pk_ses.100001.4cf6=*; ps=y; ck=PSva; _pk_id.100001.4cf6=e2b4be7d74b1b7f1.1553737626.3.1556175529.1556172807.; __utma=30149280.603561506.1535476333.1556172207.1556175529.21; __utmb=30149280.0.10.1556175529; __utmz=30149280.1556175529.21.21.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utma=223695111.530618605.1553737626.1556172264.1556175529.3; __utmb=223695111.0.10.1556175529; __utmz=223695111.1556175529.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0'
    }

    time.sleep(random.randint(5, 15))
    response = requests.get(url, headers=header, cookies=cookie, timeout = 3)
    if response.status_code != 200:
        print(response.status_code)
    return response

def get_comments(eachComment):
    commentlist = []
    user = eachComment.xpath("./h3/span[@class='comment-info']/a/text()")[0]  # 用户
    watched = eachComment.xpath("./h3/span[@class='comment-info']/span[1]/text()")[0]  # 是否看过
    rating = eachComment.xpath("./h3/span[@class='comment-info']/span[2]/@title")  # 五星评分
    if len(rating) > 0:
        rating = rating[0]

    comment_time = eachComment.xpath("./h3/span[@class='comment-info']/span[3]/@title")  # 评论时间
    if len(comment_time) > 0:
        comment_time = comment_time[0]
    else:
        # 有些评论是没有五星评分, 需赋空值
        comment_time = rating
        rating = ''

    votes = eachComment.xpath("./h3/span[@class='comment-vote']/span/text()")[0]  # "有用"数
    content = eachComment.xpath("./p/span/text()")[0]  # 评论内容
    content_c = eachComment.xpath("./p/span/text()")

    print('评论内容：')
    print(content)

    commentlist.append(user)
    commentlist.append(watched)
    commentlist.append(rating)
    commentlist.append(comment_time)
    commentlist.append(votes)
    commentlist.append(content.strip())
    # print(list)
    return commentlist

def split_word():
    with codecs.open('Marvel3_yingpping.csv', 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        content_list = []
        for row in reader:
            try:
                cc = row[5]
                if len(cc) > 2:
                    content_list.append(cc)
                #print("row5")
                #print(row[5])
            except IndexError:
                pass

        content = ''.join(content_list)


        seg_list = list(jieba.cut(content, cut_all=False))
        result = []
        for word in seg_list:
            if len(word) > 1:
                if word == '我们' or word == '他们' or word == '一个' or word == '电影':
                    continue
                result.append(word)

        result = '\n'.join(result)
        print(type(result))
        #print('result:::')
        print(result)
        return result


def wordcloudplot(txt):
    path = './msyh.ttf'
    path.encode('gb18030')
    alice_mask = np.array(PIL.Image.open('./f.jpg'))
    wordcloud = WordCloud(font_path=path, background_color="white", margin=5, width=1800, height=800, mask=alice_mask, max_words=2000, max_font_size=60, random_state=42)
    wordcloud = wordcloud.generate(txt)
    wordcloud.to_file('./f2.jpg')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    #start_spider()
    result = split_word()
    wordcloudplot(result)