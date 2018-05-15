#!/usr/bin/python
#_*_ coding: UTF-8 _*_
from selenium import webdriver
import csv
import codecs

# 云音乐第一页的url
url = "http://music.163.com/#/discover/playlist"

# 用phantomJS接口创建Selenium的websetdemo1
setdemo1 = webdriver.PhantomJS()

# 准备写入csv文件
csv_file = open("playlist.csv", "w")
csv_file.write(codecs.BOM_UTF8)
writer = csv.writer(csv_file)
writer.writerow(['标题','播放数','连接'])

count = 0

# 解释每一页，直到‘下一页’为空
while url != 'javascript:void(0)':
    # 用websetdemo1加载页面
    setdemo1.get(url)
    # 切换到内容iframe
    setdemo1.switch_to.frame("contentFrame")
    # 定位歌单标签
    data = setdemo1.find_element_by_id("m-pl-container").find_elements_by_tag_name("li")
    print '总页数:',len(data)
    # 解释每一页中的所有歌单
    for i in range(len(data)):
        # 获取播放数
        nb = data[i].find_element_by_class_name("nb").text
        if u"万" in nb and (nb.split(u"万")[0]) > 500:
            # 获取播放数大于500万的歌单的封面
            msk = data[i].find_element_by_css_selector("a.msk")
            count = count+1
            # 把封面上的标题和链接连同播放数一起写到文件中
            writer.writerow([msk.get_attribute('title').encode("utf-8"),nb.encode("utf-8"),msk.get_attribute('href').encode("utf-8")])
    url = setdemo1.find_element_by_css_selector("a.zbtn.znxt").get_attribute("href")
csv_file.close()
print u'符合条件歌单总数：',count