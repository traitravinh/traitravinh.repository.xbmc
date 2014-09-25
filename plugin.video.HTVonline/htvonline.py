__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
# import SimpleDownloader as downloader

homelink = 'http://www.htvonline.com.vn/livetv'
logo = 'http://static.htvonline.com.vn/layout/images/logo.png'

def home():
    addDir('[COLOR ffff0000]Phim [/COLOR][COLOR ff32cd32]Viet [/COLOR][COLOR ff0000ff]Nam[/COLOR]','http://www.htvonline.com.vn/phim-viet-nam',3,logo)
    addDir('[COLOR ffff0000]T[/COLOR][COLOR ff32cd32]V[/COLOR][COLOR ff0000ff] Show[/COLOR]','http://www.htvonline.com.vn/shows',3,logo)
    link = urllib2.urlopen(homelink).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    divLiveTV = soup.findAll('div',{'id':'divLiveTV'})
    aChannels = BeautifulSoup(str(divLiveTV[0]))('a',{'class':'mh-grids5-img'})
    for channel in aChannels:
        channelTitle = BeautifulSoup(str(channel))('a')[0]['title'].encode('utf-8')
        channelLink = BeautifulSoup(str(channel))('a')[0]['href'].encode('utf-8')
        channelImage = BeautifulSoup(str(channel))('img')[0]['src']
        addLink(channelTitle,channelLink,2,channelImage)

def index(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    atags = soup.findAll('a',{'class':'mh-grids4-img'})
    icount = 0
    for a in atags:
        aSoup = BeautifulSoup(str(a))
        alink = aSoup('a')[0]['href'].encode('utf-8')
        aImage = aSoup('img')[0]['data-original']
        aTitle = soup('p',{'class':'name-en'})[icount].contents[0].encode('utf-8')

        icount+=1
        addLink(aTitle,alink,2,aImage)

    paging = soup.findAll('div',{'class':'paging'})[0]
    pagelist = BeautifulSoup(str(paging))('a')
    for p in range(1,len(pagelist)):
        plink = BeautifulSoup(str(pagelist[p]))('a')[0]['href']
        ptitle = BeautifulSoup(str(pagelist[p]))('a')[0].contents[0]
        if plink.find('javascript:void(0)')==-1:
            addDir(ptitle,plink,1,logo)

def indexdir(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    atags = soup.findAll('a',{'class':'mh-grids4-img'})
    icount = 0
    for a in atags:
        aSoup = BeautifulSoup(str(a))
        alink = aSoup('a')[0]['href'].encode('utf-8')
        aImage = aSoup('img')[0]['data-original']
        aTitle = soup('p',{'class':'name-en'})[icount].contents[0].encode('utf-8')

        icount+=1
        # addLink(aTitle,alink,2,aImage)
        addDir(aTitle,alink,4,aImage)

    paging = soup.findAll('div',{'class':'paging'})[0]
    pagelist = BeautifulSoup(str(paging))('a')
    for p in range(1,len(pagelist)):
        plink = BeautifulSoup(str(pagelist[p]))('a')[0]['href']
        ptitle = BeautifulSoup(str(pagelist[p]))('a')[0].contents[0]
        if plink.find('javascript:void(0)')==-1:
            addDir(ptitle,plink,1,logo)
def episodes(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    try:
        list_episodes = soup.findAll('div',{'class':'images_container'})
        a_episodes = BeautifulSoup(str(list_episodes[0]))('a')
        for a in a_episodes:
            ahref = BeautifulSoup(str(a))('a')[0]['href']
        #     # aTitle = BeautifulSoup(str(BeautifulSoup(str(a)).a.next.next))('i')[0].contents[0]
            aTitle = BeautifulSoup(str(a)).a.next.next
        #     # aTitle = itags[0].contents[0]
        #     # print aTitle
        #     # addLink(str(aTitle).encode('utf-8'),ahref.encode('utf-8'),2,iconimage)
            addLink(str(aTitle).replace('<i>','').replace('</i>',''),ahref.encode('utf-8'),2,iconimage)
    except:
        addLink(name,url,2,iconimage)

def videoLink(url):
    link = urllib2.urlopen(url).read()
    newlink = ''.join(link.splitlines()).replace('\t','')
    vlink = re.compile('file: "(.+?)",').findall(newlink)
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

def addDir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
    index(url)
elif mode==2:
    play(url)
elif mode==3:
    indexdir(url)
elif mode==4:
    episodes(url)

xbmcplugin.endOfDirectory(int(sysarg))