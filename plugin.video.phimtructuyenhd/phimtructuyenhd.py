__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup

mysettings = xbmcaddon.Addon(id='plugin.video.phimtructuyenhd')
home = mysettings.getAddonInfo('path')
searchHistory = xbmc.translatePath(os.path.join(home,'history.txt'))
testf4m = xbmc.translatePath(os.path.join(home,'hd.txt'))
searchlink = 'http://m.phimtructuyenhd.com/index.php?name=tim-kiem&str='
home_link = 'http://m.phimtructuyenhd.com'
logo ='http://www.iconki.com/icons/3D/Mimetypes-icons/movie.png'

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        li_a = soup('li',{'data-theme':'a'})
        for li in li_a:
            lilink = BeautifulSoup(str(li))('a')[0]['href']
            lititle = BeautifulSoup(str(li))('a')[0]['title']
            liimage = BeautifulSoup(str(li))('img')[0]['src'].replace('/m.','/') #mobile link is not working

            addDir(lititle.encode('utf-8'),lilink,3,liimage,None,'')
    except:pass

def home():
    try:
        addDir('Search',searchlink,6,logo,None,'')
        link = urllib2.urlopen(home_link).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        navbar = soup('div',{'data-role':'navbar'})
        navtitle = BeautifulSoup(str(navbar[0]))('a')
        for n in range(1,len(navtitle)-1):
            nlink = BeautifulSoup(str(navtitle[n]))('a')[0]['href']
            ntitle = BeautifulSoup(str(navtitle[n]))('a')[0].contents[0]
            addDir(ntitle.encode('utf-8'),nlink,1,logo,None,'')
    except:pass

def index_nav(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        li_a = soup('li',{'data-theme':'a'})

        for li in range(0,len(li_a)):# for 18+ movies, delete -1
            lilink =BeautifulSoup(str(li_a[li]))('a')[0]['href']
            if lilink.find(home_link)==-1:
                lilink = home_link+lilink
            lititle = BeautifulSoup(str(li_a[li]))('a')[0].contents[0]
            addDir(lititle.encode('utf-8'),lilink,2,logo,None,'')

    except:pass

def server(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        svname = soup('span',{'class':'svname'})
        index_num = 0
        for s in svname:
            sname = BeautifulSoup(str(s))('span')[0].contents[0]
            addDir(sname,url,4,iconimage,index_num,sname)
            index_num = index_num+1
    except:pass

def episode(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
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
        soup = BeautifulSoup(link.decode('utf-8'))
        if mirror=='YouTube:':
            source =re.compile('http://www.youtube.com/embed/(.+?)\?').findall(str(soup('iframe')[0]['src']))[0]
        else:
            source = soup('source')[0]['src']
        PlayVideo(source,mirror)
    except:
        PlayVideo(url,'')

def PlayVideo(url,mirror):
    try:
        if mirror =='YouTube:':
            vUrl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(url).replace('?','')
        elif mirror == 'Dailymotion:':
            vUrl = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(url).replace('?','')
        elif mirror =='Picasa:':
            vUrl = url
        else:
            vUrl=url
        if mysettings.getSetting('descriptions')=='true':
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=str(vUrl)))
        else:
            listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
            xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(vUrl,listitem)
    except:pass


def SearchFirst(url):
    try:
        videofile = open(testf4m,'r')
        for text in videofile:
            videopart = re.compile('<media bitrate="1000" url="mp4:(.+?)" height="480"').findall(text)
        hist = open(searchHistory)
        addDir('Search',searchlink,7,logo,None,'')
        for text in hist:
            addDir(text,(searchlink+text).replace(' ','+').rstrip(),2,logo,None,'') #+'/page-1.html',6,logo)
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

def addDir(name, url, mode, iconimage, inum,mirror):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)+"&mirror="+urllib.quote_plus(mirror)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    if mirror=='f4m':
        u=url
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
        inum=int(params["inum"])
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
    SearchFirst(url)
elif mode==7:
    Search(url)

xbmcplugin.endOfDirectory(int(sysarg))