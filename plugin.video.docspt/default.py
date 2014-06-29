# -*- coding: utf-8 -*-

""" docsPT
    2014 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time

####################################################### CONSTANTES #####################################################

versao = '0.0.04'
addon_id = 'plugin.video.docspt'
MainURL = 'http://www.docspt.com/'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'iconpq.jpg'
traducaoma= selfAddon.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookies = os.path.join(pastaperfil, "cookies.lwp")
username = selfAddon.getSetting('docspt-username')
password = selfAddon.getSetting('docspt-password')

def traducao(texto):
      return traducaoma(texto).encode('utf-8')


#################################################### LOGIN DOCS #####################################################

def login_docspt():
      print "Sem cookie. A iniciar login"
      try:
            from t0mm0.common.net import Net
            net=Net()
            #form_d = {'user':username,'passwrd':password,'cookieneverexp':'on','hash_passwrd':token}
            form_d={'user':username,'passwrd':password,'cookielength':-1}
            ref_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Content-Type': 'application/x-www-form-urlencoded','Host':'www.docspt.com','Origin': 'http://www.docspt.com', 'Referer': 'http://www.docspt.com/index.php?action=login2','User-Agent':user_agent}
            endlogin=MainURL + 'index.php?action=login2'
            try:
                  logintest= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: logintest='Erro'
      except:
            link='Erro'
            logintest='Erro'

      if selfAddon.getSetting('docspt-username')== '':
            ok = mensagemok('docsPT','Necessitas de criar conta em','docsPT.com')
            entrarnovamente(1)
      else:    
            if re.search('<p class="error">A password est',logintest):
                  mensagemok('docsPT','Password incorrecta.')
                  entrarnovamente(1)
            elif re.search('<p class="error">Esse utilizador n',logintest):
                  mensagemok('docsPT','Esse utilizador não existe.')
                  entrarnovamente(1)
            elif re.search(username+'!</li>',logintest):
                  xbmc.executebuiltin("XBMC.Notification(docsPT,Sessão iniciada com sucesso,'500000','')")
                  net.save_cookies(cookies)
                  menu_principal(1)
            
            elif re.search('Erro',logintest) or link=='Erro':
                  opcao= xbmcgui.Dialog().yesno('docsPT', 'Sem acesso à internet.', "", "","Tentar novamente", 'OK')
                  if opcao: menu_principal(0)
                  else: login_docspt()                
################################################### MENUS PLUGIN ######################################################

def irparaurl():
      keyb = xbmc.Keyboard(selfAddon.getSetting('ultima-pesquisa'), 'Introduz ID do Tópico')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            selfAddon.setSetting('ultima-pesquisa', search)
            #encode=urllib.quote_plus(search)
            conteudo(search)

def conteudo(url):
      import urlresolver
      sources=[]
      urltopico='http://www.docspt.com/index.php/topic,'+url+'.0.html'
      print urltopico
      conteudo=clean(abrir_url_cookie(urltopico))
      nometopico=re.compile('<title>(.+?)</title>').findall(conteudo)[0]
      mesmo=re.compile('<code class="bbc_code">(.+?)</code>').findall(conteudo)
      #print mesmo
      for endereco in mesmo:
            hosted_media = urlresolver.HostedMediaFile(endereco)
            if hosted_media: print "consegue"
            else: print "nao consegue"
            #print hosted_media
            sources.append(hosted_media)
      if not mesmo:
            if re.search('youtube.com',conteudo):
                  try:
                        idyoutube=re.compile('class="aeva_link bbc_link new_win">.+?v=(.+?)</a>').findall(conteudo)[0]
                        hosted_media = urlresolver.HostedMediaFile('http://www.youtube.com/watch?v=' + idyoutube)
                        sources.append(hosted_media)
                  except:pass
            if re.search('vimeo.com',conteudo):
                  try:
                        idv=re.compile('"http://vimeo.com/(.+?)"').findall(conteudo)[0]
                        hosted_media = urlresolver.HostedMediaFile('http://www.vimeo.com/' + idv)
                        sources.append(hosted_media)
                  except:pass

      source = urlresolver.choose_source(sources)
      if source:
            linkescolha=source.resolve()
            if linkescolha==False:
                  okcheck = xbmcgui.Dialog().ok
                  okcheck('docsPT','Indisponivel')
                  return
            else:
                  comecarvideo(nometopico,linkescolha,'')
      else:
            mensagemok('docsPT','Conteúdo não disponível :(')

def filtrodeconteudos():      
      conteudo=clean(abrir_url_cookie(MainURL + 'index.php?action=autoindex;sa=board&amp;id=86'))
      listagem=re.compile('src="http://www.docspt.com/Themes/citiez_20b/images/row-ai.png"/> <a href="http://www.docspt.com/index.php/topic,(.+?).0.html" target="_blank" >(.+?)</a>').findall(conteudo)
      for idtop,nometop in listagem:
            nometop=nometop.decode('latin-1','ignore').encode('utf-8')
            addDir(nometop,idtop,3,wtpath + art + 'filmes.png',1,False)

def menu_principal(ligacao):
      if ligacao==1:
            addDir('Listagem de Documentarios',MainURL,2,wtpath + art + 'series.png',2,True)
            addDir('Ir para tópico',MainURL,1,wtpath + art + 'filmes.png',1,False)
            addLink('','','')
      elif ligacao==0:
            addDir('Reconectar Addon',MainURL,6,wtpath + art + 'refresh.png',1,True)
            addLink("",'',wtpath + art + 'nothingx.png')
      if ligacao==1:
            disponivel=versao_disponivel()
            if disponivel==versao: addLink('Última versão instalada (' + versao+ ')','',wtpath + art + 'versao_disp.png')
            else: addDir('Instalada: ' + versao + ' | ' + 'Actualização: ' + disponivel,MainURL,13,wtpath + art + 'versao_disp.png',1,False)
      else: ('Versão Instalada: ' + versao,'',wtpath + art + 'versao_disp.png')
      addDir("Definições do Addon | [COLOR green][B]docsPT[/B][/COLOR]",MainURL,8,wtpath + art + 'defs.png',6,True)
      xbmc.executebuiltin("Container.SetViewMode(50)")

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40020),MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40021),MainURL,8,wtpath + art + 'defs.png',1,False)

########################################################### PLAYER ################################################

def comecarvideo(titulo,url,thumb):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(titulo, iconImage="DefaultVideo.png", thumbnailImage=thumb)            
      listitem.setInfo("Video", {"Title":titulo})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      dialogWait = xbmcgui.DialogProgress()
      dialogWait.create('docsPT', 'A carregar')
      playlist.add(url, listitem)
      dialogWait.close()
      del dialogWait
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

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
           
######################################################## OUTRAS FUNCOES ###############################################

def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def abrir_url_cookie(url,erro=True):
      from t0mm0.common.net import Net
      net=Net()
      net.set_cookies(cookies)
      try:
            ref_data = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Connection':'keep-alive','Host':'www.docspt.com','User-Agent':user_agent}
            link=net.http_GET(url,ref_data).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            if erro==True: mensagemok('docsPT',str(urllib2.HTTPError(e.url, e.code, traducao(40032), e.hdrs, e.fp)),traducao(40033))
            sys.exit(0)
      except urllib2.URLError, e:
            if erro==True: mensagemok('docsPT',traducao(40032)+traducao(40033))
            sys.exit(0)
            
def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.docspt/addon.xml')
            match=re.compile('name="docsPT"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('docsPT','Não foi possível conectar ao servidor','de actualização. Verifique situação.','')
            match='Indisponível'
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

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
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

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      login_docspt()
elif mode==1: irparaurl()
elif mode==2: filtrodeconteudos()
elif mode==3: conteudo(url)
elif mode==6: login_docspt()
elif mode==8: selfAddon.openSettings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
