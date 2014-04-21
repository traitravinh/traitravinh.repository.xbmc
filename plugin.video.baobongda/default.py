import urllib,urllib2,re,sys
from bs4 import BeautifulSoup
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui

homelink = 'http://m.bongdaplus.vn/'
logo = 'http://m.bongdaplus.vn/style/img/logo.png'

def Home():
    addDir('New Video','http://m.bongdaplus.vn/bongda_video_clip.aspx',1,logo)
    addDir('Bongdaplus TV','http://m.bongdaplus.vn/bongda_video_clip.aspx?aid=3',1,logo)
    addDir('Clip Hai','http://m.bongdaplus.vn/bongda_video_clip.aspx?aid=15',1,logo)



def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        u=url
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty('mimetype', 'video/x-msvideo')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        return ok

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        newspic = soup.findAll('div',{'class':'newspic'})
        li_videos = BeautifulSoup(str(newspic[0])).findAll('li')
        for a in li_videos:
             a_soup = BeautifulSoup(str(a))
             aLink = a_soup('a')[0]['href']
             aImage = a_soup('img')[0]['src']
             aTitle = a_soup('span',{'class':'title'})[0].contents[0]
             addDir(aTitle.encode('utf-8'),homelink+str(aLink),2,homelink+str(aImage))
        pagetab = soup.findAll('div',{'class':'pagetab'})
        pages = BeautifulSoup(str(pagetab[0])).findAll('li')
        for page in pages:
            p_soup = BeautifulSoup(str(page))
            try:
                pLink = p_soup('a')[0]['href']
                pTitle = p_soup('a')[0].contents[0]
                addDir(pTitle,homelink+str(pLink),1,logo)
            except:pass
    except:pass


def playVideo(url):
    try:
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_DVD)
        xbmcPlayer.play(url)
    except:pass

def video_link(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        mediadiv = str(soup('div',{'id':'MainContent_MediaPlayer_itemscript'})[0].contents[0])
        medialink = re.compile("'file': '(.+?)',").findall(mediadiv)[0]
        mediaImage = re.compile("'image': '(.+?)',").findall(mediadiv)[0]
        addLink(name,medialink,3,homelink+str(mediaImage))
    except:pass

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

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

sysarg=str(sys.argv[1])
if mode==None or url==None or len(url)<1:
    Home()
elif mode==1:
    index(url)
elif mode==2:
    video_link(url)
elif mode==3:
    playVideo(url)

xbmcplugin.endOfDirectory(int(sysarg))