import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
import requests
from bs4 import BeautifulSoup


homelink = 'http://m.vkool.net'
addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
mysettings = xbmcaddon.Addon(id='plugin.video.vkool')
icon = addon.getAddonInfo('icon')
mysettings = xbmcaddon.Addon(id='plugin.video.vkool')
home = mysettings.getAddonInfo('path')
logo = addon.getAddonInfo('icon')

searchlink = 'http://m.vkool.net/search/'

while (not os.path.exists(xbmc.translatePath("special://profile/addon_data/"+addonID+"/settings.xml"))):
    addon.openSettings()

def GetContent(url):
    headers = {'User-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'}
    response = requests.get(url,headers=headers)
    return response.text

def home():
    addDir('[COLOR ffffd700]Search[/COLOR]',searchlink,5,logo,False,None)
    link = GetContent(homelink)
    soup = BeautifulSoup(link)
    slists = soup('ul',{'class':'slist'})

    for s in slists:
        sli = BeautifulSoup(str(s))('li')
        for l in sli:
            lsoup = BeautifulSoup(str(l))
            llink = lsoup('a')[0]['href']
            lname = lsoup('a')[0].contents[0]
            addDir(lname.encode('utf-8'), llink, 1, logo, False, None)

def category(url):
    link = GetContent(url)
    soup = BeautifulSoup(link)
    content_items = soup('a',{'class':'content-items'})
    for citem in content_items:
        cisoup = BeautifulSoup(str(citem))
        cname = cisoup('h3')[0].next
        clink = cisoup('a')[0]['href']
        cimage = cisoup('img')[0]['src']
        # cinfo = cisoup('li')[3].next
        addDir(cname.encode('utf-8'), clink.encode('utf-8'), 2, cimage, False, None)
    try:
        pagination = soup('div',{'class':'pagination'})
        page = BeautifulSoup(str(pagination[0]))('a')
        for p in page:
            psoup = BeautifulSoup(str(p))
            try:
                pactive=psoup('a',{'class':'active'})[0]
            except:
                ptitle = psoup('a')[0].contents[0]
                plink = psoup('a')[0]['href']
                addDir(ptitle.encode('utf-8'), plink.encode('utf-8'), 1, logo, False, None)
    except:pass

def serverlist(url):
    link = GetContent(url)
    soup = BeautifulSoup(link)
    serverlink = BeautifulSoup(str(soup('a',{'class':'click-watch button'})))('a')[0]['href']

    newlink = GetContent(serverlink)
    nsoup = BeautifulSoup(newlink)
    server_item = nsoup('div', {'class':'server_item'})
    inum = 0
    for si in range(0, len(server_item)):
        siname = BeautifulSoup(str(server_item[si]))('strong')[0].text
        addDir(siname.encode('utf-8'), serverlink, 3, iconimage,False, inum)
        inum += 1


def episode(url):
    link = GetContent(url)
    soup = BeautifulSoup(link)
    server_item = soup('div', {'class':'server_item'})[inum]
    span = BeautifulSoup(str(server_item))('span')
    for s in span:
        ssoup = BeautifulSoup(str(s))
        try:
            s['class']
            sname = '1'
            slink = ssoup('a')[0]['href']
            addLink(sname, slink, 4, iconimage)
        except KeyError:
            slink = ssoup('a')[0]['href']
            sname = ssoup('a')[0].contents[0]
            addLink(sname.encode('utf-8'), slink, 4, iconimage)

def medialink(url):
    link = GetContent(url)
    soup = BeautifulSoup(link)
    print soup
    if link.find('youtube.com')!=-1:
        vlink = soup('iframe')[1]['src']
    elif link.find('<div id="player">')!=-1:
        vsources = soup('source')
        vlink = BeautifulSoup(str(vsources[len(vsources)-1]))('source')[0]['src']
    return vlink

def play(url):
    VideoUrl = medialink(url)
    if VideoUrl.find('youtube')!=-1:
        match = re.compile('&.+').findall(VideoUrl)
        if len(match)>0:
            VideoUrl= VideoUrl.replace(match[0],'')
        idregex = r'https?://www.youtube.com/watch\?v='+r'(.+)'
        VideoUrl = re.compile(idregex).findall(VideoUrl)[0]

        VideoUrl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(VideoUrl).replace('?','')

    # listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=VideoUrl))


######## SEARCH ###############################################################################################
def loadHistory(url):
    try:
        addDir('[COLOR ffffd700]Search[/COLOR]',url,6,logo,False,None)
        if mysettings.getSetting('save_search')=='true':
            searches = getStoredSearch()
            if len(searches)!=0:
                searches = eval(searches)
                idn = 0
                for s in searches:
                    addDir(s,url+urllib.quote_plus(s)+'.html',1,logo,True,idn)
                    idn+=1
    except:pass

def deleteSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        del(searches[inum])
        saveStoredSearch(searches)
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
        newsearch=urllib.quote_plus(newsearch)+'.html'
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Search(searchlink+newsearch)
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR ffffd700]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            url = searchlink+ searchText+'.html'
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
        if url.find('.html')!=-1:
            url = url.rstrip()
        else:
            url = getUserInput()
        xbmc.executebuiltin("XBMC.Container.Refresh")
        category(url)
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
######## END SEARCH #########################################################################################

def addDir(name, url, mode, iconimage,edit, inum):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name })
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%d)'%('plugin://plugin.video.vkool',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        contextmenuitems.append(('[COLOR ff00ff00]Edit[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%d)'%('plugin://plugin.video.vkool',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
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
    category(url)
elif mode==2:
    serverlist(url)
elif mode==3:
    episode(url)
elif mode==4:
    play(url)
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