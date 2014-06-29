# -*- coding: utf-8 -*-

""" XBMC Log Viewer
    2013 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil

####################################################### CONSTANTES #####################################################

versao = '0.0.02'
addon_id = 'plugin.video.xbmclogviewer'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'logo32.png'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
pastadeaddons = os.path.join(xbmc.translatePath('special://home/addons'), '')
               
################################################### MENUS PLUGIN ######################################################

def menu_principal():
      selfAddon.setSetting('avisoinicial', 'false')
      mostrarlog()
      addDir('Recarregar Log','nada',1,'',1,False)
            
def loglocation(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
        log = os.path.join(log_path, 'xbmc.log')
    return log_path

def mostrarlog():
      try:            
            os.remove(pathcopia)
      except: pass

      copyfile(pathoriginal, pathcopia)
      
      ##hora log##
      dt  = datetime.datetime.now()
      dt.strftime('%Y-%m-%d%%20%H:%M')
      dts = dt.strftime('%Y-%m-%d%%20%H:%M')
      
      conteudolog=openfile(pathcopia)

      ##janela##
      try:
            xbmc.executebuiltin("ActivateWindow(10147)")
            window = xbmcgui.Window(10147)
            xbmc.sleep(100)
            window.getControl(1).setLabel("XBMC Log Viewer")
            window.getControl(5).setText(conteudolog)
      except:
            ## CRIAR JANELA ##
            pass


def copyfile(source, dest, buffer_size=1024*1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
    if not hasattr(dest, 'write'):
        dest = open(dest, 'wb')

    while 1:
        copy_buffer = source.read(buffer_size)
        if copy_buffer:
            dest.write(copy_buffer)
        else:
            break

    source.close()
    dest.close()

def openfile(pastacaminho):
    try:
        fh = open(pastacaminho, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % pastacaminho
        return None

def savefile(pastacaminho,conteudo):
    try:
        fh = open(pastacaminho, 'wb')
        fh.write(conteudo)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename


def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

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

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      pathoriginal=loglocation() + 'xbmc.log'
      pathcopia=os.path.join(pastaperfil,'xbmc.log')
      menu_principal()
elif mode==1:
      pathoriginal=loglocation() + 'xbmc.log'
      pathcopia=os.path.join(pastaperfil,'xbmc.log')
      mostrarlog()
                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
