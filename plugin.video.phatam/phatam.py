import httplib
import urllib,urllib2,re,sys
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
##from BeautifulSoup import BeautifulSoup

pl=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
pl.clear()
homelink ='http://www.phatam.com/video/index.html'
logo='http://www.phatam.com/video/templates/ngodung/images/logo.png'


def home():
    addDir('Chuyen Muc',homelink,3,logo)
    addDir('Tac gia',homelink,4,logo)
    addDir('New Videos',homelink,7,logo)


def playVideo(url):
    try:
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_DVD)
        xbmcPlayer.play(url)

    except:pass

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,mirror):
        if mirror.lower().find("youtube") != -1:
            u="plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(url).replace('?','')
            print u
        elif mirror.lower().find("picasaweb")!=-1:
            u=urllib.unquote_plus(url)##
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name })
        liz.setProperty('mimetype', 'video/x-msvideo')
        pl.add(url, liz)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def Category(url):
    try:
        doc = urllib2.urlopen(url).read()
        soup = BeautifulSoup(doc)
        catedoc = soup.findAll('ul',id='ul_categories')
        soup = BeautifulSoup(str(catedoc[0]))
        catelinks = soup('a')
        for link in catelinks:
            lsoup = BeautifulSoup(str(link))
            lhref = lsoup('a')[0]['href']
            lname = lsoup('a')[0].contents[0]
            addDir(lname.encode("utf-8"),lhref.encode("utf-8"),1,logo)

    except:pass
def new_random(url):
    try:
        doc = urllib2.urlopen(url).read()
        soup = BeautifulSoup(doc)
        item = soup.findAll('div',{'class':'item'})
        for i in item:
            isoup = BeautifulSoup(str(i))
            ilink = BeautifulSoup(str(isoup('a',{'class':'song_name'})[0]))('a')[0]['href']
            iimage = isoup('img')[0]['src']
            ititle = isoup('span',{'class':'artist_name'})[0].contents[0]
            addDir(ititle.encode("utf-8"),ilink.encode("utf-8"),2,iimage.encode("utf-8"))
    except:pass

def authors(url):
    try:
        doc = urllib2.urlopen(url).read()
        soup = BeautifulSoup(doc)
        audoc = soup.findAll('div',{'class':'list_left'})
        soup = BeautifulSoup(str(audoc[0]))
        aulinks = soup('a')
        for link in aulinks:
            ausoup = BeautifulSoup(str(link))
            auhref = ausoup('a')[0]['href']
            auname = ausoup('a')[0].contents[0]
            addDir(auname.encode("utf-8"),auhref.encode("utf-8"),1,logo)
        newlink = ''.join(doc.splitlines()).replace('\t','')
        match = re.compile('<div class="xemthem"><a href="(.+?)">(.+?)</a></div>').findall(newlink)
        for m in match:
            pl,pn = m
            addDir(pn,pl,6,logo)
    except:pass
def moreAuth(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        matchArea = re.compile('<div id="newvideos_results">(.+?)<a href="http://www.phatam.com/video/rss.php">').findall(newlink)
        match = re.compile('"250"><a href="(.+?)" title="(.+?)">').findall(matchArea[0])
        for m in match:
            al,an = m
            addDir(an,al,1,'')
        paging(url,6)

    except:pass
def index2(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        searchArea= re.compile('<div id="newvideos_results">(.+?)<td width="33%"><a href="http://www.phatam.com/video/rss.php').findall(newlink)
        linkarea = re.compile('"10"><a href="(.+?)"><img src="(.+?)" alt="(.+?)" class="tinythumb"').findall(searchArea[0])
        for content in linkarea:
            (vlink, vimage, vtitle)=content
            addDir(vtitle,vlink,2,vimage)
        paging(url,1)
    except:pass

def paging (url,mode):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        matchPageArea = re.compile('<div class="pagination">(.+?)<div id="footer">').findall(newlink)
        matchlinks = re.compile('<a href="(.+?)">(.+?)</a>').findall(matchPageArea[0])
        for match in matchlinks:
            plink,pname = match
            addDir(pname,'http://www.phatam.com/video/'+plink,mode,'')
    except:pass

def getVideos(name,url):
    try:
        content = urllib2.urlopen(url).read()
        newlink = ''.join(content.splitlines()).replace('\t','')
        match = re.compile('<div id="Playerholder">(.+?)</object></div>').findall(newlink)
        matchcode = re.compile('value="http://www.youtube.com/v/(.+?)&hl=en').findall(match[0])
        addLink(name,matchcode[0],5,logo,'youtube')
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
formvar=None
mirrorname=None

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
try:
        mirrorname=urllib.unquote_plus(params["mirrorname"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
        home()
elif mode==1:
        index2(url)
elif mode==2:
        getVideos(name,url)
elif mode==3:
        Category(url)
elif mode==4:
        authors(url)
elif mode==5:
        playVideo(url)
elif mode==6:
        moreAuth(url)
elif mode==7:
        new_random(url)

xbmcplugin.endOfDirectory(int(sysarg))
