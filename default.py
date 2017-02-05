# Standard libraries
import urllib, urllib2, urlparse, re
from HTMLParser import HTMLParser

# Kodi libraries
import xbmc, xbmcplugin, xbmcgui

# Identifiers
BASE_URL = sys.argv[0]
ADDON_HANDLE = sys.argv[1]

domain_home = "http://www.liveleak.com/"

# --- Functions ---

def categories():
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
    

def index(url):
    if url=="browse?q=":
        searchString = addSearch()
        url="browse?q="+searchString
    after = url
    url = domain_home + url
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
        # Convert utf8-encoded 'name' string to unicode to prevent errors.
        # Also ignore unrecognized characters.
        name = unicode(name, 'utf-8', errors='ignore')

        # Strip any dangling whitespace and decode (possibly double-stacked) html entities.
        h = HTMLParser()
        name = h.unescape(h.unescape(name.strip()))

        # Convert back to utf-8 for output
        name = name.encode('utf-8')
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        match = re.findall('<source src="(.+?)".*$', link, re.MULTILINE)
        for url in match:
            addLink(name, url, thumbnail, "")
        match = re.findall('src="//www.youtube.com/embed/(.+?)\?rel=0.*$', link, re.MULTILINE)
        for url in match:
            youtubeurl = 'plugin://plugin.video.youtube/play/?video_id=%s' % url
            addLink(name, youtubeurl, thumbnail, "")

def addLink(name,url,iconimage,urlType):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable','true')
    ok=xbmcplugin.addDirectoryItem(handle=int(ADDON_HANDLE),url=url,listitem=liz)
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
    u=BASE_URL+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)\
        +"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(ADDON_HANDLE),url=u,listitem=liz,isFolder=True)
    return ok


# --- Main Event ---

# Get any provided query string
params = sys.argv[2][1:]
if len(params) < 2: # No query string provided
    mode = None # No mode, default to categories
    name = None # Define to prevent errors
    url = None # ... ditto
else: # Parse the query string
    # Strip any trailing '/'
    if params[-1] == '/': params = params[:-1]

    # Parse query string into dictionary as {"key": [list-of-one]}
    params = urlparse.parse_qs(params)

    # Get list for parameter keys defaulting to None if nonexistent
    mode = params.get('mode', None)
    name = params.get('name', None)
    url = params.get('url', None)

    # Get the only 'mode' list item and cast to int
    if mode is not None: mode = int(mode[0]) 

    # Decode any %xx in the only 'name' list item
    if name is not None:
        name = urllib.unquote_plus(params["name"][0]) 

    # Decode any %xx in the only 'url' list item
    if url is not None:
        url = urllib.unquote_plus(params["url"][0])

#xbmc.log( "LIVELEAK-> Mode: "+str(mode)+", Name: "+str(name)+", URL: "+str(url) )


if mode is None or url is None or len(url) < 1:
    categories()

elif mode == 1:
    index(url)

elif mode == 2:
    addSearch()


xbmcplugin.endOfDirectory(int(ADDON_HANDLE))
