__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
from bs4 import BeautifulSoup
import xbmcaddon,xbmcplugin,xbmcgui
import urlresolver
import SimpleDownloader as downloader

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
mysettings = xbmcaddon.Addon(id='plugin.video.phimxixam')
home_path = mysettings.getAddonInfo('path')
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
message = "Please wait! Loading.."
time=3000
searchlink = 'http://phim.xixam.com/tim-kiem/?tk='
homelink = 'http://phim.xixam.com'
mhomelink='http://phim.xixam.com/m'
logo ='http://phim.xixam.com/images/logo.png'

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
        Search(searchlink+newsearch)
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR ffff8c00]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            url = searchlink+ searchText
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
        if url.find('+')!=-1:
            url = url.rstrip()
        else:
            if len(re.compile('\w\s\w$').findall(url))==0:
                if len(re.compile('=$').findall(url))==0:
                    url=url
                else:
                    url = getUserInput()
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

def home():
    try:
        addDir('[COLOR ffff8c00]Search[/COLOR]',searchlink,1,logo,False,None)
        link = urllib2.urlopen(homelink).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        ul_sf_menu = soup('ul',{'class':'sf-menu'})
        li = BeautifulSoup(str(ul_sf_menu[0]))('li')
        for l in li:
            ltitle = BeautifulSoup(str(l))('a')[0].contents[0]
            llink = BeautifulSoup(str(l))('a')[0]['href']
            if ltitle!=' ' and llink!='javascript:;':
                addDir(ltitle.encode('utf-8'),homelink+llink,2,logo,False,None)
    except:pass

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        div_BlockProduct2 = soup('div',{'class':'BlockProduct2'})
        for div in div_BlockProduct2:
            div_title = BeautifulSoup(str(div))('a')[1].contents[0]
            div_link = BeautifulSoup(str(div))('a')[0]['href']
            div_img = BeautifulSoup(str(div))('img')[0]['src']
            if div_img.find('http://')==-1:
                div_img = homelink+div_img
            addDir(div_title.encode('utf-8'),homelink+div_link,3,div_img,False,None)

        div_fr_page_links = soup('div',{'class':'fr_page_links'})
        pages = BeautifulSoup(str(div_fr_page_links[0]))('a')
        for p in pages:
            ptitle = BeautifulSoup(str(p))('a')[0].contents[0]
            plink = BeautifulSoup(str(p))('a')[0]['href']
            addDir(ptitle,homelink+plink,2,logo,False,None)
    except:pass

def overview(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    div_overview = soup('div',{'class':'overview'})
    p_style_10px = BeautifulSoup(str(div_overview[0]))('p',{'style':'padding-top:10px'})
    return mhomelink+BeautifulSoup(str(p_style_10px[0]))('a')[0]['href']

def serverlist(url):
    try:
        link = urllib2.urlopen(overview(url)).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        div_serverlist = soup('div',{'class':'serverlist'})
        if inum is None:
            for i in range(0,len(div_serverlist)):
                svtitle = BeautifulSoup(str(div_serverlist[i]))('div',{'class':'serverlist'})[0].next.contents[0]
                svindex = i
                addDir(svtitle,url,3,iconimage,False,svindex)
        else:
            episodes = BeautifulSoup(str(div_serverlist[inum]))('a')
            for e in episodes:
                etitle = BeautifulSoup(str(e))('a')[0].contents[0]
                elink =''.join([mhomelink,'/',BeautifulSoup(str(e))('a')[0]['href']])
                addLink(etitle,elink,4,'',iconimage)
    except:pass

def videoLink(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        if link.find('http://www.youtube.com/embed/')!=-1:
            video = soup('iframe')[1]['src']
        else:
            video = BeautifulSoup(str(soup('video')[0]))('source')[0]['src']
        return video
    except:pass

def play(url):
    try:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,message, time, iconimage))
        videoId = videoLink(url)
        if videoId.find('youtube')!=-1:
            hostedmedia = urlresolver.HostedMediaFile('http://youtube.com/watch?v=%s'%(re.compile('http://www.youtube.com/embed/(.+?)\?').findall(videoId)[0]))
            videoId = hostedmedia.resolve()
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        listitem.setPath(videoId)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        # xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(videoId,listitem)

    except:pass

def addDir(name,url,mode,iconimage,edit,inum):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)
    # ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR ffff8c00]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%d)'%('plugin://plugin.video.phimxixam',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        contextmenuitems.append(('[COLOR yellow]Edit[/COLOR] [COLOR ffff8c00]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%d)'%('plugin://plugin.video.phimxixam',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
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
    serverlist(url)
elif mode==4:
    play(url)
elif mode==5:
    videoLink(url)
elif mode==6:
    Search(url)
elif mode==8:
    deleteSearch()
elif mode==9:
    editSearch()

xbmcplugin.endOfDirectory(int(sysarg))