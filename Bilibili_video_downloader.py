import requests
import re
import json
import os

#Set origin address
def set_url():
    url = input('Enter video address: ')
    headers.update({'referer':url})
    return url

#test_url = "https://www.bilibili.com/video/BV1Dg411F7G6"

#Request Header
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53',
    'referer': '',
    'range': 'bytes=0-'
}

#Get video and audio infromation on the html file and replace to the json file 
def getVideoDetail():
    src = requests.get(url=url,headers=headers)
    webtext = src.text
    data = re.findall(r'<script>window.__playinfo__=(.*?)</script>', webtext)[0]
    title = re.findall(r'<title data-vue-meta="true">(.*?)</title>',webtext)[0]
    #acid = re.findall(r'<script>window.__INITIAL_STATE__=(.*?)</script>', webtext)[0]
    json_data = json.loads(data)
    #json_acid = json.loads(acid)
    #aid = json_acid['aid'][0]
    #cid = json_acid['cid'][0]
    #print('aid: '+aid+'cid: '+cid)
    return json_data,title

# Use the json file to select video and audio address
def getVideoLink():
    json_data,_ = getVideoDetail()
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    return video_url,audio_url

#Download
def downloadVideo():
    video_url,audio_url = getVideoLink()
    _,title = getVideoDetail()
    print('Now Downloading: \n' + '\033[4;33m' + title + '\033[0m' + '\n' + '\033[1;34m Video_Url: \033[0m' + video_url + '\n' + '\033[1;34m Audio_Url: \033[0m' + audio_url)
    video_save = requests.get(video_url, headers=headers)
    audio_save = requests.get(audio_url, headers=headers)
    with open('video.mp4','wb') as fp:
        fp.write(video_save.content)
    with open('audio.mp4','wb') as fp:
        fp.write(audio_save.content)
    print('\033[5;31m OK.\033[0m')
    os.system("pause")

#Start
if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    url = set_url()
    getVideoDetail()
    getVideoLink()
    downloadVideo()
