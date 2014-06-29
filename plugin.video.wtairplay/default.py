import xbmc,urllib

try:url=sys.argv[1].replace('url=','')
except:
    import xbmcgui
    xbmcgui.Dialog().ok('wareztuga.tv','Deve iniciar este addon pela interface web.','http://bit.ly/wt-airplay')
    sys.exit(0)
    
comando='plugin://plugin.video.wt/?url=%s&mode=5&name=Nada' % (urllib.quote_plus(url))
xbmc.executebuiltin("RunPlugin(%s)"%(comando))
