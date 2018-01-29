#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#__author__:goukunpeng 2018/1/29
import requests
import time
import re
import json

def specifiedsongID():  #获得指定歌曲sid
    songName = input("请输入你要下载的歌曲名：")
    url = 'http://music.baidu.com/search?'
    data = {'key': songName}
    response = requests.get(url,params = data)
    response.encoding = 'utf-8'
    specifiedsongid = re.findall(r'sid&quot;:(\d+)',response.text)
    return specifiedsongid

def one_song_sid():  #下载指定歌曲指（指定歌手)
    songname = input("请输入要下载的歌曲名：")
    url_sid = 'http://music.baidu.com/search?'
    data = {'key': songname }
    response_sid = requests.get(url_sid,params=data)
    response_sid.encoding = 'utf-8'
    sid = re.findall(r'sid&quot;:(\d+)',response_sid.text)
    # print(sid)
    order = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'
    }
    for id in sid :
        url_download = "http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&" \
              "callback=jQuery172012899607095157362_1516780559345&songid=%s&_=1516780562795" % id
        response_download = requests.get(url_download,headers=headers)
        songinfo = re.findall(r'\((.*)\)',response_download.text)[0]
        data = json.loads(songinfo)  # 将提取出来的内容加载成json格式
        song_name = data['songinfo']['title']
        song_author = data['songinfo']['author']
        song_id = data['songinfo']['song_id']
        song_filelink = data['bitrate']['file_link']
        print('\n',"序号:",order,'\n', "歌曲名：", song_name, '\n', "歌手:", song_author, '\n', "歌曲ID：", song_id, '\n', "歌曲链接:", song_filelink)
        order = order + 1
    print("******输入序号下载对应歌曲******")
    num = int(input("请输入序号："))
    print("******开始下载歌曲******")
    url_dn =  "http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&" \
              "callback=jQuery172012899607095157362_1516780559345&songid=%s&_=1516780562795" % sid[num]
    response_dn = requests.get(url_dn,headers=headers)
    song_info = re.findall(r'\((.*)\)',response_dn.text)[0]
    data = json.loads(song_info)
    song_name = data['songinfo']['title']
    singer = data['songinfo']['author']
    song_link = data['bitrate']['file_link']
    song_downloadurl = song_link
    song_content = requests.get(song_downloadurl,headers=headers)
    time.sleep(3)
    with open('F:\\baidumusicdownloadlist\\%s+%s.mp3' % (song_name,singer), 'wb') as song:
        song.write(song_content.content)
    print('******歌曲下载完成******')


def querysongidlist():  #查询歌曲sid
    singer = input("输入歌手名：")
    # url = 'http://music.baidu.com/search?key=%s' % singer
    # response = requests.get(url)
    url = 'http://music.baidu.com/search?'
    data = {'key' : singer}
    response = requests.get(url,params=data)   #了解params,headers
    response.encoding = 'utf-8'
    htmlcontent = response.text
    #在html里 &quot;  是 双引号
    #翻页查找歌曲ID
    songNum = int(re.findall(r'歌曲\((\d+)\)',htmlcontent)[0])   #查看歌曲数目
    print('歌曲数目：',songNum)
    if songNum %20 == 0:
        page = songNum //20
    else :
        page = songNum //20 + 1
    if songNum <= 20 :
        songidList = re.findall(r'sid&quot;:(\d+)',htmlcontent)
        return songidList
    elif songNum == 0 :
        print("找不到歌曲！！")
    else :
        start = 0
        songidList = []
        while page > 0 :
            url_nextpage = 'http://music.baidu.com/search/song?s=1&key=%s&jump=0&start=%s&size=20&third_type=0' % (singer,start)
            response_nextpage = requests.get(url_nextpage)
            response_nextpage.encoding = 'utf-8'
            songid = re.findall(r'sid&quot;:(\d+)',response_nextpage.text)
            page = page - 1
            start = start + 20
            songidList.append(songid)
            while page == 0 :
                return songidList
# songidList = querysongidlist()

def downloadmusics(songid):    #通过歌曲sid下载歌曲
    url = "http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&" \
          "callback=jQuery172012899607095157362_1516780559345&songid=%s&_=1516780562795" % songid
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36'}
    response = requests.get(url,headers = headers)
    content = response.text
    info = re.findall(r'\((.*)\)',content)[0]    #通过正则表达式将content里面的json格式的内容提取出来
    # print(info,type(info))   #判断此时info为str格式
    data = json.loads(info)   #将提取出来的内容加载成json格式
    # print(data,type(data))      #此时data为dict格式
    song_name = data['songinfo']['title']
    song_author = data['songinfo']['author']
    song_id = data['songinfo']['song_id']
    song_filelink = data['bitrate']['file_link']
    print('\n',"歌曲名：",song_name,'\n',"歌手:",song_author,'\n',"歌曲ID：",song_id,'\n',"歌曲链接:",song_filelink,'\n')
    ###进行下载歌曲
    song_downloadurl = song_filelink   #获得歌曲下载链接
    # print(song_downloadurl)
    responseOfSong = requests.get(song_downloadurl,headers = headers)
    time.sleep(3)
    with open('F:\\baidumusicdownloadlist\\%s+%s.mp3' % (song_name,song_author),'wb') as song :
        song.write(responseOfSong.content)
    with open('F:\\baidumusicdownloadlist\\musiclist.txt','a',encoding= 'gbk') as musiclist :
        musiclist.write(song_name + '\n' +song_author+ '\n' + song_id+ '\n' + song_filelink +'\n'*2)


print("请选择下载方式：1.下载指定歌曲； 2. 下载指定歌曲（指定歌手） 3.下载指定歌手所有歌曲")
choose = int(input('输入指令：'))    #input的是str格式，需要格式化成int类型
if choose == 1 :
    specifiedsongid = specifiedsongID()
    for songid in specifiedsongid :
        downloadmusics(songid)
        print('正在下载歌曲！！！')
elif choose == 2:
    one_song_sid()
elif choose == 3 :
    songidList = querysongidlist()  # 得到songidlist
    for sid in songidList :         #songidList是一个List，而downloadmusics（）函数也可以传list作为参数。
        downloadmusics(sid)
        print('正在下载歌曲！！！')
else :
    print("输入指令错误，请重新输入")



