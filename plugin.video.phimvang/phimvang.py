__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
import urlresolver

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
mysettings = xbmcaddon.Addon(id='plugin.video.phimvang')
icon = addon.getAddonInfo('icon')
message = "Loading. Please Wait!..."
time=6000
root_link = 'http://m.phimvang.com'
logo ='http://phimvang.com/sites/all/themes/news/logo.png'
searchlink = 'http://m.phimvang.com/tim-kiem?key='
mysettings = xbmcaddon.Addon(id='plugin.video.phimvang')
home = mysettings.getAddonInfo('path')
searchHistory = xbmc.translatePath(os.path.join(home,'history.txt'))
while (not os.path.exists(xbmc.translatePath("special://profile/addon_data/"+addonID+"/settings.xml"))):
    addon.openSettings()

def Home():
    addDir('[COLOR ffffd700]Search[/COLOR]',searchlink,5,logo,False,None)
    addDir('[COLOR white]Phim[/COLOR] [COLOR ffffd700]Moi Nhat[/COLOR]','http://m.phimvang.com/phim-moi-cap-nhat.html',1,logo,False,None)
    addDir('[COLOR white]Phim[/COLOR] [COLOR ffff0000]Hot[/COLOR]','http://m.phimvang.com/phim-xem-nhieu/trong-ngay.html',1,logo,False,None)
    link = urllib2.urlopen(root_link).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    a_in_div_view_content =BeautifulSoup(str(soup('div',{'class':'view-content'})[1]))('a')
    for a in a_in_div_view_content:
        atitle = BeautifulSoup(str(a))('a')[0].contents[0]
        alink = BeautifulSoup(str(a))('a')[0]['href']
        addDir(atitle.encode('utf-8'),root_link+alink,1,logo,False,None)

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        title_soup = soup.findAll('div',{'class':'phim_teaser'})
        for t in title_soup:
            tSoup = BeautifulSoup(str(t))
            tLink = tSoup('a')[0]['href']
            tTitle = tSoup('img')[0]['alt']
            tImage = tSoup('img')[0]['src']
            addDir(tTitle.encode('utf-8'),root_link+tLink,2,tImage,False,None)
        page_soup = soup.findAll('li', {'class': 'pager-item'})
        for p in page_soup:
            pSoup = BeautifulSoup(str(p))
            pLink = pSoup('a')[0]['href']
            pTitle = pSoup('a')[0].contents[0]
            addDir(pTitle,root_link+pLink,1,logo,False,None)
    except:pass

def mirrors(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        mirror_soup = soup.findAll('div',{'class':'videobig chapter'})
        mSoup = BeautifulSoup(str(mirror_soup[0]))#because only 1 div found
        server_soup = mSoup.findAll('span',{'class':'link'})
        for i in range(1,len(server_soup)+1):
            addDir('[COLOR white]Server: [/COLOR][COLOR ffffd700]'+str(i)+'[/COLOR]',url,4,iconimage,False,None)
    except:pass

def mirror_link(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    mirror_soup = soup.findAll('div',{'class': 'videobig chapter'})
    mSoup = BeautifulSoup(str(mirror_soup[0]))
    server_soup = mSoup.findAll('span',{'class':'link'})
    for i in range(0,len(server_soup)):
        if name.find(str(i)):
            lSoup = BeautifulSoup(str(server_soup[i])).findAll('a')
            for l in lSoup:
                aSoup = BeautifulSoup(str(l))
                aLink = aSoup('a')[0]['href']
                aTitle = aSoup('a')[0].contents[0]
                addLink(aTitle,root_link+aLink,7,'',iconimage)
            break

def play(VideoUrl,mirror):
    if mirror == 'dailymotion':
        # VideoUrl = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(VideoUrl).replace('?','')
        hostedmedia = urlresolver.HostedMediaFile('http://www.dailymotion.com/embed/video/%s'%(VideoUrl))
        VideoUrl = hostedmedia.resolve()
    elif mirror == 'youtube':
        # VideoUrl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(VideoUrl).replace('?','')
        hostedmedia = urlresolver.HostedMediaFile('http://youtube.com/watch?v=%s'%(VideoUrl))
        VideoUrl = hostedmedia.resolve()
    listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=VideoUrl))
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(VideoUrl,listitem)

def episodes(url):
    try:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,message, time, iconimage))
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        gSoup=[]
        try:
            gSoup = soup.findAll('div', {'class': 'video_container'})
        except:pass
        vLink=''
        mirror=''
        if len(gSoup) > 0:
            vLink = BeautifulSoup(str(gSoup[0]))('source')[0]['src']
            server = 'googlevideo'
            if vLink.find(server):
                mirror = server
        else:
            fSoup = soup.findAll('div', {'class': 'videobig'})
            baseLink = BeautifulSoup(str(fSoup[0]))('iframe')[0]['src']
            vLink,mirror = videoID(baseLink)
        play(vLink,mirror)
    except:pass

def videoID(url):
    id=''
    if url.find('youtube')!=-1:
        idList = re.compile('http://www.youtube.com/embed/(.+)').findall(url)
        id = idList[0]
        mirror = 'youtube'
    elif url.find('dailymotion')!=-1:
        idList=re.compile('http://www.dailymotion.com/video/(.+)').findall(url)
        id = idList[0]
        mirror = 'dailymotion'
    elif url.find('googlevideo')!=-1:
        id = url
        mirror = 'googlevideo'
    return id,mirror

def loadHistory(url):
    try:
        addDir('[COLOR ffffd700]Search[/COLOR]',url,6,logo,False,None)
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
        del(searches[inum])
        saveStoredSearch(searches)
        # xbmc.executebuiltin('Container.Refresh')
    except StopIteration:
        pass

def editSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            newsearch = keyb.getText()
            searches[inum]=newsearch
        saveStoredSearch(searches)
        newsearch=urllib.quote_plus(newsearch)
        Search(searchlink+newsearch)
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR ffffd700]Enter search text[/COLOR]')
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
    except:pass

def addDir(name, url, mode, iconimage,edit,inum):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%d)'%('plugin://plugin.video.phimvang',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        contextmenuitems.append(('[COLOR ff00ff00]Edit[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%d)'%('plugin://plugin.video.phimvang',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
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
    Home()
elif mode==1:
    index(url)
elif mode==2:
    mirrors(url)
elif mode==4:
    mirror_link(url)
elif mode==5:
    loadHistory(url)
elif mode==6:
    Search(url)
elif mode==7:
    episodes(url)
elif mode==8:
    deleteSearch()
elif mode==9:
    editSearch()

xbmcplugin.endOfDirectory(int(sysarg))