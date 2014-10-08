__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
import SimpleDownloader as downloader


addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
downloader = downloader.SimpleDownloader()
mysettings = xbmcaddon.Addon(id='plugin.video.chiasenhac')
downloadpath = mysettings.getSetting('download_path')
logo ='http://chiasenhac.com/images/logo_csn_300x300.jpg'
homelink = 'http://chiasenhac.com/'
searchlink ='http://search.chiasenhac.com/search.php?s='

while (not os.path.exists(xbmc.translatePath("special://profile/addon_data/"+addonID+"/settings.xml"))):
    addon.openSettings()

def home():
    loadMenu(homelink)
    addDir('Downloaded [COLOR ffffd700]Audios[/COLOR]',downloadpath,11,logo,False,None)
    addDir('Downloaded [COLOR ffffd700]Videos[/COLOR]',downloadpath,11,logo,False,None)
    addDir('[COLOR ffff0000]Search[/COLOR]',searchlink,5,logo,False,None)

def index_search(url):
    link = urllib2.urlopen(url).read()
    newlink = ''.join(link.splitlines()).replace('\t','')
    match = re.compile('<div class="m-left">(.+?)<div class="main-right">').findall(newlink)

    soup = BeautifulSoup(str(match[0]))
    tenbh = soup('div',{'class':'tenbh'})
    gen = soup('span',{'class':'gen'})
    index=0
    for t in tenbh:
        tsoup = BeautifulSoup(str(t))
        ttitle = tsoup('a')[0].contents[0]
        tlink =homelink+tsoup('a')[0]['href']
        tartist = tsoup('p')[1].text
        try:
            info = BeautifulSoup(str(gen[index]))('span')[0].next.next.next.next
            if info==None:
                info = BeautifulSoup(str(gen[index]))('span')[0].next.next.next

            addLink('[COLOR ffff6347]['+str(info)+'][/COLOR] - '+ttitle.encode('utf-8')+' - [COLOR ffffd700]'+tartist.encode('utf-8')+'[/COLOR]',tlink,4,logo)
        except:
            pass
        index +=1

        # addLink(ttitle.encode('utf-8')+' - [COLOR ffffd700]'+tartist.encode('utf-8')+'[/COLOR]',tlink,4,logo)

    matchpages=re.compile('<div class="padding">(.+?)</div>').findall(newlink)
    soupli = BeautifulSoup(str(matchpages[0]))
    lipage = soupli('li')
    for l in lipage:
        try:
            l['class']  #active_page
        except KeyError:
            lsoup = BeautifulSoup(str(l))
            ltitle = lsoup('a')[0].contents[0]
            llink = lsoup('a')[0]['href']
            addDir(ltitle,llink,10,iconimage,False,None)

def medialist(url):
    link = urllib2.urlopen(url).read()
    newlink = ''.join(link.splitlines()).replace('\t','')
    match = re.compile('<div class="m-left">(.+?)<div class="main-right">').findall(newlink)
    soup = BeautifulSoup(str(match[0]))

    gen = soup('div',{'class':'list-r list-1'})
    if len(gen)>0:
        for g in gen:
            gsoup = BeautifulSoup(str(g))
            gtitle = gsoup('a')[0]['title']
            glink =homelink+gsoup('a')[0]['href']
            if str(gsoup('a')[0]).find('img')!=-1:
                gimage = gsoup('img')[0]['src']
            else:
                gimage=logo
            info = gsoup('span',{'style':'color: red'})
            if len(info)>0:
                infotext = info[0].text
                gtitle = '[COLOR ffff6347]['+infotext+'][/COLOR] - '+gtitle
            addLink(gtitle.encode('utf-8'),glink,4,gimage)

    gen = soup('div',{'class':'list-l list-1'})
    if len(gen)>0:
        for g in gen:
                gsoup = BeautifulSoup(str(g))
                gtitle = gsoup('a')[0]['title']
                glink =homelink+gsoup('a')[0]['href']
                if str(gsoup('a')[0]).find('img')!=-1:
                    gimage = gsoup('img')[0]['src']
                else:
                    gimage=logo
                info = gsoup('span',{'style':'color: red'})
                if len(info)>0:
                    infotext = info[0].text
                    gtitle = '[COLOR ffff6347]['+infotext+'][/COLOR] - '+gtitle
                addLink(gtitle.encode('utf-8'),glink,4,gimage)
    else:
        gen = soup('div',{'class':'text2'})
        if len(gen)<=0:
            gen = soup('div',{'class':'gensmall'})
        if len(gen)<=0:
            gen = soup('span',{'class':'gen'})

        for g in gen:
            try:
                gsoup = BeautifulSoup(str(g))
                if len(gsoup('a'))>1:
                    gtitle = gsoup('a')[2]['title']
                    glink =homelink+gsoup('a')[1]['href']
                    if str(gsoup('a')[0]).find('img')!=-1:
                        gimage = gsoup('img')[0]['src']
                    else:
                        gimage=logo
                else:
                    gtitle = gsoup('a')[0]['title']
                    glink =homelink+gsoup('a')[0]['href']
                    if str(gsoup('a')[0]).find('img')!=-1:
                        gimage = gsoup('img')[0]['src']
                    else:
                        gimage=logo

                addLink(gtitle.encode('utf-8'),glink,4,gimage)
            except:pass
    try:
        matchpages=re.compile('<div class="padding">(.+?)</div>').findall(newlink)
        soupli = BeautifulSoup(str(matchpages[0]))
        lipage = soupli('li')
        for l in lipage:
            try:
                l['class']  #active_page
            except KeyError:
                lsoup = BeautifulSoup(str(l))
                ltitle = lsoup('a')[0].contents[0]
                llink =homelink+lsoup('a')[0]['href']
                addDir(ltitle,llink,3,iconimage,False,None)
    except:pass

def medialink(url):
    link = urllib2.urlopen(url).read()
    newlink = ''.join(link.splitlines()).replace('\t','')
    mlink =urllib2.unquote(re.compile('"file": decodeURIComponent\("(.+?)"\),').findall(newlink)[0])
    return mlink

def play(url):
    try:
        if url.find('.m')==-1:
            url = medialink(url)
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        listitem.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    except:pass

def download(url):
    try:
        url=medialink(url)
        filename = str(re.compile('[a-zA-Z0-9-_%]+\.\w+$').findall(url)[0])
        filename= urllib2.unquote(filename).replace(' ','').replace('-','')
        params = {"url": url, "download_path": downloadpath, "Title": '[COLOR ffff0000]'+filename+'[/COLOR]'}
        if os.path.isfile(downloadpath+filename):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('Download message','File exists! re-download?'):
                downloader.download(filename, params)
        else:
            downloader.download(filename, params)
    except:pass

def list_downloaded(url):
    try:
        if str(name).find('Audio')!=-1:
            filetype = '.m4a'
        elif str(name).find('Video')!=-1:
            filetype = '.mp4'
        loadfiles = [a for a in os.listdir(url) if a.endswith(filetype)]
        for a in loadfiles:
            addLink(a,url+a,4,logo)
    except:pass

def delete(url):
    try:
        dialog = xbmcgui.Dialog()
        if dialog.yesno('Delete','Delete File?'):
            os.remove(url)
        xbmc.excutebuiltin('Container Refesh')
    except:pass

def loadHistory(url):
    try:
        addDir('[COLOR ffff0000]Search[/COLOR]',url,6,logo,False,None)
        if mysettings.getSetting('save_search')=='true':
            searches = getStoredSearch()
            if len(searches)!=0:
                searches = eval(searches)
                idn = 0
                for s in searches:
                    addDir(s,url+urllib.quote_plus(s),10,logo,True,idn)
                    idn+=1
    except:pass

def loadMenu(url):
    try:
        menus = eval(getStoredMenu())
        if len(menus)>1:
            for chname,chlink in menus:
                title=chname
                link=chlink
                if title=='[COLOR ffff0000]Search[/COLOR]':
                    addDir(title,link,5,logo,False,None)
                else:
                    addDir(title,link,3,logo,False,None)
        else:
            link = urllib2.urlopen(url).read()
            newlink = ''.join(link.splitlines()).replace('\t','')
            match = re.compile('<div id="myslidemenu"(.+?)<br style="clear:').findall(newlink)
            soup = BeautifulSoup(str(match[0]))
            li_menu = soup('li')
            for i in range(1,len(li_menu)):
                lsoup = BeautifulSoup(str(li_menu[i]))
                ltitle = lsoup('a')[0]['title']
                llink =homelink+lsoup('a')[0]['href']
                updateMenu(ltitle.encode('utf-8'),llink)
                addDir(ltitle.encode('utf-8'),llink,3,logo,False,None)
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
        keyb = xbmc.Keyboard(name, '[COLOR ffff0000]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            newsearch = keyb.getText()
            searches[inum]=newsearch
        saveStoredSearch(searches)
        newsearch=urllib.quote_plus(newsearch)
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Search(searchlink+newsearch)
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR ffff0000]Enter search text[/COLOR]')
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
        index_search(url)
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

def getStoredMenu():
    try:
        menus = mysettings.getSetting('store_menus')
        if len(menus)==0:
            menus="[('[COLOR ffff0000]Search[/COLOR]','http://search.chiasenhac.com/search.php?s=')]"
        return menus
    except:pass

def saveStoredMenu(param):
    try:
        mysettings.setSetting('store_menus',repr(param))
    except:pass

def updateMenu(title,link):
    try:
        menus = getStoredMenu()
        menus=eval(menus)
        if title!='':
            menus_namelink = [(title,link)]
            menus = menus+menus_namelink
            saveStoredMenu(menus)

    except:pass


def addDir(name, url, mode, iconimage,edit,inum):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%d)'%('plugin://plugin.video.chiasenhac',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        contextmenuitems.append(('[COLOR ff00ff00]Edit[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%d)'%('plugin://plugin.video.chiasenhac',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    contextmenuitems = []
    if url.find('http://')!=-1:
        contextmenuitems.append(('[COLOR yellow]Download[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=1)'%('plugin://plugin.video.chiasenhac',urllib.quote_plus(url))))
    else:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=2)'%('plugin://plugin.video.chiasenhac',urllib.quote_plus(url))))
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
    download(url)
elif mode==2:
    delete(url)
elif mode==3:
    medialist(url)
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
elif mode==10:
    index_search(url)
elif mode==11:
    list_downloaded(url)

xbmcplugin.endOfDirectory(int(sysarg))