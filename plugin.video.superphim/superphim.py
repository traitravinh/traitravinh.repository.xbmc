__author__ = 'traitravinh'

import urllib, urllib2, re, StringIO, os, sys, base64, gzip, string
from bs4 import BeautifulSoup
import xbmcaddon,xbmcplugin,xbmcgui

root_link = 'http://www.superphim.com'
mob_root = 'http://www.phimmobile.com'
mob_link = 'http://www.phimmobile.com/index.php?action=play&id='
searchlink = 'http://www.superphim.com/search.php?q='
mysettings = xbmcaddon.Addon(id='plugin.video.superphim')
home = mysettings.getAddonInfo('path')
logo = xbmc.translatePath(os.path.join(home, 'icon.png'))
searchHistory = xbmc.translatePath(os.path.join(home,'history.txt'))

def Home():
    addDir('Search',searchlink,5,logo)
    addDir('Phim Moi Nhat','http://www.superphim.com/phim-moi-update.html',1,logo)
    addDir('Phim HK & TQ','http://www.superphim.com/Phim-Hong-Kong-movies-72-page-1.html',1,logo)
    addDir('Phim Han Quoc','http://www.superphim.com/Phim-Han-Quoc-movies-107-page-1.html',1,logo)
    addDir('Phim Vietnam','http://www.superphim.com/Phim-Viet-Nam-movies-141-page-1.html',1,logo)
    addDir('Hai Kich','http://www.superphim.com/Hai-Kich-Viet-Nam-movies-83-page-1.html',1,logo)

def SearchFirst(url):
    try:
        hist = open(searchHistory)
        addDir('Search',searchlink,6,logo)
        for text in hist:
            addDir(text,(searchlink+text).replace(' ','+').rstrip(),1,logo) #+'/page-1.html',6,logo)
    except:pass
def Search(url):
    try:
        if url.find('html')!=-1:
            url =url
        else:
            keyb = xbmc.Keyboard('', 'Enter search text')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    searchText = urllib.quote_plus(keyb.getText())
            url = searchlink+ searchText.replace(' ','+').rstrip()
            if searchText!='':
                with open(searchHistory,'a') as file:
                    file.write('\n'+searchText.replace('+',' '))
        index(url)
    except: pass


def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        title_soup = soup.findAll('div', {'id': 'makers'})
        for t in title_soup:
            tSoup = BeautifulSoup(str(t))
            tLink = (tSoup('a')[0]['href']).lstrip('.')
            tTitle = tSoup('strong')[0].contents[0]
            tImage = (tSoup('img')[0]['src']).replace(' ', '%20')
            addDir(tTitle.encode('utf-8'),root_link+tLink,2,root_link + tImage)
        page_soup = soup.findAll('a',{'class':'pagelink'})
        for p in page_soup:
            pSoup = BeautifulSoup(str(p))
            pLink = (pSoup('a')[0]['href']).lstrip('.')
            pTitle = pSoup('a')[0].contents[0]
            addDir(pTitle,root_link + pLink,1,logo)
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
                addDir(mName,url,3,iconimage)
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

def play(url,mirror):
    try:
        if mirror == 'dailymotion':
            videoId = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(url).replace('?','')
        elif mirror == 'youtube':
            videoId = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(url).replace('?','')
        if mysettings.getSetting('play')=='true':
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=videoId))
        else:
            listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
            xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(videoId,listitem)
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

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
    SearchFirst(url)
elif mode==6:
    Search(url)

xbmcplugin.endOfDirectory(int(sysarg))