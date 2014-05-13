__author__ = 'traitravinh'

import urllib, urllib2, re, StringIO, os, sys, base64, gzip, string
from bs4 import BeautifulSoup
import xbmcaddon,xbmcplugin,xbmcgui
import urlresolver
import SimpleDownloader as downloader


downloader = downloader.SimpleDownloader()

root_link = 'http://www.superphim.com'
mob_root = 'http://www.phimmobile.com'
mob_link = 'http://www.phimmobile.com/index.php?action=play&id='
searchlink = 'http://www.superphim.com/search.php?q='
mysettings = xbmcaddon.Addon(id='plugin.video.superphim')
downloadpath = mysettings.getSetting('download_path')
home = mysettings.getAddonInfo('path')
logo = xbmc.translatePath(os.path.join(home, 'icon.png'))
# downloadpath = xbmc.translatePath(os.path.join(home,'/download'))

def Home():
    addDir('[COLOR FF67cc33]Search[/COLOR]',searchlink,5,logo,False)
    addDir('Phim Moi Nhat','http://www.superphim.com/phim-moi-update.html',1,logo,False)
    addDir('Phim HK & TQ','http://www.superphim.com/Phim-Hong-Kong-movies-72-page-1.html',1,logo,False)
    addDir('Phim Han Quoc','http://www.superphim.com/Phim-Han-Quoc-movies-107-page-1.html',1,logo,False)
    addDir('Phim Vietnam','http://www.superphim.com/Phim-Viet-Nam-movies-141-page-1.html',1,logo,False)
    addDir('Hai Kich','http://www.superphim.com/Hai-Kich-Viet-Nam-movies-83-page-1.html',1,logo,False)

def loadHistory(url):
    try:
        addDir('[COLOR FF67cc33]Search[/COLOR]',url,6,logo,False)
        searches = getStoredSearch()
        if len(searches)!=0:
            searches = eval(searches)
            for s in searches:
                addDir(s,url+urllib.quote_plus(s),1,logo,True)
    except:pass

def deleteSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        for i in range(0,len(searches)):
            if searches[i]==name:
                del(searches[i])
                break
        saveStoredSearch(searches)
        # xbmc.executebuiltin('Container.Refresh')
    except StopIteration:
        pass

def editSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        keyb = xbmc.Keyboard(name, '[COLOR yellow]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            newsearch = keyb.getText()
            for i in range(0,len(searches)):
                if searches[i]==name:
                    searches[i]=newsearch
        saveStoredSearch(searches)
        newsearch=urllib.quote_plus(newsearch)
        Search(searchlink+newsearch)
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR yellow]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            url = searchlink+ searchText
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


def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        title_soup = soup.findAll('div', {'id': 'makers'})
        for t in title_soup:
            tSoup = BeautifulSoup(str(t))
            tLink = (tSoup('a')[0]['href']).lstrip('.')
            tTitle = tSoup('strong')[0].contents[0]
            tImage = urllib.quote(tSoup('img')[0]['src'],safe="%/:=&?~#+!$,;'@()*[]")
            addDir(tTitle.encode('utf-8'),root_link+tLink,2,root_link + tImage,False)
        page_soup = soup.findAll('a',{'class':'pagelink'})
        for p in page_soup:
            pSoup = BeautifulSoup(str(p))
            pLink = (pSoup('a')[0]['href']).lstrip('.')
            pTitle = pSoup('a')[0].contents[0]
            addDir(pTitle,root_link + pLink,1,logo,False)
    except:
        pass


def mirrors(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        mirror_soup = soup.findAll('td', {'class': 'movieepisode'})
        for m in mirror_soup:
            try:
                m_soup = BeautifulSoup(str(m))
                mName = m_soup('strong')[0].contents[0]
                addDir(mName,url,3,iconimage,False)
            except:
                pass

    except:
        pass
def episodes(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        mirror_soup = soup.findAll('td', {'class': 'movieepisode'})
        for m in mirror_soup:
            m_soup = BeautifulSoup(str(m))
            mr = (str(m_soup('strong')[0].contents[0])).strip()
            if name.strip().lower().find(mr.lower()) != -1:
                ep_soup = m_soup.findAll('a')
                for e in ep_soup:
                    e_soup = BeautifulSoup(str(e))
                    eLink = (e_soup('a')[0]['href']).lstrip('.')
                    eTitle = e_soup('b')[0].contents[0]
                    eT = str(eTitle)
                    eLink_ID = re.compile('-[0-9]*\.html').findall(eLink)
                    finalLink = mob_link+(eLink_ID[0]).strip('-.html')
                    addLink(eT.decode('utf-8'),finalLink,4,name.lower(),iconimage)
                break
    except:
        pass

def videoID(url):
    VideoMobileLink = GetVideoMobileLink(url)
    newLink = GetDirVideoUrl(VideoMobileLink,url)
    if newLink.find('dailymotion') > -1:
        match = re.compile('http://www.dailymotion.com/embed/video/(.+?)\?auto').findall(newLink)
        mirror='dailymotion'
    elif newLink.find('youtube') > -1:
        match = re.compile('http://www.youtube.com/embed/(.+?)\?auto').findall(newLink)
        mirror = 'youtube'
    return match[0], mirror

def loadVideos(url,mirror):
    try:
        nUrl, mirrorName = videoID(url)
        play(nUrl, mirrorName)
    except:pass

def getHostedMediaFile(url,mirror):
    if mirror == 'dailymotion':
        hostedmedia = urlresolver.HostedMediaFile('http://www.dailymotion.com/embed/video/%s'%(url))
        videoId=hostedmedia.resolve()
        # videoId = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(url).replace('?','')
    elif mirror == 'youtube':
        hostedmedia = urlresolver.HostedMediaFile('http://youtube.com/watch?v=%s'%(url))
        videoId = hostedmedia.resolve()
    return videoId
def makeDir():
    try:
        dialog = xbmcgui.Dialog()
        if dialog.yesno('New Folder','Download to new folder?'):
            keyb = xbmc.Keyboard('', 'Enter search text')
            keyb.doModal()
            if (keyb.isConfirmed()):
                newfolder = urllib.quote_plus(keyb.getText())
                mypath = xbmc.translatePath(os.path.join(downloadpath,newfolder))
                if not os.path.isdir(mypath):
                   os.makedirs(mypath)
        else:
            mypath=''
        return mypath
    except:pass

def download():
    nUrl, mirrorName = videoID(url)
    videoId = getHostedMediaFile(nUrl,mirrorName)
    mypath = makeDir()
    if mypath!='':
        downloadpath=mypath
    params = { "url": videoId, "download_path": downloadpath, "Title": name }
    downloader.download(str(name)+".mp4", params)

def play(url,mirror):
    try:
        videoId = getHostedMediaFile(url,mirror)
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        listitem.setPath(videoId)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    except:pass

def GetContent(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-agent','Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    response = urllib2.urlopen(req).read()
    return response

def GetVideoMobileLink(url):
    link = GetContent(url)
    soup = BeautifulSoup(link.decode('utf-8'))
    iFrame_soup = soup.findAll('td',{'colspan':'4'})
    full_link=''
    if len(iFrame_soup)>1:
        iSource = (BeautifulSoup(str((BeautifulSoup(str(iFrame_soup[1]))).findAll('iframe')[0])))('iframe')[0]['src']
        full_link = mob_root+iSource
    return full_link

def GetDirVideoUrl(url,referr):
    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        http_error_301 = http_error_303 = http_error_307 = http_error_302
    redirhndler = MyHTTPRedirectHandler()
    opener = urllib2.build_opener(redirhndler)
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',referr),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','www.phimmobile.com')]
    usock = opener.open(url)
    return redirhndler.video_url

def GetContentMob(url):
    opener = urllib2.build_opener()
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',"http://www.phimmobile.com/index.php"),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','www.phimmobile.com')]
    uSock = opener.open(url)
    if uSock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(uSock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = uSock.read()
    uSock.close()
    return response

def addDir(name,url,mode,iconimage,edit):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR blue]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s)'%('plugin://plugin.video.superphim',urllib.quote_plus(url),urllib.quote_plus(name))))
        contextmenuitems.append(('[COLOR yellow]Edit[/COLOR] [COLOR blue]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s)'%('plugin://plugin.video.superphim',urllib.quote_plus(url),urllib.quote_plus(name))))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    contextmenuitems=[]
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    contextmenuitems.append(('Download','XBMC.Container.Update(%s?url=%s&mode=10&mirror=%s&name=%s)'%('plugin://plugin.video.superphim',urllib.quote_plus(url),urllib.quote_plus(mirror),urllib.quote_plus(name))))

    liz.addContextMenuItems(contextmenuitems,replaceItems=False)
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

sysarg=str(sys.argv[1])
if mode==None or url==None or len(url)<1:
    Home()
elif mode==1:
    index(url)
elif mode==2:
    mirrors(url)
elif mode==3:
    episodes(url)
elif mode==4:
    loadVideos(url,mirror)
elif mode==5:
    loadHistory(url)
elif mode==6:
    Search(url)
elif mode==7:
    download(url)
elif mode==8:
    deleteSearch()
elif mode==9:
    editSearch()
elif mode==10:
    download()


xbmcplugin.endOfDirectory(int(sysarg))


#test
# index('http://www.superphim.com/Phim-Hong-Kong-movies-72-page-1.html')
# mirrors('http://www.superphim.com/vua-phim-truong-the-movie-tycoon-online-5692.html')
# episodes('http://www.superphim.com/vua-phim-truong-the-movie-tycoon-online-5692.html', 'Mirror 1:')
# GetContent('http://www.phimmobile.com/index.php?action=play&id=832745')
# GetContent('http://www.phimmobile.com/index.php?action=play&id=832898')
# GetVideoMobileLink('http://www.phimmobile.com/index.php?action=play&id=832898')
# GetVideoMobileLink('http://www.phimmobile.com/index.php?action=play&id=832745')
# videoID('http://www.phimmobile.com/index.php?action=play&id=832898')
# videoID('http://www.phimmobile.com/index.php?action=play&id=832745')