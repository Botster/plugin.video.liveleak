import urllib,urllib2,re,xbmcplugin,xbmcgui
from HTMLParser import HTMLParser

BASE = "http://www.liveleak.com/"


def CATEGORIES():
    addDir('Popular','browse?popular',1,'')
    addDir('Featured','browse?featured=1',1,'')
    addDir('News & Politics','browse?channel_token=04c_1302956196',1,'')
    addDir('Yoursay','browse?channel_token=1b3_1302956579',1,'')
    addDir('Must See','browse?channel_token=9ee_1303244161',1,'')
    addDir('Syria','browse?channel_token=cf3_1304149308',1,'')
    addDir('Iraq','browse?channel_token=e8a_1302956438',1,'')
    addDir('Afghanistan','browse?channel_token=79f_1302956483',1,'')
    addDir('Entertainment','browse?channel_token=51a_1302956523',1,'')
    addDir('Search','browse?q=',1,'')
    

def INDEX(url):
    if url=="browse?q=":
        searchString = addSearch()
        url="browse?q="+searchString
    after = url
    url = BASE + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    
    try:
        appdg = after.split('&')[1]
        before = after.split('&')[0]
        appdg = int(appdg.split('=')[1]) + 1
        newURL = before + "&page=" + str(appdg)
    except:
        newURL = after + "&page=2"
        appdg = 2
    addDir("Go To Page " + str(appdg), newURL, 1, "")
    
    match=re.findall('<a href="(.+?)"><img class="thumbnail_image" src="(.+?)" alt="(.+?)"', link)
    for url,thumbnail,name in match:
        # Aggressively decode HTML entities to regular characters
        h = HTMLParser()
        name=h.unescape(h.unescape(name))
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        match = re.findall('<source src="(.+?)".*$', link, re.MULTILINE)
        for idx, url in enumerate(match):
            if len(match) > 1:
                idx_tag = " (" + str(idx + 1) + ")"
            else:
                idx_tag = ''
            addLink(name + idx_tag, url, thumbnail, "")
        match = re.findall('src="//www.youtube.com/embed/(.+?)\?rel=0.*$', link, re.MULTILINE)
        for idx, url in enumerate(match):
            if len(match) > 1:
                idx_tag = " (" + str(idx + 1) + ")"
            else:
                idx_tag = ''
            youtubeurl = 'plugin://plugin.video.youtube/play/?video_id=%s' % url
            addLink(name + idx_tag, youtubeurl, thumbnail, "")


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


def addLink(name,url,iconimage,urlType):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable','true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok


def addSearch():
    searchStr = ''
    keyboard = xbmc.Keyboard(searchStr, 'Search')
    keyboard.doModal()
    if (keyboard.isConfirmed()==False):
        return
    searchStr=keyboard.getText()
    if len(searchStr) == 0:
        return
    else:
        return searchStr


def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)\
        +"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    print ""
    CATEGORIES()

elif mode==1:
    print ""+url
    INDEX(url)

elif mode==2:
    print ""+url
    addSearch()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
