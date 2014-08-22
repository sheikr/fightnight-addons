# -*- coding: utf-8 -*-

""" Karaoke Portugues
    2013 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time

####################################################### CONSTANTES #####################################################

versao = '0.0.06'
addon_id = 'plugin.video.karaokept'
MainURL = 'http://abelhas.pt/'
art = '/resources/art/'
BaseURL = 'http://fightnight-xbmc.googlecode.com/svn/karaoke/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'iconpqmudar.jpg'
traducaoma= selfAddon.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
#downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
entrada='wbnb.fvyin333/Cevinqn/'
pastafavoritos = os.path.join(pastaperfil, "favoritos")
cookies = os.path.join(pastaperfil, "cookies.lwp")
username = urllib.quote(selfAddon.getSetting('abelhas-username'))
password = selfAddon.getSetting('abelhas-password')


def traducao(texto):
      return traducaoma(texto).encode('utf-8')

def login_abelhas():
      print "Sem cookie. A iniciar login"
      from t0mm0.common.net import Net
      net=Net()
      try:
            link=abrir_url(MainURL)
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(link)[0]
            form_d = {'RedirectUrl':'','Redirect':'True','FileId':0,'Login':username,'Password':password,'RememberMe':'true','__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
            endlogin=MainURL + 'action/login/login'
            try:
                  logintest= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: logintest='Erro'
      except:
            link='Erro'
            logintest='Erro'

      if selfAddon.getSetting('abelhas-username')== '':
            ok = mensagemok('Karaoke Português',traducao(40000),traducao(40001))
            entrarnovamente(1)
      else:    
            if re.search('003eA senha indicada n',logintest):
                  mensagemok('Karaoke Português',traducao(40002))
                  entrarnovamente(1)
            elif re.search('existe. Certifica-te que indicaste o nome correcto.',logintest):
                  mensagemok('Karaoke Português',traducao(40003))
                  entrarnovamente(1)
            elif re.search(username,logintest):
                  #xbmc.executebuiltin("XBMC.Notification(Karaoke Português,"+traducao(40004)+",'500000',"+iconpequeno.encode('utf-8')+")")
                  net.save_cookies(cookies)
                  conteudo=clean(abrir_url_cookie(MainURL + str(entrada.decode('rot13'))))
                  if re.search('ProtectedFolderChomikLogin',conteudo):
                        chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                        folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                        foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                        routinas1='Cnffjbeq'; routinas2='enzobvn'
                        form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,str(routinas1.decode('rot13')):str(routinas2.decode('rot13')),'Remember':'true','__RequestVerificationToken':token}
                        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                        endlogin=MainURL + 'action/Files/LoginToFolder'
                        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')

                  listagem=abrir_url(BaseURL + 'listagem2.txt')
                  localizacao=os.path.join(pastaperfil,'listagem.txt')
                  try:os.remove(localizacao)
                  except: pass
                  savefile(pastaperfil,'listagem.txt',listagem)
                 
                  menu_principal(1)
            
            elif re.search('Erro',logintest) or link=='Erro':
                  opcao= xbmcgui.Dialog().yesno('Karaoke Português', traducao(40005), "", "",traducao(40006), 'OK')
                  if opcao: menu_principal(0)
                  else: login_abelhas()
                
################################################### MENUS PLUGIN ######################################################

def menu_principal(ligacao):
      if ligacao==1:
            addDir('Todas as Músicas','querotodasasmusicas',1,wtpath + art + 'pasta.png',1,True)
            addDir('TOP30 Cantadas',MainURL,12,wtpath + art + 'pasta.png',2,True)
            addDir('Artistas',MainURL,4,wtpath + art + 'pasta.png',2,True)
            addDir('Filtros',MainURL,13,wtpath + art + 'pasta.png',2,True)
            addDir('Mais recentes','all',7,wtpath + art + 'pasta.png',2,True)
            addDir('Música directa (ID)',MainURL + username,3,wtpath + art + 'pasta.png',2,False)
            addDir('Favoritos','pastas',9,wtpath + art + 'pasta.png',2,True)
            #addDir('Pesquisar','pastas',5,wtpath + art + 'series.png',2,True)
            #addLink("",'',wtpath + art + 'nothingx.png')
      elif ligacao==0:
            addDir(traducao(40015),MainURL,6,wtpath + art + 'pasta.png',1,True)
            #addLink("",'',wtpath + art + 'nothingx.png')
      #if ligacao==1:
      #      disponivel=versao_disponivel()
      #      if disponivel==versao: addLink(traducao(40017) + versao+ ')','',wtpath + art + 'versao_disp.png')
      #      else: addDir(traducao(40016) + versao + ' | ' + traducao(40019) + disponivel,MainURL,13,wtpath + art + 'versao_disp.png',1,False)
      #else: addLink(traducao(40016) + versao,'',wtpath + art + 'versao_disp.png')
      addDir("[COLOR gold][B]%s[/B][/COLOR] | Karaoke Português" % (traducao(40018)),MainURL,8,wtpath + art + 'pasta.png',6,False)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def filtros():
      addDir('[B]Portuguesas[/B] (brevemente)','oth',14,wtpath + art + 'pasta.png',1,False)
      addDir('[B]Brasileiras[/B] (brevemente)','oth',14,wtpath + art + 'pasta.png',1,False)
      
      addDir('Jardim de Infancia','jdi',14,wtpath + art + 'pasta.png',1,True)
      addDir('Kantatu','ktt',14,wtpath + art + 'pasta.png',1,True)
      addDir('Karaoke Mania','kam',14,wtpath + art + 'pasta.png',1,True)
      addDir('Outros','oth',14,wtpath + art + 'pasta.png',1,True)
      addDir('Portugal Karaoke','ptk',14,wtpath + art + 'pasta.png',1,True)
      xbmc.executebuiltin("Container.SetViewMode(51)")
      

def filtroscat(url):
      listagem=openfile('listagem.txt')
      try:favoritos = os.listdir(pastafavoritos)
      except: favoritos=[]
      musicas=re.compile('"id":"'+url+'(.+?)","artist":"(.+?)","song":"(.+?)"').findall(listagem)
      for musicid,artist,song in musicas:
            if musicid in favoritos: faved=True
            else: faved=False
            addCont('[B]%s[/B] - %s (%s)' % (artist,song,'%s%s' % (url,musicid)),'%s%s' % (url,musicid),2,wtpath + art + 'seta.png',len(musicas),faved,False)
      xbmc.executebuiltin("Container.SetViewMode(51)")


def todasasmusicas(url):
      listagem=openfile('listagem.txt')
      try:favoritos = os.listdir(pastafavoritos)
      except: favoritos=[]
      
      if url=='querotodasasmusicas':
            update=re.compile('"update":"(.+?)"').findall(listagem)[0]
            addLink('[B]Última Actualização[/B]: %s' % update,'',wtpath + art + 'pasta.png')
            
            musicas=re.compile('"id":"(.+?)","artist":"(.+?)","song":"(.+?)"').findall(listagem)
            for musicid,artist,song in musicas:
                  if musicid in favoritos: faved=True
                  else: faved=False
                  addCont('[B]%s[/B] - %s (%s)' % (artist,song,musicid),musicid,2,wtpath + art + 'seta.png',len(musicas),faved,False)
      
      else:
            musicas=re.compile('"id":"(.+?)","artist":"'+url+'","song":"(.+?)"').findall(listagem)
            for musicid,song in musicas:
                  if musicid in favoritos: faved=True
                  else: faved=False
                  addCont('[B]%s[/B] - %s (%s)' % (url,song,musicid),musicid,2,wtpath + art + 'seta.png',len(musicas),faved,False)
      xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
      xbmc.executebuiltin("Container.SetViewMode(51)")

def artistas():
      listagem=openfile('listagem.txt')
      musicas=re.compile('"artist":"(.+?)"').findall(listagem)
      seen= set()
      seen_add = seen.add
      limpo= [ x for x in musicas if x not in seen and not seen_add(x)]
      for artistas in limpo:
            addDir(artistas,artistas,1,wtpath + art + 'pasta.png',len(limpo),True)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def top30():
      i=0
      conteudo=abrir_url_cookie(MainURL + str(entrada.decode('rot13')) + 'all?requestedFolderMode=filesList&fileListSortType=Downloads&fileListAscending=False')
      ultimas=re.compile('<span class="bold">(.+?)</span>').findall(conteudo)
      listagem=openfile('listagem.txt')
      try: favoritos = os.listdir(pastafavoritos)
      except: favoritos=[]
      for referencias in ultimas:
            i=i+1
            if referencias in favoritos: faved=True
            else: faved=False
            try:
                  musicas=re.compile('"id":"'+referencias+'","artist":"(.+?)","song":"(.+?)"').findall(listagem)[0]
                  addCont('[COLOR blue][B]%sº[/B][/COLOR]: [B]%s[/B] - %s (%s)' % (i,musicas[0],musicas[1],referencias),referencias,2,wtpath + art + 'seta.png',len(ultimas),faved,False)
            except: pass
      xbmc.executebuiltin("Container.SetViewMode(51)")


def ultimasadicionadas(url):
      if re.search('>>',name):conteudo=abrir_url_cookie(MainURL + url + '?requestedFolderMode=filesList&fileListSortType=Date&fileListAscending=False')
      else: conteudo=abrir_url_cookie(MainURL + str(entrada.decode('rot13')) + url + '?requestedFolderMode=filesList&fileListSortType=Date&fileListAscending=False')
      
      ultimas=re.compile('<span class="bold">(.+?)</span>').findall(conteudo)
      listagem=openfile('listagem.txt')
      try: favoritos = os.listdir(pastafavoritos)
      except: favoritos=[]
      for referencias in ultimas:
            if referencias in favoritos: faved=True
            else: faved=False
            try:
                  musicas=re.compile('"id":"'+referencias+'","artist":"(.+?)","song":"(.+?)"').findall(listagem)[0]
                  addCont('[B]%s[/B] - %s (%s)' % (musicas[0],musicas[1],referencias),referencias,2,wtpath + art + 'seta.png',len(ultimas),faved,False)
            except: pass
      paginas(conteudo)
      xbmc.executebuiltin("Container.SetViewMode(51)")
      
def paginas(link):
      try:
            pagina=re.compile('anterior.+?<a href="/(.+?)" class="right" rel=".+?"').findall(link)[0].replace(' ','+')
            addDir('[COLOR blue]Mais Antigas >>>[/COLOR]',pagina,7,wtpath + art + 'seta.png',1,True)
      except:
            pass


def musicadirecta():
      idname=caixadetexto(url).lower()
      listagem=openfile('listagem.txt')
      try:
            musicas=re.compile('"id":"'+idname+'","artist":"(.+?)","song":"(.+?)"').findall(listagem)[0]
            name='[B]%s[/B] - %s (%s)' % (musicas[0],musicas[1],idname)
            analyzer(idname,name)
      except:
            mensagemok('Karaoke Português','ID inválido.')

def favoritos():
      listagem=openfile('listagem.txt')
      listagem = unicode(listagem, errors='ignore')
      try: favoritos = os.listdir(pastafavoritos)
      except: favoritos=[]
      for referencias in favoritos:
            if referencias in favoritos: faved=True
            else: faved=False
            musicas=re.compile('"id":"'+referencias+'","artist":"(.+?)","song":"(.+?)"').findall(listagem)[0]
            addCont('[B]%s[/B] - %s (%s)' % (musicas[0],musicas[1],referencias),referencias,2,wtpath + art + 'seta.png',len(favoritos),faved,False)
      xbmc.executebuiltin("Container.SetViewMode(51)")      

def guardarfavoritos(url):
      if not os.path.exists(pastafavoritos):
          os.makedirs(pastafavoritos)
      from random import randint
      nomeficheiro=str(randint(0, 0x7fffffff))
      savefile(pastafavoritos,url,'')
      xbmc.executebuiltin("XBMC.Notification(Karaoke Português,Adicionado aos favoritos,'500000',"+iconpequeno.encode('utf-8')+")")

def apagarfavoritos(url):
      favorito=os.path.join(pastafavoritos,url)
      os.remove(favorito)
      xbmc.executebuiltin("XBMC.Notification(Karaoke Português,Removido dos favoritos,'500000',"+iconpequeno.encode('utf-8')+")")
      xbmc.executebuiltin("Container.Refresh")
      
def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40020),MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40021),MainURL,8,wtpath + art + 'defs.png',1,False)

########################################################### PLAYER ################################################

def analyzer(url,name):
      final=''
      mensagemprogresso.create('Karaoke Português', traducao(40025))
      mensagemprogresso.update(0)
      from t0mm0.common.net import Net
      net=Net()
      if re.search('ptk',url) or re.search('jdi',url) or re.search('kam',url) or re.search('oth',url):filetype='.mp4'
      else: filetype='.avi'
      conteudo=abrir_url_cookie(MainURL + str(entrada.decode('rot13')) + 'all/' + url + filetype)

      if re.search('Pode acontecer que a mensagem de confirma',conteudo):
            mensagemok('Karaoke Português','Necessitas de activar a tua conta abelhas.')
            return
      try:
            fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            form_d = {'fileId':fileid,'__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
            endlogin=MainURL + 'action/License/Download'
            final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
      except:
            mensagemok('Karaoke Português','Ficheiro indisponivel.')

      try:
            if re.search('action/License/acceptLargeTransfer',final):
                  fileid=re.compile('<input type="hidden" name="fileId" value="(.+?)"').findall(final)[0]
                  orgfile=re.compile('<input type="hidden" name="orgFile" value="(.+?)"').findall(final)[0]
                  userselection=re.compile('<input type="hidden" name="userSelection" value="(.+?)"').findall(final)[0]
                  form_d = {'fileId':fileid,'orgFile':orgfile,'userSelection':userselection,'__RequestVerificationToken':token}
                  ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
                  endlogin=MainURL + 'action/License/acceptLargeTransfer'
                  final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
      except: pass
      try:
            if re.search('causar problemas com o uso de aceleradores de download',final):linkfinal=re.compile('a href=\"(.+?)\"').findall(final)[0]
            else: linkfinal=re.compile('"redirectUrl":"(.+?)"').findall(final)[0]
      except:
            if re.search('Por favor tenta baixar este ficheiro mais tarde.',final):
                  mensagemok('Karaoke Português',traducao(40026))
                  return
            else:
                  linkfinal=''
                  mensagemok('Karaoke Português',traducao(40027))
                  print str(final)
                  print str(linkfinal) 
                  return

      mensagemprogresso.close()
      comecarvideo(name,linkfinal)

def comecarvideo(name,url):
        thumbnail=wtpath + art + 'player.jpg'
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        listitem.setInfo("Video", {"Title":name})
        listitem.setInfo("Music", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(url, listitem)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
        #dialogWait = xbmcgui.DialogProgress()
        #dialogWait.create('Video', 'A carregar')
        
        #dialogWait.close()
        #del dialogWait
        
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

def addCont(name,url,mode,iconimage,total,faved,pasta):
      contexto=[]
      if faved==False: contexto.append(('Adicionar aos favoritos', 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      else:
            contexto.append(('Remover dos favoritos', 'XBMC.RunPlugin(%s?mode=11&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
            iconimage=wtpath + art + 'star2.png'
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems(contexto, replaceItems=True) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

######################################################## OUTRAS FUNCOES ###############################################

def savefile(caminho,filename, contents):
    try:
        destination = os.path.join(caminho, filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename

def openfile(filename):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % filename
        return None

def caixadetexto(url):
      title="Introduza o ID - Karaoke Português"
      keyb = xbmc.Keyboard(selfAddon.getSetting('ultima-pesquisa'), title)
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote_plus(search)
            return encode
            
      else: sys.exit(0)
            
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
            ref_data = {'Host': 'abelhas.pt', 'Connection': 'keep-alive', 'Referer': 'http://abelhas.pt/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            link=net.http_GET(url,ref_data).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            if erro==True: mensagemok('Karaoke Português',str(urllib2.HTTPError(e.url, e.code, traducao(40032), e.hdrs, e.fp)),traducao(40033))
            sys.exit(0)
      except urllib2.URLError, e:
            if erro==True: mensagemok('Karaoke Português',traducao(40032)+traducao(40033))
            sys.exit(0)
            
def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.karaokept/addon.xml')
            match=re.compile('name="Karaoke Portugues"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Karaoke Português',traducao(40034),traducao(40035),'')
            match=traducao(40036)
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
      login_abelhas()
elif mode==1: todasasmusicas(url)
elif mode==2: analyzer(url,name)
elif mode==3: musicadirecta()
elif mode==4: artistas()
elif mode==5: caixadetexto(url)
elif mode==6: login_abelhas()
elif mode==7: ultimasadicionadas(url)
elif mode==8: selfAddon.openSettings()#sacarficheiros()
elif mode==9: favoritos()
elif mode==10: guardarfavoritos(url)
elif mode==11: apagarfavoritos(url)
elif mode==12: top30()
elif mode==13: filtros()
elif mode==14: filtroscat(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
