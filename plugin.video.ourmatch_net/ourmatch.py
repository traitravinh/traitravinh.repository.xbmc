import urllib, urllib2, re, os, sys
from bs4 import BeautifulSoup
# import BeautifulSoup
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui

homelink = 'http://ourmatch.net'
playwire_base_url='http://cdn.playwire.com/'
mysettings = xbmcaddon.Addon(id='plugin.video.ourmatch_net')
home = mysettings.getAddonInfo('path')
logo = 'http://www.ourmatch.net/wp-content/themes/OurMatchV2/images/logo.png'

def GetContent(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-agent','Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    response = urllib2.urlopen(req).read()
    return response

def home():
    try:
        link = GetContent(homelink)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match = re.compile('<div class="division">(.+?)<div class="ads_mid">').findall(newlink)
        addDir('Latest Games',homelink,1,logo)
        li = BeautifulSoup(str(match[0].replace('\t','')))('li',{'class':'hover-tg'})
        for l in li:
            lilink = BeautifulSoup(str(l))('a')[0]['href']
            lititle = BeautifulSoup(str(l))('a')[0].contents[0]
            addDir(lititle,lilink,1,logo)
    except:pass

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        match = re.compile('<div id="main-content">(.+?)<footer id="footer">').findall(newlink)
        thumb = BeautifulSoup(match[0].decode('utf-8'))('div',{'class':'thumb'})
        for t in thumb:
            tlink = BeautifulSoup(str(t))('a')[0]['href']
            ttitle = BeautifulSoup(str(t))('a')[0]['title']
            timage = BeautifulSoup(str(t))('img')[0]['src']
            addDir(ttitle,tlink,2,timage)

        match_pages = re.compile('<div class="loop-nav pag-nav">(.+?)<footer id="footer">').findall(newlink)
        wp_pagenavi = BeautifulSoup(str(match_pages[0]))('div',{'class':'wp-pagenavi'})
        page_larger = BeautifulSoup(str(wp_pagenavi[0]))('a')
        for p in page_larger:
            plink = BeautifulSoup(str(p))('a')[0]['href']
            ptitle = BeautifulSoup(str(p))('a')[0].contents[0]
            addDir(ptitle.encode('utf-8'),plink,1,logo)
    except:pass

def videoLink(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        match = re.compile('embed:\'<iframe src="(.+?)&loop=1').findall(newlink)
        vlink=''
        try:
            rematch = match[0]
            vlink = retrievVideoLink(rematch)
        except:pass
        if vlink is None:
            rematch = re.compile('https://(.+?)&amp').findall(match[0])
            rematch= 'https://'+rematch[0]
            vlink = retrievVideoLink(rematch)
        addLink('Highlights',vlink,3,'',iconimage)

    except:pass

def retrievVideoLink(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link)
        match = soup('video',{'id':'embed_video_player'})
        sources = BeautifulSoup(str(match[0]))('source')
        finallink = BeautifulSoup(str(sources[len(sources)-1]))('source')[0]['src']
        return finallink
    except:pass

def PlayVideo(url):
    try:
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url,listitem)
    except:pass

def addDir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})#, "overlay":6,"watched":False})
    liz.setProperty('mimetype', 'video/x-msvideo')
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
mirror=None
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
try:
        mirror=urllib.unquote_plus(params["mirror"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index(url)
elif mode==2:
    videoLink(url)
elif mode==3:
    PlayVideo(url)
xbmcplugin.endOfDirectory(int(sysarg))