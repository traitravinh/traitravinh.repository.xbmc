import urllib, urllib2, re, os, sys
from bs4 import BeautifulSoup
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui

homelink = 'http://ourmatch.net'
playwire_base_url='http://cdn.playwire.com/'
mysettings = xbmcaddon.Addon(id='plugin.video.ourmatch_net')
home = mysettings.getAddonInfo('path')
logo = 'http://www.ourmatch.net/wp-content/themes/OurMatchV2/images/logo.png'


def home():
    try:
        link = urllib2.urlopen(homelink).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        main_nav = soup('div',{'id':'main-nav'})
        li = BeautifulSoup(str(main_nav[0]))('li')
        for l in li:
            lilink = BeautifulSoup(str(l))('a')[0]['href']
            lititle = BeautifulSoup(str(l))('a')[0].contents[0]
            addDir(lititle,lilink,1,logo)
    except:pass

def index(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        thumb = soup('div',{'class':'thumb'})
        for t in thumb:
            tlink = BeautifulSoup(str(t))('a')[0]['href']
            ttitle = BeautifulSoup(str(t))('a')[0]['title']
            timage = BeautifulSoup(str(t))('img')[0]['src']
            addDir(ttitle,tlink,2,timage)
        wp_pagenavi = soup('div',{'class':'wp-pagenavi'})
        page_larger = BeautifulSoup(str(wp_pagenavi[0]))('a')
        for p in page_larger:
            plink = BeautifulSoup(str(p))('a')[0]['href']
            ptitle = BeautifulSoup(str(p))('a')[0].contents[0]
            addDir(ptitle.encode('utf-8'),plink,1,logo)
    except:pass

def videoLink(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        entry_content = soup('div',{'class':'entry-content rich-content'})
        p_tag = BeautifulSoup(str(entry_content[0]))('p')
        for p in p_tag:
            ptext = BeautifulSoup(str(p)).p.contents[0]
            ptext = ptext.encode('utf-8')
            pscritp =retrievVideoLink(str(BeautifulSoup(str(p)).p.next.next.next.next))
            addLink(ptext,pscritp,3,'',iconimage)
    except:pass

def retrievVideoLink(url):
    try:
        publisherId = re.compile('data-publisher-id="(.+?)" data-video-id').findall(url)
        videoId = re.compile('data-video-id="(.+?)"').findall(url)
        f4m_link = playwire_base_url+'v2/' + str(publisherId[0])+'/config/'+str(videoId[0])+'.json'
        link = urllib2.urlopen(f4m_link).read()
        f4m_src = re.compile('"src":"(.+?)"|\'').findall(str(link))
        if str(f4m_src[0]).find('.f4m')!=-1:
            nlink = urllib2.urlopen(f4m_src[0]).read()
            vCode = re.compile('mp4:(.+?)" ').findall(str(nlink))
            if len(vCode)>1:
                sCode = vCode[1]
            else:
                sCode=vCode[0]
            real_link = playwire_base_url+publisherId[0]+'/'+str(sCode)
        elif str(f4m_src[0]).find('rtmp://streaming')!=-1:
            real_link = str(f4m_src[0]).replace('rtmp://streaming','http://cdn').replace('mp4:','')

        return real_link
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