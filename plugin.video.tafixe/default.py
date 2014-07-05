# -*- coding: utf-8 -*-

""" Ta Fixe
    2014 fightnight
"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re,sys, urllib, urllib2

####################################################### CONSTANTES #####################################################

versao = '0.0.06'
addon_id = 'plugin.video.tafixe'
MainURL = 'http://www.tafixe.com/'
vazio= []
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
selfAddon = xbmcaddon.Addon(id=addon_id)
sapopath = selfAddon.getAddonInfo('path')
menuescolha = xbmcgui.Dialog().select
mensagemok = xbmcgui.Dialog().ok

def menu_principal():
      addDir("Categorias",MainURL,3,'',1,True)
      addDir("Últimos Vídeos",MainURL,2,'',1,True)
      addDir("Procurar Vídeos",MainURL,5,'',1,True)
      addLink("",'','')
      disponivel=versao_disponivel()
      if disponivel==versao: addLink('Última versao instalada (' + versao+ ')','','')
      else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,MainURL,4,'',1,False)
      addDir("Definições do Addon | [COLOR blue][B]Tá Fixe[/B][/COLOR]",MainURL,6,'',1,False)
      xbmc.executebuiltin("Container.SetViewMode(501)")

def categorias():
      link=abrir_url(MainURL + 'category/videos/')
      
      categorias=re.compile('<li class="entry-category"><a href="(.+?)">(.+?)</a></li>').findall(link)
      for endereco,titulo in categorias:
            addDir(titulo,endereco,2,'',len(categorias),True)
      
def request(url):
      link=abrir_url(url)
      link=clean(link)
      #print link
      #listavideos=re.compile('<h1 class="title"><a href="(.+?)" title="(.+?)">.+?</a></h1>').findall(link)
      #listavideos=re.compile('<div class="thumb-wrap"><a href="(.+?)" rel="bookmark" title="(.+?)">').findall(link)
      listavideos=re.compile('<h3 itemprop="name" class="entry-title"><a itemprop="url" href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h3>').findall(link)
      for endereco,titulo in listavideos:
            addDir(titulo,endereco,1,'',len(listavideos),False)
      paginas(url,link)

def paginas(url,link):
      try:
            proxpagina=re.compile('[^<]*<a href="([^"]+?)">Próximo').findall(link)[0]
            nrpagina=re.compile('page/(.+?)/').findall(proxpagina)[0]
            addDir('[COLOR blue]Ir para a página ' + nrpagina + ' >>[/COLOR]',proxpagina,2,'',1,True)
      except:
            pass

            
def captura(name,url):
      link=abrir_url(url)
      link=clean(link)
      info=re.compile('<meta name="description" content="(.+?)"/>').findall(link)[0].replace('&quot;','')
      titles=[]; ligacao=[]
      dailymotionref=int(0)
      dailymotion=re.compile('<iframe frameborder="0" width=".+?" height=".+?" src="http://www.dailymotion.com/embed/video/(.+?)"></iframe>').findall(link)
      if dailymotion:
            for codigo in dailymotion:
                  dailymotionref=int(dailymotionref + 1)
                  if len(dailymotion)==1: dailymotion2=str('')
                  else: dailymotion2=' #' + str(dailymotionref)
                  titles.append('Dailymotion' + dailymotion2)
                  ligacao.append('http://www.dailymotion.com/video/' + codigo)
      youtuberef=int(0)
      youtube=re.compile('<iframe.+?src=".+?youtube.com/embed/(.+?)".+?></iframe>').findall(link)
      if youtube:
            for codigo in youtube:
                  youtuberef=int(youtuberef + 1)
                  if len(youtube)==1: youtube2=str('')
                  else: youtube2=' #' + str(youtuberef)
                  titles.append('Youtube' + youtube2)
                  ligacao.append('http://www.youtube.com/watch?v=' + codigo)
      if selfAddon.getSetting('infovideo') == 'true':
            try:
                  xbmc.executebuiltin("ActivateWindow(10147)")
                  window = xbmcgui.Window(10147)
                  xbmc.sleep(100)
                  window.getControl(1).setLabel( "%s - %s" % (name,'Ta Fixe',))
                  window.getControl(5).setText(info)
            except: pass
      index=0
      if len(ligacao)==0:
            mensagemok('Ta Fixe','Servidor nao disponivel')
            return
      if index > -1:
             linkescolha=ligacao[index]
             if linkescolha:
                   import urlresolver
                   if re.search('youtube',linkescolha) or re.search('dailymotion',linkescolha):
                         sources=[]
                         hosted_media = urlresolver.HostedMediaFile(url=linkescolha)
                         sources.append(hosted_media)
                         source = urlresolver.choose_source(sources)
                         if source:
                               linkescolha=source.resolve()
                               if linkescolha==False:
                                     okcheck = xbmcgui.Dialog().ok
                                     okcheck('Ta Fixe','Video indisponivel ou removido.')
                                     return
                   comecarvideo(name,linkescolha,'')

def comecarvideo(titulo,url,thumb):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(titulo, iconImage="DefaultVideo.png", thumbnailImage=thumb)            
      listitem.setInfo("Video", {"Title":titulo})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      dialogWait = xbmcgui.DialogProgress()
      dialogWait.create('Video', 'A carregar')
      playlist.add(url, listitem)
      dialogWait.close()
      del dialogWait
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
      return ok

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
      return ok

def pesquisa():
      keyb = xbmc.Keyboard('', 'Pesquisar video')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            encode=urllib.quote_plus(search)
            if encode=='': pass
            else: request('http://www.tafixe.com/?s=' + encode)
                        
def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.tafixe/addon.xml')
            match=re.compile('name="Ta Fixe"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Tá Fixe','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
            match='Erro. Verificar origem do erro.'
      return match


def redirect(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      gurl=response.geturl()
      return gurl

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

def clean(text):
      command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)


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

if mode==None or url==None or len(url)<1: print "Versao Instalada: v" + versao; menu_principal()
elif mode==1: captura(name,url)
elif mode==2: request(url)
elif mode==3: categorias()
elif mode==4: ok = mensagemok('TVGolo','A actualizacao é automática. Caso nao actualize va ao','repositorio fightnight e prima c ou durante 2seg','e force a actualizacao. De seguida, reinicie o XBMC.')
elif mode==5: pesquisa()
elif mode==6: selfAddon.openSettings()
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
