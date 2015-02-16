import urllib, urllib2, re, os, sys
from bs4 import BeautifulSoup

import xbmcaddon,xbmcplugin,xbmcgui
import urlresolver
import SimpleDownloader as downloader


downloader = downloader.SimpleDownloader()
addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
mysettings = xbmcaddon.Addon(id='plugin.video.anhtrang_org')
downloadpath = mysettings.getSetting('download_path')
home = mysettings.getAddonInfo('path')
homelink = 'http://phim.anhtrang.org'
logo = xbmc.translatePath(os.path.join(home, 'icon.png'))
searchlink = 'http://m.anhtrang.org/tim-kiem/'

while (not os.path.exists(xbmc.translatePath("special://profile/addon_data/"+addonID+"/settings.xml"))):
    addon.openSettings()
def loadHistory(url):
    try:
        addDir('[COLOR ffff8c00]Search[/COLOR]',url,6,logo,False,None)
        if mysettings.getSetting('save_search')=='true':
            searches = getStoredSearch()
            if len(searches)!=0:
                searches = eval(searches)
                idn = 0
                for s in searches:
                    addDir(s,url+urllib.quote_plus(s),2,logo,True,idn)
                    idn+=1
    except:pass

def deleteSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        searches.pop(inum)
        saveStoredSearch(searches)
        # xbmc.executebuiltin("XBMC.Container.Refresh")
    except:pass

def editSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        keyb = xbmc.Keyboard(name, '[COLOR ffff8c00]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            newsearch = keyb.getText()
            searches[inum]=newsearch
        saveStoredSearch(searches)
        newsearch=urllib.quote_plus(newsearch)
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Search(searchlink+newsearch+'.html')
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR ffff8c00]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            url = searchlink+ searchText+'.html'
            if mysettings.getSetting('save_search')=='true':
                if searchText!='':
                    if len(searches)==0:
                        searches = ''.join(["['",urllib.unquote_plus(searchText),"']"])
                        searches = eval(searches)
                    else:
                        searches = eval(searches)
                        searches = [urllib.unquote_plus(searchText)] + searches
                    saveStoredSearch(searches)
        return url
    except:pass

def Search(url):
    try:
        if url.find('.html')!=-1:
            url = url.rstrip()
        else:
            url = getUserInput()
        xbmc.executebuiltin("XBMC.Container.Refresh")
        index(url)
    except: pass

def getStoredSearch():
    try:
        searches = mysettings.getSetting('store_searches')
        return searches
    except:pass

def saveStoredSearch(param):
    try:
        mysettings.setSetting('store_searches',repr(param))
        # xbmc.executebuiltin("XBMC.Container.Refresh")
    except:pass

## End Search


def GetContent(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-agent','Mozilla/5.0')
    response = urllib2.urlopen(req).read()
    return response

def GetContentMobile(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-agent','Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    response = urllib2.urlopen(req).read()
    return response

def home():
    try:
        addDir('[COLOR ffff8c00]Search[/COLOR]',searchlink,1,logo,False,None)
        link = GetContent(homelink)
        soup = BeautifulSoup(link.decode('utf-8'))
        category = soup('a',{'class':'link'})
        for cat in category:
            catlink = BeautifulSoup(str(cat))('a')[0]['href']
            cattitle = BeautifulSoup(str(cat))('span')[0].contents[0]
            addDir(cattitle.encode('utf-8'),catlink,2,logo,False,None)
    except:pass

def index(url):
    try:
        link = GetContent(url)
        soup = BeautifulSoup(link.decode('utf-8'))
        list_movies = soup('div',{'class':'poster'})
        for movie in list_movies:
            movie_img = BeautifulSoup(str(movie))('img')[0]['src']
            movie_link = BeautifulSoup(str(movie))('a')[0]['href']
            matchObj = re.match('http?:\/\/(w+)?\.?\w+\.+(\w+)?\.?\w+\/',movie_link).group()
            movie_link = movie_link.replace(matchObj,'http://m.anhtrang.org/')
            movie_title = BeautifulSoup(str(movie))('a')[0]['title']
            addDir(movie_title.encode('utf-8'),movie_link,3,movie_img,False,None)
        pages = soup('a',{'class':'pagelink'})
        for p in pages:
            plink = BeautifulSoup(str(p))('a')[0]['href']
            ptitle = BeautifulSoup(str(p))('a')[0].contents[0]
            addDir(ptitle,plink,2,logo,False,None)
    except:pass

def episodes(url):
    try:
        link = GetContentMobile(url)
        soup = BeautifulSoup(link.decode('utf-8'))
        addLink('1',url,4,'',iconimage)
        episodes = soup('a',{'class':'ep'})
        for e in episodes:
            etitle = BeautifulSoup(str(e))('a')[0].contents[0]
            elink = BeautifulSoup(str(e))('a')[0]['href']
            addLink(etitle,elink,4,'',iconimage)
    except:pass

def play(url):
    try:
        videoId = getVideoLink(url)
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        listitem.setPath(videoId)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    except:pass

def getVideoLink(url):
    try:
        link = GetContent(url)
        soup = BeautifulSoup(link.decode('utf-8'))
        source = soup('source')[0]['src']
        return source
    except:pass

def addDir(name,url,mode,iconimage,edit,inum):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)
    # ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR ffff8c00]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%d)'%('plugin://plugin.video.anhtrang_org',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        contextmenuitems.append(('[COLOR yellow]Edit[/COLOR] [COLOR ffff8c00]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%d)'%('plugin://plugin.video.anhtrang_org',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
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
mirror=None
iconimage=None
edit=None
inum=None

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
try:
        edit = bool(params["edit"])
except:
        pass
try:
        inum=int(params["inum"])
except:
        pass

sysarg=str(sys.argv[1])
if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    loadHistory(url)
elif mode==2:
    index(url)
elif mode==3:
    episodes(url)
elif mode==4:
    play(url)
elif mode==5:
    getVideoLink(url)
elif mode==6:
    Search(url)
elif mode==8:
    deleteSearch()
elif mode==9:
    editSearch()
xbmcplugin.endOfDirectory(int(sysarg))