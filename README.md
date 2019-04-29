# movie_spyder
在豆瓣上爬取复联4电影评论，将词云图可视化出来。

<div align="center">
<img src="./f2.jpg" height="320" width="320" >
</div>

词频最高的是“复联”、“十年”、“漫威”、“情怀”、“最后”等。
## 分析
先通过影评网页确定爬取的内容。我要爬取的是用户名，是否看过，五星评论值，评论时间，有用数以及评论内容。

## 数据爬取
本文爬取数据，采用的主要是 requests 库和 lxml 库中 Xpath。豆瓣网站虽然对网络爬虫算是很友好，但是还是有反爬虫机制。如果你没有设置延迟，一下子发起大量请求，会被封 IP 的。另外，如果没有登录豆瓣，只能访问前 10 页的影片。因此，发起爬取数据的 HTTP 请求要带上自己账号的 cookie。搞到 cookie 也不是难事，可以通过浏览器登录豆瓣，然后在开发者模式中获取。

我想从影评首页开始爬取，爬取入口是：https://movie.douban.com/subject/26100958/comments
然后依次获取url地址以及需要爬取的内容，接着继续访问下一个页面的地址。

我在请求头中增加随机变化的 User-agent, 增加 cookie。最后增加请求的随机等待时间，防止请求过猛被封 IP。

## 制作云图
因为爬取出来评论数据都是一大串字符串，所以需要对每个句子进行分词，然后统计每个词语出现的评论。我采用 jieba 库来进行分词，然后使用WordCloud和matplotlib来可视化出词云图。


## 使用
- `git clone git@github.com:binaryacademy/movie_spyder.git`
- 运行`douban.py`

*  关注我们微信公众号，了解更多
<div align="center">
<img src="https://raw.githubusercontent.com/lidabing/AirView/master/WechatIMG1.jpeg" height="160" width="160" >
</div>

---
*  加我们winter老师账号进群学习
<div align="center">
<img src="https://raw.githubusercontent.com/binaryacademy/tf-pose-estimation/master/winter.jpeg" height="160" width="160" >
</div>

