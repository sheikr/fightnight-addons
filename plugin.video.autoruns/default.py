# -*- coding: utf-8 -*-

""" Autoruns
    2013 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,os,re,sys

versao = '0.1.00'
addon_id = 'plugin.video.autoruns'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
               
################################################### MENUS PLUGIN ######################################################

def menu_principal():
      if selfAddon.getSetting('avisoinicial') == 'true':
            xbmcgui.Dialog().ok('Autoruns','This addon improves xbmc speed by disabling','addons from startup. Be careful. Some addons','may require the startup service to run.')
            xbmcgui.Dialog().ok('Autoruns','Click on addon name to turn off/on service.','Restart XBMC to reload changes.')
            selfAddon.setSetting('avisoinicial', 'false')
      listaraddons()

def listaraddons():
      pastadeaddons = os.path.join(xbmc.translatePath('special://home/addons'), '')
      directories = os.listdir(pastadeaddons)
      for nomedeaddon in directories:
            pastadirecta = os.path.join(pastadeaddons, nomedeaddon)
            addonxmlcaminho=os.path.join(pastadirecta,'addon.xml')
            if os.path.exists(addonxmlcaminho):
                  conteudo=openfile(addonxmlcaminho)
                  if re.search('point="xbmc.service"',conteudo):
                        addDir(nomedeaddon + ' (on)',pastadirecta,1,os.path.join(pastadirecta,'icon.png'),1,False)
                  elif re.search('point="xbmc.pass"',conteudo):
                        addDir('[B][COLOR gold]'+ nomedeaddon + '[/B] (off)[/COLOR]',pastadirecta,1,os.path.join(pastadirecta,'icon.png'),1,False)

def mudaestado(name,url):
      directoparaxml=os.path.join(url,'addon.xml')
      conteudo=openfile(directoparaxml)
      if re.search('COLOR gold',name): conteudo=conteudo.replace('point="xbmc.pass"','point="xbmc.service"')
      else: conteudo=conteudo.replace('point="xbmc.service"','point="xbmc.pass"')
      savefile(directoparaxml,conteudo)
      xbmc.executebuiltin("Container.Refresh")
      

def openfile(pastacaminho):
    try:
        fh = open(pastacaminho, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % filename
        return None

def savefile(pastacaminho,conteudo):
    try:
        fh = open(pastacaminho, 'wb')
        fh.write(conteudo)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

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

if mode==None:
      print "Versao Instalada: v" + versao
      menu_principal()
elif mode==1: mudaestado(name,url)
                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
