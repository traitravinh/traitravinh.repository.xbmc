__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui,urlresolver
from bs4 import BeautifulSoup

mysettings = xbmcaddon.Addon(id='plugin.video.phimtructuyenhd')
home = mysettings.getAddonInfo('path')
downloadpath = mysettings.getSetting('download_path')
searchlink = 'http://m.phimtructuyenhd.com/index.php?name=tim-kiem&str='
home_link = 'http://m.phimtructuyenhd.com'
logo ='http://www.iconki.com/icons/3D/Mimetypes-icons/movie.png'

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link)
        li_a = soup('li',{'data-theme':'a'})
        for li in li_a:
            lilink = BeautifulSoup(str(li))('a')[0]['href']
            lititle = BeautifulSoup(str(li))('a')[0]['title']
            liimage = BeautifulSoup(str(li))('img')[0]['src'].replace('/m.','/') #mobile link is not working

            addDir(lititle.encode('utf-8'),lilink,3,liimage,None,'',False)

        option_value = soup('option')
        for ov in option_value:
            ovlink = BeautifulSoup(str(ov))('option')[0]['value']
            ovtitle = BeautifulSoup(str(ov))('option')[0].contents[0]

            addDir(ovtitle,ovlink,2,logo,None,'',False)
    except:pass

def home():
    try:
        addDir('Search',searchlink,6,logo,None,'',False)
        link = urllib2.urlopen(home_link).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        soup = BeautifulSoup(newlink)
        # print str(len(soup))
        # print soup[0]
        navbar = soup('div',{'data-role':'navbar'})
        navtitle = BeautifulSoup(str(navbar[0]))('a')
        for n in range(1,len(navtitle)-1):
            nlink = BeautifulSoup(str(navtitle[n]))('a')[0]['href']
            ntitle = BeautifulSoup(str(navtitle[n]))('a')[0].contents[0]

            addDir(ntitle.encode('utf-8'),nlink,1,logo,None,'',False)
    except:pass

def index_nav(url):
    try:
        link = urllib2.urlopen(url).read()
        # print link
        soup = BeautifulSoup(link)
        li_a = soup('li',{'data-theme':'a'})
        # print li_a

        for li in range(0,len(li_a)):# for 18+ movies, delete -1
            lilink =BeautifulSoup(str(li_a[li]))('a')[0]['href']
            if lilink.find(home_link)==-1:
                lilink = home_link+lilink
            lititle = BeautifulSoup(str(li_a[li]))('a')[0].contents[0]

            addDir(lititle.encode('utf-8'),lilink,2,logo,None,'',False)

    except:pass

def server(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link)
        svname = soup('span',{'class':'svname'})
        index_num = 0
        for s in svname:
            sname = BeautifulSoup(str(s))('span')[0].contents[0]
            addDir(sname,url,4,iconimage,index_num,sname,False)
            index_num = index_num+1
    except:pass

def episode(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link)
        svep = soup('span',{'class':'svep'})
        eps = BeautifulSoup(str(svep[inum]))('a')
        for e in eps:
            elink = BeautifulSoup(str(e))('a')[0]['href']
            etitle = BeautifulSoup(str(e)).a.next.next.next.string

            addLink(etitle.encode('utf-8'),elink,5,mirror,iconimage)
    except:pass

def videolink(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link)
        if mirror=='YouTube:':
            source =re.compile('http://www.youtube.com/embed/(.+?)\?').findall(str(soup('iframe')[0]['src']))[0]
        else:
            source = soup('source')[0]['src']
        PlayVideo(source,mirror)
    except:
        PlayVideo(url,'')

def PlayVideo(url,mirror):
    try:

        if mirror.lower() == 'dailymotion:':
            hostedmedia = urlresolver.HostedMediaFile('http://www.dailymotion.com/embed/video/%s'%(url))
            videoId=hostedmedia.resolve()
            # videoId = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(url).replace('?','')
        elif mirror.lower() == 'youtube:':
            hostedmedia = urlresolver.HostedMediaFile('http://youtube.com/watch?v=%s'%(url))
            videoId = hostedmedia.resolve()
        else:
            videoId=url

        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=str(videoId)))
        # xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(videoId,listitem)
    except:pass

def loadHistory(url):
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        addDir('Search',url,7,logo,None,'',False)
        if len(searches)!=0:
            indexnum=0
            for s in searches:
                addDir(s,url+urllib.quote_plus(s),2,logo,indexnum,'',True)
                indexnum=indexnum+1
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
        keyb = xbmc.Keyboard(name, 'Enter search text')
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
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            url = searchlink+ searchText
        if searchText!='':
            searches = eval(searches)
            searches = [urllib.unquote_plus(searchText)] + searches
            saveStoredSearch(searches)
        return url
    except:pass

def Search(url):
    try:
        if url.find('html')!=-1:
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
        if len(searches)==0:
            searches="['hello']"
        return searches
    except:pass

def saveStoredSearch(param):
    try:
        mysettings.setSetting('store_searches',repr(param))
    except:pass

def addDir(name, url, mode, iconimage, inum,mirror,edit):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)+"&mirror="+urllib.quote_plus(mirror)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('Delete Search','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%s)'%('plugin://plugin.video.phimtructuyenhd',urllib.quote_plus(url),urllib.quote_plus(name),urllib.quote_plus(str(inum)))))
        contextmenuitems.append(('Edit Search','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%s)'%('plugin://plugin.video.phimtructuyenhd',urllib.quote_plus(url),urllib.quote_plus(name),urllib.quote_plus(str(inum)))))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    if mirror=='f4m':
        u=url
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
mirror=None
iconimage=None
inum=None
edit=None

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
        inum=int(params["inum"])
except:
        pass
try:
        edit = bool(params["edit"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index_nav(url)
elif mode==2:
    index(url)
elif mode==3:
    server(url)
elif mode==4:
    episode(url)
elif mode==5:
    videolink(url)
elif mode==6:
    loadHistory(url)
elif mode==7:
    Search(url)
elif mode==8:
    deleteSearch()
elif mode==9:
    editSearch()
xbmcplugin.endOfDirectory(int(sysarg))