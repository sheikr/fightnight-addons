# -*- coding: utf-8 -*-

""" Log Viewer for Kodi
    2015 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,os,re,sys

versao = '0.1.01'
addon_id = 'plugin.video.xbmclogviewer'
versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
dataPath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile').decode('utf-8'))
if not os.path.exists(dataPath): os.makedirs(dataPath)
               
def loglocation(): 
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
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
        return log_path

def mostrarlog(get=False):
      if versionNumber < 14: filename='xbmc.log'
      else: filename='kodi.log'
      pathoriginal=loglocation() + filename
      pathcopia=os.path.join(dataPath,filename)

      try: os.remove(pathcopia)
      except: pass

      copyfile(pathoriginal, pathcopia)
      conteudolog=openfile(pathcopia)
      if xbmcaddon.Addon().getSetting('inverter') == 'true':
            inverted=conteudolog.splitlines()[::-1]
            try:
                  nrlinhas=xbmcaddon.Addon().getSetting('nrlinhas')
                  if nrlinhas=='1': inverted=inverted[0:100]
                  elif nrlinhas=='2': inverted=inverted[0:50]
                  elif nrlinhas=='3': inverted=inverted[0:20]
            except: pass
            conteudolog='\n'.join(inverted)
      
      if get==False:window(conteudolog)
      else: return conteudolog

def window(conteudolog):
      try:
            xbmc.executebuiltin("ActivateWindow(10147)")
            window = xbmcgui.Window(10147)
            xbmc.sleep(100)
            window.getControl(1).setLabel("Log Viewer for Kodi")
            window.getControl(5).setText(conteudolog)
      except:
            pass


def copyfile(source, dest, buffer_size=1024*1024):
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

def addReload(name,iconimage=''):
      u=sys.argv[0]+"?&mode=None"
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

mode=None

if sys.argv[2]=='showlog/':
      mostrarlog()

elif sys.argv[2]=='getlog/':
      mostrarlog(get=True)

elif mode==None:
      print "Versao Instalada: v" + versao
      mostrarlog()
      addReload('Recarregar Log')
                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
