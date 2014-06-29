# -*- coding: utf-8 -*-

""" Autoruns
    2013 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys

####################################################### CONSTANTES #####################################################

versao = '0.0.02'
addon_id = 'plugin.video.autoruns'
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
      if selfAddon.getSetting('avisoinicial') == 'true':
            mensagemok('Autoruns','This addon improves xbmc speed by disabling','addons from startup. Be careful. Some addons','may require the startup service to run.')
            mensagemok('Autoruns','Click on addon name to turn off/on service.','Restart XBMC to reload changes.')
            selfAddon.setSetting('avisoinicial', 'false')
      listaraddons()

def listaraddons():
      directories = os.listdir(pastadeaddons)
      for nomedeaddon in directories:
            pastadirecta = os.path.join(pastadeaddons, nomedeaddon)
            addonxmlcaminho=os.path.join(pastadirecta,'addon.xml')
            if os.path.exists(addonxmlcaminho):
                  conteudo=openfile(addonxmlcaminho)
                  if re.search('point="xbmc.service"',conteudo):
                        addDir(nomedeaddon + ' (on)',pastadirecta,1,pastadirecta + 'icon.png',1,False)
                  elif re.search('point="xbmc.pass"',conteudo):
                        addDir('[B][COLOR gold]'+ nomedeaddon + '[/B] (off)[/COLOR]',pastadirecta,1,pastadirecta + 'icon.png',1,False)
            else: print "NAO EXISTE!!!!"

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

def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/wareztuga/plugin.video.wt/addon.xml')
            match=re.compile('name="wareztuga.tv"\r\n       version="(.+?)"\r\n       provider-name="wareztuga">').findall(link)[0]
      except:
            ok = mensagemok('wareztuga.tv',traducao(40184),traducao(40185),'')
            match=traducao(40186)
      return match

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
      menu_principal()
elif mode==1: mudaestado(name,url)
                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
