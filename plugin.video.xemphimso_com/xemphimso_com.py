import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup

root_link = 'http://xemphimso.com'
logo = 'http://xemphimso.com/quangcao/images/logo.png'
searchlink = 'http://xemphimso.com/tim-kiem/'
addon = xbmcaddon.Addon()
mysettings = xbmcaddon.Addon(id='plugin.video.xemphimso_com')
home = mysettings.getAddonInfo('path')
searchHistory = xbmc.translatePath(os.path.join(home,'history.txt'))
headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'}

# def test(url):
#     resolver = urlresolver.UrlResolver
#     videolinks = urlresolver.UrlResolver.get_url(resolver,'http://cdn.playwire.com/',id)
#     print videolinks

def home():
    try:
        # addDir('test','17003',8,logo)
        addDir('Search',searchlink,5,logo)
        req = urllib2.Request(root_link, None, headers)
        link = urllib2.urlopen(req).read()
        soup = BeautifulSoup(''.join(link.decode('utf-8')))
        glist_soup = soup('div',{'class':'glist'})
        for glist in glist_soup:
            gl_soup = BeautifulSoup(str(glist))
            stitle = gl_soup('h3')[0].contents[0]
            addDir(stitle.encode('utf-8'),'',None,'')
            slist_soup = BeautifulSoup(str(gl_soup))
            ul_slist = slist_soup('ul',{'class':'slist'})
            for ul in ul_slist:
                ul_soup = BeautifulSoup(str(ul))
                li_list = ul_soup('li')
                for li in li_list:
                    asoup = BeautifulSoup(str(li))
                    alink = asoup('a')[0]['href']
                    atitle = asoup('a')[0]['title']
                    addDir('    '+atitle.encode('utf-8'),alink,1,logo)
    except:pass

def index(url):
    try:
        req = urllib2.Request(url, None, headers)
        link = urllib2.urlopen(req).read()
        soup = BeautifulSoup(''.join(link.decode('utf-8')))
        content_items = soup('div',{'class':'content-items'})
        for item in content_items:
            item_soup = BeautifulSoup(str(item))
            iTitle = item_soup('h3')[0].contents[0]
            iLink = item_soup('a')[0]['href']
            iImage = item_soup('img')[0]['src']
            addDir(iTitle.encode('utf-8'),iLink,2,iImage)
        # print soup.prettify()
        pagination_list = soup('div',{'class':'pagination_list'})
        pagelink = BeautifulSoup(str(pagination_list[0]))('a',{'class':'pagelink'})
        for page in pagelink:
            page_soup = BeautifulSoup(str(page))
            pLink = page_soup('a')[0]['href']
            pTitle = page_soup('a')[0].contents[0]
            addDir(pTitle.encode('utf-8'),pLink,1,logo)
    except:pass

def serverlist(url):
    try:
        req = urllib2.Request(url, None, headers)
        link = urllib2.urlopen(req).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        nurl = BeautifulSoup(str(soup('a',{'class':'btn'})[0]))('a')[0]['href']
        newlink =urllib2.urlopen(urllib2.Request(nurl, None, headers)).read()
        newsoup = BeautifulSoup(newlink.decode('utf-8'))
        mirror_soup = newsoup('div',{'class':'listserver'})
        for m in mirror_soup:
            mName = BeautifulSoup(str(m))('span')[0].contents[0]
            addDir(mName,nurl,3,iconimage)
    except:pass

def serverSelected(url):
    try:
        server = name
        req = urllib2.Request(url, None, headers)
        link = urllib2.urlopen(req).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        mirror_soup = soup('div',{'class':'listserver'})
        for m in mirror_soup:
            if str(m).find(server)!=-1:
                part_soup = BeautifulSoup(str(m)).findAll('a')
                for p in part_soup:
                    ptSoup = BeautifulSoup(str(p))
                    ptLink = ptSoup('a')[0]['href']
                    # ptTitle = ptSoup('a')[0].contents[0].encode('utf-8')
                    ptTitle = ptSoup.a.next.string
                    print 'HERE------------------------------------>'
                    print ptLink
                    addLink(ptTitle,ptLink,4,server,iconimage)
    except:pass

def videoUrl(url):
    try:
        req = urllib2.Request(url, None, headers)
        link = urllib2.urlopen(req).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        if link.find('youtube.com')!=-1:
            vCode = re.compile('http://youtube.com/embed/(.+?)\?api').findall(link)[0]
            server = 'youtube'
        elif link.find('dailymotion.com')!=-1:
            vCode = re.compile("http://www.dailymotion.com/video/(.+?)' ").findall(link)[0]
            server='dailymotion'
        else:
            vCode_soup = soup.findAll('video')
            vCode = BeautifulSoup(str(vCode_soup[0]))('video')[0]['src']
            server = 'picasaweb'

        PlayVideo(vCode,server)
    except:pass

def PlayVideo(url,server):
    try:
        if server =='youtube':
            vUrl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(url).replace('?','')
        elif server == 'dailymotion':
            vUrl = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(url).replace('?','')
        elif server =='picasaweb':
            vUrl = url
        else:
            vUrl=url
        if mysettings.getSetting('descriptions')=='true':
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=vUrl))
        else:
            listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
            xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(vUrl,listitem)
    except:pass



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
    serverlist(url)
elif mode==3:
    serverSelected(url)
elif mode==4:
    videoUrl(url)
elif mode==5:
    SearchFirst(url)
elif mode==6:
    Search(url)
elif mode==7:
    PlayVideo(url,server)
# elif mode==8:
#     test(url)

xbmcplugin.endOfDirectory(int(sysarg))