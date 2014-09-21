__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
# import SimpleDownloader as downloader

homelink = 'http://www.htvonline.com.vn/livetv'

def home():
    link = urllib2.urlopen(homelink).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    divLiveTV = soup.findAll('div',{'id':'divLiveTV'})
    aChannels = BeautifulSoup(str(divLiveTV[0]))('a',{'class':'mh-grids5-img'})
    for channel in aChannels:
        channelTitle = BeautifulSoup(str(channel))('a')[0]['title'].encode('utf-8')
        channelLink = BeautifulSoup(str(channel))('a')[0]['href'].encode('utf-8')
        channelImage = BeautifulSoup(str(channel))('img')[0]['src']
        addLink(channelTitle,channelLink,2,channelImage)

def videoLink(url):
    link = urllib2.urlopen(homelink).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    newlink = ''.join(link.splitlines()).replace('\t','')
    vlink = re.compile('file: "(.+?)",height').findall(newlink)
    return vlink[0]

def play(url):
    try:
        videoId = videoLink(url)
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        listitem.setPath(videoId)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    except:pass

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})#, "overlay":6,"watched":False})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    videoLink(url)
elif mode==2:
    play(url)

xbmcplugin.endOfDirectory(int(sysarg))