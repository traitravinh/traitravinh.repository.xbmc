# __author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui,requests
from bs4 import BeautifulSoup
import SimpleDownloader as downloader
import xbmcvfs

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
mysettings = xbmcaddon.Addon(id='plugin.video.movihd')
homelink = 'http://movihd.net'
logo = 'http://movihd.net/img/logo.png'
downloader = downloader.SimpleDownloader()
downloadpath = mysettings.getSetting('download_path')
home = mysettings.getAddonInfo('path')

addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID).decode('utf-8')
libraryFolder = os.path.join(addonUserDataFolder, "library")
libraryFolderMovies = os.path.join(libraryFolder, "Movies")
libraryFolderTV = os.path.join(libraryFolder, "TV")
custLibFolder = mysettings.getSetting('library_path')
custLibTvFolder = mysettings.getSetting('libraryTV_path')

if not os.path.exists(os.path.join(addonUserDataFolder, "settings.xml")):
    addon.openSettings()
if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)
if not os.path.isdir(libraryFolder):
    os.mkdir(libraryFolder)
if not os.path.isdir(libraryFolderMovies):
    os.mkdir(libraryFolderMovies)
if not os.path.isdir(libraryFolderTV):
    os.mkdir(libraryFolderTV)

def GetContent(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-agent','Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
    response = urllib2.urlopen(req).read()
    return response

def home():
    link = requests.get(homelink)
    soup = BeautifulSoup(link.text)
    catli = soup('li')
    for li in range(0,34):
        lisoup = BeautifulSoup(str(catli[li]))
        lititle = str(lisoup('a')[0].contents[0].encode('utf-8'))
        if lititle==' ':
            lititle = lisoup('a')[0].next.next.next.encode('utf-8')
        lilink = homelink+lisoup('a')[0]['href']
        if lititle.find('PHIM B')!=-1:
            addDir(lititle,lilink,1,logo,False,1,'')
        else:
            addDir(lititle,lilink,1,logo,False,None,'')

def index(url):
    link = requests.get(url)
    soup = BeautifulSoup(link.text)
    blockbase = soup('div',{'class':'block-base movie'})
    for b in blockbase:
        bsoup = BeautifulSoup(str(b))
        btitle = str(bsoup('a')[0]['title'].encode('utf-8'))
        blink = homelink+bsoup('a')[0]['href']
        bimage = homelink+bsoup('img')[0]['src']
        if inum==1:
            addDir(btitle,blink,4,bimage,True,None,btitle)
        else:
            addLink(btitle,blink,3,bimage,btitle)

    pagination = BeautifulSoup(str(soup('div',{'class':'action'})[0]))('a')
    for p in pagination:
        psoup = BeautifulSoup(str(p))
        plink = homelink+psoup('a')[0]['href']
        ptitle = psoup('a')[0].contents[0]

        addDir(ptitle,plink,1,iconimage,False,inum,'')

def episodes(url):
    link = requests.get(url)
    soup = BeautifulSoup(link.text)
    episodes =BeautifulSoup(str(soup('div',{'class':'action left'})[0]))('a')
    for e in episodes:
        esoup = BeautifulSoup(str(e))
        elink =homelink+'/playlist/'+re.compile("javascript:PlayFilm\('(.+?)'\)").findall(esoup('a')[0]['href'])[0]+'_server-2.xml'
        etitle = str(esoup('a')[0].contents[0].encode('utf-8'))
        addLink(etitle,elink,3,iconimage,gname)

def videolinks(url):
    if url.find('xml')!=-1:
        xml_link=url
    else:
        xml_link =homelink+'/playlist/'+re.compile('http://movihd.net/phim/(.+?)_').findall(url)[0]+'_server-2.xml'
    link = requests.get(xml_link)
    soup = BeautifulSoup(link.text)
    media = homelink+soup('item')[0].next.next.next.next['url']
    return media

def play(url,name):
    VideoUrl = videolinks(url)
    listitem = xbmcgui.ListItem(name, path=VideoUrl)
    listitem.setInfo( type="Video", infoLabels={ "Title": name })
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=VideoUrl))

def addToLibrary(url):
    if mysettings.getSetting('cust_Lib_path')=='true':
        newlibraryFolderMovies = custLibFolder
    else:
        newlibraryFolderMovies = libraryFolderMovies
    movieFolderName = (''.join(c for c in unicode(gname, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
    newMovieFolderName=''
    finalName=''
    keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter Title[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
        newMovieFolderName=keyb.getText()
    if newMovieFolderName !='':
        dir = os.path.join(newlibraryFolderMovies, newMovieFolderName)
        finalName=newMovieFolderName
    else:
        dir = os.path.join(newlibraryFolderMovies, movieFolderName)
        finalName=movieFolderName

    if not os.path.isdir(dir):
        xbmcvfs.mkdir(dir)
        fh = xbmcvfs.File(os.path.join(dir, finalName+".strm"), 'w')
        fh.write('plugin://'+addonID+'/?mode=3&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(finalName))
        fh.close()
        # xbmc.executebuiltin('UpdateLibrary(video)')

def addSeasonToLibrary(url):
    if mysettings.getSetting('cust_LibTV_path')=='true':
        newlibraryFolderMovies = custLibTvFolder
    else:
        newlibraryFolderMovies = libraryFolderTV
    movieFolderName = (''.join(c for c in unicode(gname, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
    newMovieFolderName=''
    finalName=''
    keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter Title[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
        newMovieFolderName=keyb.getText()
    if newMovieFolderName !='':
        dir = os.path.join(newlibraryFolderMovies, newMovieFolderName)
        finalName=newMovieFolderName
    else:
        dir = os.path.join(newlibraryFolderMovies, movieFolderName)
        finalName=movieFolderName

    keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter Season[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
        seasonnum=keyb.getText()
    link = requests.get(url)
    soup = BeautifulSoup(link.text)
    episodes =BeautifulSoup(str(soup('div',{'class':'action left'})[0]))('a')

    if not os.path.isdir(dir):
        xbmcvfs.mkdir(dir)
        for e in episodes:
            esoup = BeautifulSoup(str(e))
            elink =homelink+'/playlist/'+re.compile("javascript:PlayFilm\('(.+?)'\)").findall(esoup('a')[0]['href'])[0]+'_server-2.xml'
            etitle = str(esoup('a')[0].contents[0].encode('utf-8'))
            if len(etitle)==1:
                epnum = '0'+etitle
            else:
                epnum=etitle
            epname = ''.join(["S", seasonnum, "E", epnum, ' - ', finalName])
            fh = xbmcvfs.File(os.path.join(dir, epname+".strm"), 'w')
            fh.write('plugin://'+addonID+'/?mode=3&url='+urllib.quote_plus(elink)+'&name='+urllib.quote_plus(''.join(["[", etitle.encode('utf-8'), "] ", gname])))
            fh.close()
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno('TV Show Exists','Update Files?'):
            for e in episodes:
                esoup = BeautifulSoup(str(e))
                elink =homelink+'/playlist/'+re.compile("javascript:PlayFilm\('(.+?)'\)").findall(esoup('a')[0]['href'])[0]+'_server-2.xml'
                etitle = str(esoup('a')[0].contents[0].encode('utf-8'))
                if len(etitle)==1:
                    epnum = '0'+etitle
                else:
                    epnum=etitle
                epname = ''.join(["S", seasonnum, "E", epnum, ' - ', finalName])
                fh = xbmcvfs.File(os.path.join(dir, epname+".strm"), 'w')
                fh.write('plugin://'+addonID+'/?mode=3&url='+urllib.quote_plus(elink)+'&name='+urllib.quote_plus(''.join(["[", etitle.encode('utf-8'), "] ", gname])))
                fh.close()

def addDir(name, url, mode, iconimage,edit,inum,gname):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)+"&gname="+urllib.quote_plus(gname)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR yellow]Add Season To Library[/COLOR]','XBMC.Container.Update(%s?url=%s&gname=%s&mode=6)'%('plugin://plugin.video.moviHD',urllib.quote_plus(url),urllib.quote_plus(gname))))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage,gname):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    contextmenuitems = []
    contextmenuitems.append(('Download','XBMC.Container.Update(%s?url=%s&gname=%s&mode=10)'%('plugin://plugin.video.moviHD',urllib.quote_plus(url),urllib.quote_plus(gname))))
    contextmenuitems.append(('[COLOR yellow]Add To Library[/COLOR]','XBMC.Container.Update(%s?url=%s&gname=%s&mode=5)'%('plugin://plugin.video.moviHD',urllib.quote_plus(url),urllib.quote_plus(gname))))
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
gname=None


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
try:
        gname=urllib.unquote_plus(params["gname"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index(url)
elif mode==2:
    videolinks(url)
elif mode==3:
    play(url,name)
elif mode==4:
    episodes(url)
elif mode==5:
    addToLibrary(url)
elif mode==6:
    addSeasonToLibrary(url)

xbmcplugin.endOfDirectory(int(sysarg))