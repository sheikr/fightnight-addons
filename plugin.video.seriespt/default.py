# -*- coding: utf-8 -*-

""" Séries Portuguesas
    2014 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time

####################################################### CONSTANTES #####################################################

versao = '0.1.00'
addon_id = 'plugin.video.seriespt'
MainURL = 'http://abelhas.pt/'
art = '/resources/art/'
BaseURL = 'http://fightnight-xbmc.googlecode.com/svn/series/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'icon32.png'
traducaoma= selfAddon.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
#downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
entrada='wbnb.fvyin333/Cevinqn/'
pastaguardados = os.path.join(pastaperfil, "guardados")
pastatracks = os.path.join(pastaperfil, "tracking")
pastavistos = os.path.join(pastaperfil, "vistos")
if not os.path.exists(pastatracks):
      os.makedirs(pastatracks)
if not os.path.exists(pastavistos):
      os.makedirs(pastavistos)
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
            ok = mensagemok('Séries Portuguesas',traducao(40000),traducao(40001))
            entrarnovamente(1)
      else:    
            if re.search('003eA senha indicada n',logintest):
                  mensagemok('Séries Portuguesas',traducao(40002))
                  entrarnovamente(1)
            elif re.search('existe. Certifica-te que indicaste o nome correcto.',logintest):
                  mensagemok('Séries Portuguesas',traducao(40003))
                  entrarnovamente(1)
            elif re.search(username,logintest):
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

                  verificarbd()                 
                  menu_principal(1)
            
            elif re.search('Erro',logintest) or link=='Erro':
                  opcao= xbmcgui.Dialog().yesno('Séries Portuguesas', traducao(40005), "", "",traducao(40006), 'OK')
                  if opcao: menu_principal(0)
                  else: login_abelhas()
                
def verificarbd():
      try:
            check=abrir_url(BaseURL + 'listagem2.md5')
            listagem=openfile('listagem2.md5')
            if listagem!=check:
                  ## BD ##
                  listagem=abrir_url(BaseURL + 'listagem2.txt')
                  localizacao=os.path.join(pastaperfil,'listagem2.txt')
                  try:os.remove(localizacao)
                  except: pass
                  savefile(pastaperfil,'listagem2.txt',listagem)
                  ## MD5 ##
                  localizacao=os.path.join(pastaperfil,'listagem2.md5')
                  try:os.remove(localizacao)
                  except: pass
                  savefile(pastaperfil,'listagem2.md5',check)
                  print "BD actualizada"
                  xbmc.executebuiltin("XBMC.Notification(Séries Portuguesas, Conteúdos Actualizados!,'100000')")
            else:
                  print "Ultima BD ja em cache"
      except: xbmc.executebuiltin("XBMC.Notification(Séries Portuguesas, Não conseguiu actualizar para ultima BD,'100000')")            

################################################### MENUS PLUGIN ######################################################

def menu_principal(ligacao):
      if ligacao==1:
            #addDir('Todas as Séries','querotodasasmusicas',1,wtpath + art + 'pasta.png',1,True)
            series('nada')
      elif ligacao==0:
            addDir(traducao(40015),MainURL,None,wtpath + art + 'pasta.png',1,True)
            #addDir("[COLOR gold][B]%s[/B][/COLOR] | Séries Portuguesas" % (traducao(40018)),MainURL,8,wtpath + art + 'pasta.png',6,False)
      addDir('Guardados','all',6,wtpath + art + 'guardados.png',2,True)
      xbmc.executebuiltin("Container.SetViewMode(500)")

def series(url):
      listagem=openfile('listagem2.txt')
      listaseries=re.compile('"sid":"(.+?)","sname":"(.+?)","sdesc":".+?","sthumb":"(.+?)"').findall(listagem)
      for sid,sname,sthumb in listaseries:
            addDir('[B]%s[/B]' % (sname),sid,3,sthumb,len(listaseries),True)

def eplist(url):
      listagem=openfile('listagem2.txt')
      try:vistos = os.listdir(pastavistos)
      except: vistos=[]
      sthumb=re.compile('"sid":"'+url+'","sname":".+?","sdesc":".+?","sthumb":"(.+?)"').findall(listagem)[0]
      sstatus=re.compile('"sid":"'+url+'","sname":".+?","sdesc":".+?","sthumb":".+?","sstatus":"(.+?)"').findall(listagem)[0]
      addLink("[B]Estado da Série:[/B] %s" % sstatus,'nada',sthumb)
      eplist=re.compile('"epid":"'+url+'(.+?)","epext":"(.+?)","epsea":"(.+?)","epnum":"(.+?)","epname":"(.+?)"').findall(listagem)
      for epid,epext,epsea,epnum,epname in eplist:
            filename='%s%s.txt'%(url,epid)
            if filename in vistos: checked=True
            else: checked=False
            addCont('[B]%sx%s[/B]: %s' % (epsea,epnum.zfill(2),epname),'%s%s.%s' % (url,epid,epext),2,sthumb,len(eplist),checked,filename,False)

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40020),MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40021),MainURL,8,wtpath + art + 'defs.png',1,False)

########################################################### PLAYER ################################################

def analyzer(url,name,play=True,offline=False):
      final=''
      mensagemprogresso.create('Séries Portuguesas', traducao(40025))
      mensagemprogresso.update(0)
      from t0mm0.common.net import Net
      net=Net()
      if offline==True:
            filename=os.path.basename(url).split('.')[0]
      else: filename=url.split('.')[0]
      listagem=openfile('listagem2.txt')
      eplist=re.compile('"epid":"'+filename+'","epext":".+?","epsea":"(.+?)","epnum":"(.+?)","epname":"(.+?)"').findall(listagem)[0]
      listaseries=re.compile('"sid":".+?","sname":"(.+?)","sdesc":".+?","sthumb":"'+thumb+'"').findall(listagem)[0]

      season=eplist[0]
      episode=eplist[1]
      epname=eplist[2]
      seriesname=listaseries

      if offline==True:
            linkfinal=os.path.join(pastaguardados,url)
            mensagemprogresso.close()
            comecarvideo(name,linkfinal,season,episode,epname,seriesname,filename)
            return
      
      conteudo=abrir_url_cookie(MainURL + str(entrada.decode('rot13')) + 'others/' + url)
      
      if re.search('Pode acontecer que a mensagem de confirma',conteudo):
            mensagemok('Séries Portuguesas','Necessitas de activar a tua conta abelhas.')
            return
      try:
            
            fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            form_d = {'fileId':fileid,'__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
            endlogin=MainURL + 'action/License/Download'
            print endlogin
            final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
      except:
            mensagemok('Séries Portuguesas','Ficheiro indisponivel.')

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
                  mensagemok('Séries Portuguesas',traducao(40026))
                  return
            else:
                  linkfinal=''
                  mensagemok('Séries Portuguesas',traducao(40027))
                  print str(final)
                  print str(linkfinal) 
                  return

      mensagemprogresso.close()
      if play==True: comecarvideo(name,linkfinal,season,episode,epname,seriesname,filename)
      else: return (url),linkfinal

def guardados():
      listagem=openfile('listagem2.txt')
      #listagem = unicode(listagem, errors='ignore')
      try: guardados = os.listdir(pastaguardados)
      except: guardados=[]
      try:vistos = os.listdir(pastavistos)
      except: vistos=[]
      for referenciaswithext in guardados:
            referencias=referenciaswithext.replace('.mp4','').replace('.avi','')
            filename='%s.txt'%(referencias)
            if filename in vistos: checked=True
            else: checked=False
            epinfo=re.compile('"epid":"'+referencias+'","epext":".+?","epsea":"(.+?)","epnum":"(.+?)","epname":"(.+?)"').findall(listagem)[0]
            sname=re.compile('"sid":"'+referencias[0:3]+'","sname":"(.+?)","sdesc":".+?","sthumb":"(.+?)"').findall(listagem)[0]
            addCont('[B]%s[/B] %sx%s: %s' % (sname[0],epinfo[0],epinfo[1].zfill(2),epinfo[2]),os.path.join(pastaguardados,referenciaswithext),8,sname[1],len(guardados),checked,referenciaswithext,False,download=False)
      
def guardarepisodio(url):
      if not os.path.exists(pastaguardados):
          os.makedirs(pastaguardados)
      nomeficheiro,url=analyzer(url,name,play=False)
      pathf=os.path.join(pastaguardados,nomeficheiro)
      if not os.path.exists(pathf):
            downloader(url,pathf)
            xbmc.executebuiltin("XBMC.Notification(Séries Portuguesas,Episódio Guardado,'500000',"+iconpequeno.encode('utf-8')+")")
      else: xbmc.executebuiltin("XBMC.Notification(Séries Portuguesas,Episódio já está guardado,'500000',"+iconpequeno.encode('utf-8')+")")

def apagarepisodio(url):
      favorito=os.path.join(pastaguardados,url)
      os.remove(favorito)
      xbmc.executebuiltin("XBMC.Notification(Séries Portuguesas,Episódio removido,'500000',"+iconpequeno.encode('utf-8')+")")
      xbmc.executebuiltin("Container.Refresh")


def comecarvideo(name,url,season,episode,epname,seriesname,filename):
        url=url.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>')#.replace('\\','')
        playlist = xbmc.PlayList(1)
        playlist.clear()
        print "Estou a ver a serie " + str(seriesname) + " S" + season + "E" + episode + " - " + epname
      
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
        listitem.setInfo("Video", {"title":epname,"TVShowTitle": seriesname,"Season":int(season),"Episode":int(episode),"type":"episode"})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(url, listitem)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
        player = Player(epid=filename)
        player.play(playlist)
        while player._playbackLock:
              player._trackPosition()
              xbmc.sleep(3500)

        
class Player(xbmc.Player):
      def __init__(self,epid):
            xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            self._playbackLock = True
            self._refInfo = True
            self._totalTime = 999999
            self.epid=epid
            self._lastPos = 0
            self.nomeficheiro=epid + '.txt'
            self.caminhoficheiro=os.path.join(pastatracks, self.nomeficheiro)
            print "Criou o player"
            
      def onPlayBackStarted(self):
            print "Comecou o player"
            self._totalTime = self.getTotalTime()
            #if selfAddon.getSetting('marcadores') == 'true':
            if os.path.exists(self.caminhoficheiro):
                  print "Existe um marcador. A perguntar."
                  bookmark=openfile(self.caminhoficheiro)
                  opcao=xbmcgui.Dialog().yesno("Series Portuguesas", '','Continuar em %s?' % (format_time(float(bookmark))),'', 'Começar de novo', 'Resumir')
                  if opcao: self.seekTime(float(bookmark))
                        
      def onPlayBackStopped(self):
            print "Parou o player"
            self._playbackLock = False
            playedTime = int(self._lastPos)
            watched_values = [.7, .8, .9, .95]
            min_watched_percent = watched_values[int(selfAddon.getSetting('watched-percent'))]
            print 'playedTime / totalTime : %s / %s = %s' % (playedTime, self._totalTime, playedTime/self._totalTime)
            xbmc.sleep(3510)
            if playedTime == 0 and self._totalTime == 999999: raise PlaybackFailed('XBMC falhou a comecar o playback')
            elif ((playedTime/self._totalTime) > min_watched_percent):
                  #if selfAddon.getSetting('marcadores') == 'true':
                  try:os.remove(self.caminhoficheiro)
                  except: pass
                  print "A marcar como visto"
                  savefile(pastavistos,self.nomeficheiro,'')
                  xbmc.executebuiltin("XBMC.Container.Refresh")
            else: print 'Nao atingiu a marca das definicoes. Nao marcou como visto.'

      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'

      def _trackPosition(self):
            try: self._lastPos = self.getTime()
            except: print 'Erro quando estava a tentar definir o tempo de playback'
            #if selfAddon.getSetting('marcadores') == 'true':
            if (self._lastPos>15):
                  savefile(pastatracks,self.nomeficheiro,str(self._lastPos))

class PlaybackFailed(Exception):
      '''XBMC falhou a carregar o stream'''


def format_time(seconds):
	minutes,seconds = divmod(seconds, 60)
	if minutes > 60:
		hours,minutes = divmod(minutes, 60)
		return "%02d:%02d:%02d" % (hours, minutes, seconds)
	else: return "%02d:%02d" % (minutes, seconds)

def mudarvistos(name,url):
      path=os.path.join(pastavistos,url)
      if name=='add': savefile(pastavistos,url,'')
      else:
            try:os.remove(path)
            except: pass
      xbmc.executebuiltin("XBMC.Container.Refresh")

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems([], replaceItems=True) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems([], replaceItems=True) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addCont(name,url,mode,iconimage,total,checked,filename,pasta,download=True):
      contexto=[]
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      if checked==False:
            contexto.append(('Marcar como visto', 'XBMC.RunPlugin(%s?mode=4&url=%s&name=%s)' % (sys.argv[0], filename,'add')))
            liz.setInfo( type="Video", infoLabels={ "Title": name,"overlay":6,"playcount":0} )
      else:
            contexto.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?mode=4&url=%s&name=%s)' % (sys.argv[0], filename,'remove')))
            liz.setInfo( type="Video", infoLabels={ "Title": name,"overlay":7,"playcount":1} )
      if download==True: contexto.append(('Guardar Episódio', 'XBMC.RunPlugin(%s?mode=5&url=%s&name=%s&thumb=%s)' % (sys.argv[0], urllib.quote_plus(url),name,urllib.quote_plus(iconimage))))
      else:contexto.append(('Apagar Episódio', 'XBMC.RunPlugin(%s?mode=7&url=%s&name=%s&thumb=%s)' % (sys.argv[0], urllib.quote_plus(url),name,urllib.quote_plus(iconimage))))
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumb=" + urllib.quote_plus(iconimage)
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
      title="Introduza o ID - Séries Portuguesas"
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
            if erro==True: mensagemok('Séries Portuguesas',str(urllib2.HTTPError(e.url, e.code, traducao(40032), e.hdrs, e.fp)),traducao(40033))
            sys.exit(0)
      except urllib2.URLError, e:
            if erro==True: mensagemok('Séries Portuguesas',traducao(40032)+traducao(40033))
            sys.exit(0)
            
def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.karaokept/addon.xml')
            match=re.compile('name="Karaoke Portugues"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Séries Portuguesas',traducao(40034),traducao(40035),'')
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
            
def downloader(url,dest, mensagem="A fazer download...",useReq = False):
    dp = xbmcgui.DialogProgress()
    dp.create("Séries Portuguesas",mensagem,'')

    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://wallpaperswide.com/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled(): 
                raise Exception("Canceled")                
                dp.close()

            chunk = resp.read(size)
            if not chunk:            
                f.close()
                break

            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)       
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()


params=get_params()
url=None
name=None
mode=None
thumb=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: thumb=urllib.unquote_plus(params["thumb"])
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
elif mode==1: series(url)
elif mode==2: analyzer(url,name)
elif mode==3: eplist(url)
elif mode==4: mudarvistos(name,url)
elif mode==5: guardarepisodio(url)
elif mode==6: guardados()
elif mode==7: apagarepisodio(url)
elif mode==8: analyzer(url,name,offline=True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
