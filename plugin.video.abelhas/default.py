# -*- coding: utf-8 -*-

""" abelhas.pt
    2013 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time
from t0mm0.common.net import Net
net=Net()

####################################################### CONSTANTES #####################################################

versao = '0.0.10'
addon_id = 'plugin.video.abelhas'
MainURL = 'http://abelhas.pt/'
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
username = urllib.quote(selfAddon.getSetting('abelhas-username'))
password = selfAddon.getSetting('abelhas-password')

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

#################################################### LOGIN ABELHAS #####################################################

def login_abelhas():
      print "Sem cookie. A iniciar login"
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
            ok = mensagemok('Abelhas.pt',traducao(40000),traducao(40001))
            entrarnovamente(1)
      else:    
            if re.search('003eA senha indicada n',logintest):
                  mensagemok('Abelhas.pt',traducao(40002))
                  entrarnovamente(1)
            elif re.search('existe. Certifica-te que indicaste o nome correcto.',logintest):
                  mensagemok('Abelhas.pt',traducao(40003))
                  entrarnovamente(1)
            elif re.search(username,logintest):
                  #xbmc.executebuiltin("XBMC.Notification(abelhas.pt,"+traducao(40004)+",'500000',"+iconpequeno.encode('utf-8')+")")
                  net.save_cookies(cookies)
                  menu_principal(1)
            
            elif re.search('Erro',logintest) or link=='Erro':
                  opcao= xbmcgui.Dialog().yesno('abelhas.pt', traducao(40005), "", "",traducao(40006), 'OK')
                  if opcao: menu_principal(0)
                  else: login_abelhas()
                
################################################### MENUS PLUGIN ######################################################

def menu_principal(ligacao):
      if ligacao==1:
            conteudo=clean(abrir_url_cookie('http://abelhas.pt/action/Help'))
            pontos=re.compile('href="/Points.aspx" title="Pontos" rel="nofollow".+?</a><strong>(.+?)</strong>').findall(conteudo)[0]
            mensagens=re.compile('href="/action/PrivateMessage" id="topbarMessage".+?</a><strong>(.+?)</strong>').findall(conteudo)[0]
            transf=re.compile('Transfe.+?ncia.+?<strong>(.+?)</strong>').findall(conteudo)[0]
            addDir(traducao(40007),MainURL,1,wtpath + art + 'filmes.png',1,True)
            addDir(traducao(40008),MainURL,2,wtpath + art + 'series.png',2,True)
            addDir(traducao(40009),MainURL + username,3,wtpath + art + 'series.png',2,True)
            addDir(traducao(40010),'pastas',5,wtpath + art + 'series.png',2,True)
            addDir(traducao(40037),MainURL,9,wtpath + art + 'series.png',2,True)
            addDir(traducao(40011),'pesquisa',7,wtpath + art + 'pesquisa.png',3,True)
            addLink("",'',wtpath + art + 'nothingx.png')
            #addLink("[COLOR blue][B]"+traducao(40012)+ ":[/B][/COLOR] " + mensagens,'',wtpath + art + 'nothingx.png')
            #addLink("[COLOR blue][B]"+traducao(40013)+ ":[/B][/COLOR] " + transf,'',wtpath + art + 'nothingx.png')            
      elif ligacao==0:
            addDir(traducao(40015),MainURL,6,wtpath + art + 'refresh.png',1,True)
            addLink("",'',wtpath + art + 'nothingx.png')
      #if ligacao==1:
      #      disponivel=versao_disponivel()
      #      if disponivel==versao: addLink(traducao(40017) + versao+ ')','',wtpath + art + 'versao_disp.png')
      #      else: addDir(traducao(40016) + versao + ' | ' + traducao(40019) + disponivel,MainURL,13,wtpath + art + 'versao_disp.png',1,False)
      #else: addLink("[COLOR blue][B]%s[/B][/COLOR] %s" % (traducao(40016),versao),'',wtpath + art + 'versao_disp.png')
      if ligacao==1: addLink("[COLOR blue][B]%s:[/B][/COLOR] %s  [COLOR blue][B]%s:[/B][/COLOR] %s" % (traducao(40012),mensagens,traducao(40014),pontos),'',wtpath + art + 'nothingx.png')
      addDir("[COLOR blue][B]%s[/B][/COLOR] | abelhas.pt" % (traducao(40018)),MainURL,8,wtpath + art + 'defs.png',6,True)
      xbmc.executebuiltin("Container.SetViewMode(50)")

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40020),MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40021),MainURL,8,wtpath + art + 'defs.png',1,False)

def topcolecionadores():
      conteudo=clean(abrir_url_cookie('http://abelhas.pt/' + username))
      users=re.compile('<li><div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span></span></a></div>.+?<i>(.+?)</i></li>').findall(conteudo)
      for urluser,nomeuser,thumbuser,nruser in users:
            addDir('[B][COLOR blue]' + nruser + 'º[/B][/COLOR] ' + nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
      xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def abelhasmaisrecentes():
      conteudo=clean(abrir_url_cookie('http://abelhas.pt/action/LastAccounts/MoreAccounts'))
      users=re.compile('<div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span>').findall(conteudo)
      for urluser,nomeuser,thumbuser in users:
            addDir(nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
      xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def pesquisa():
      conteudo=clean(abrir_url_cookie('http://abelhas.pt/action/Help'))
      opcoeslabel=re.compile('<option value=".+?">(.+?)</option>').findall(conteudo)
      opcoesvalue=re.compile('<option value="(.+?)">.+?</option>').findall(conteudo)
      index = xbmcgui.Dialog().select(traducao(40022), opcoeslabel)
      if index > -1:
            caixadetexto('pesquisa',ftype=opcoesvalue[index])
      else:sys.exit(0)

def favoritos():
      conteudo=abrir_url_cookie(MainURL + username)
      chomikid=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
      token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
      
      
      if name==traducao(40037):pagina=1
      else: pagina=int(name.replace("[COLOR blue]Página ",'').replace(' >>>[/COLOR]',''))
      form_d = {'page':pagina,'chomikName':chomikid,'__RequestVerificationToken':token}
      ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
      endlogin=MainURL + 'action/Friends/ShowAllFriends'
      info= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
      info=info.replace('javascript:;','/javascript:;')
      users=re.compile('<div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" />').findall(info)
      for urluser,nomeuser,thumbuser in users:
            addDir(nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
      paginas(info)
      xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')


def proxpesquisa():
    from t0mm0.common.addon import Addon
    addon=Addon('plugin.video.abelhas')
    form_d=addon.load_data('temp.txt')
    ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
    form_d['Page']= form_d['Page'] + 1
    endlogin=MainURL + 'action/SearchFiles/Results'
    net.set_cookies(cookies)
    conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
    addon.save_data('temp.txt',form_d)
    pastas(MainURL + 'action/nada','coco',conteudo=conteudo)

def pastas(url,name,formcont={},conteudo=''):
      
      if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'abelhas.pt', 'Connection': 'keep-alive', 'Referer': 'http://abelhas.pt/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            endlogin=MainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('O ficheiro n&#227;o foi encontrado',conteudo):
                  mensagemok('Abelhas.pt','Sem resultados.')
                  sys.exit(0)
            try:
                  filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  except: ftype='All'
                  #pagina=re.compile('<input name="Page" type="hidden" value="(.+?)" />').findall(conteudo)[0]

                  pagina=1
                  token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]

                  form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
                  from t0mm0.common.addon import Addon
                  addon=Addon('plugin.video.abelhas')
                  addon.save_data('temp.txt',form_d)
                  ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                  endlogin=MainURL + 'action/SearchFiles/Results'
                  conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
            
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))

      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            
            
            
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Abelhas.pt',traducao(40002))
                  sys.exit(0)
            else:
                  pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            
            passwordfolder=caixadetexto('password')
            
            
      
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Abelhas.pt',traducao(40002))
                  sys.exit(0)
            else:
                  pastas_ref(url)
      else:
            try:
                  conta=re.compile('<h3>(.+?)<span>(.+?)</span></h3>').findall(conteudo)[0]
                  nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  addLink('[COLOR blue][B]' + traducao(40023) + nomeconta + '[/B][/COLOR]: ' + conta[0] + conta[1],'',wtpath + art + 'star2.png')
            except: pass

            try:
                  pastas=re.compile('<div id="foldersList">(.+?)</table>').findall(conteudo)[0]
                  seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas)
                  for urlpasta,nomepasta,password in seleccionados:
                        if re.search('<span class="pass">',password): displock=' (' + traducao(40024)+')'
                        else:displock=''
                        addDir(nomepasta + displock,MainURL + urlpasta,3,wtpath + art + 'pasta.png',len(seleccionados),True)
            except: pass
            #contributo mafarricos com alteracoes, ty
            items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)         
            for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items1:
                  extensao=extensao.replace(' ','')
                  tamanhoficheiro=tamanhoficheiro.replace(' ','')
                  if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.RAR' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
                  elif extensao=='.mp3' or extensao=='.MP3' or extensao == '.wma' or extensao=='.WMA' or extensao=='.m3u' or extensao=='.M3U' or extensao=='.flac' or extensao=='.FLAC': thumb=wtpath + art + 'musica.png'
                  elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
                  elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV': thumb=wtpath + art + 'video.png'
                  else:thumb=wtpath + art + 'file.png'
                  tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                  addCont('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,4,tamanhoparavariavel,thumb,len(items1),False)
            #contributo mafarricos com alteracoes, ty
            items2=re.compile('<ul class="borderRadius tabGradientBg">.+?<li><span>(.+?)</span></li>.+?<li><span class="date">(.+?)</span></li></ul></div>.+?<ul>            <li><a href="/(.+?)" class="downloadAction".+?<li class="fileActionsFacebookSend" data-url=".+?" data-title="(.+?)">.+?<span class="bold">.+?</span>(.+?)</a>').findall(conteudo)
            for tamanhoficheiro,dataficheiro,urlficheiro, tituloficheiro,extensao in items2:
                  extensao=extensao.replace(' ','')
                  if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.RAR' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
                  elif extensao=='.mp3' or extensao=='.MP3' or extensao == '.wma' or extensao=='.WMA' or extensao=='.m3u' or extensao=='.M3U' or extensao=='.flac' or extensao=='.FLAC': thumb=wtpath + art + 'musica.png'
                  elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
                  elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV': thumb=wtpath + art + 'video.png'
                  else:thumb=wtpath + art + 'file.png'
                  tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                  addCont('[B]' + tituloficheiro + extensao + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,4,tamanhoparavariavel,thumb,len(items2),False)
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        #isto ta feio
                        items3=re.compile('<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for urlficheiro,tituloficheiro, tamanhoficheiro,dataficheiro in items3:
                              tamanhoficheiro=tamanhoficheiro.replace(' ','')
                              thumb=wtpath + art + 'file.png'
                              tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                              addCont('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,4,tamanhoparavariavel,thumb,len(items2),False)
            
            paginas(conteudo)
            
      xbmc.executebuiltin("Container.SetViewMode(51)")            

def criarplaylist(url,name,formcont={},conteudo=''):
      mensagemprogresso.create('Abelhas.pt', traducao(40049))
      playlist = xbmc.PlayList(1)
      playlist.clear()
      if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'abelhas.pt', 'Connection': 'keep-alive', 'Referer': 'http://abelhas.pt/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            endlogin=MainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('O ficheiro n&#227;o foi encontrado',conteudo):
                  mensagemok('Abelhas.pt','Sem resultados.')
                  sys.exit(0)
            try:
                  filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  except: ftype='All'
                  pagina=1
                  token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
                  form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
                  from t0mm0.common.addon import Addon
                  addon=Addon('plugin.video.abelhas')
                  addon.save_data('temp.txt',form_d)
                  ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                  endlogin=MainURL + 'action/SearchFiles/Results'
                  conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Abelhas.pt',traducao(40002))
                  sys.exit(0)
            else: pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Abelhas.pt',traducao(40002))
                  sys.exit(0)
            else: pastas_ref(url)
      else:
            items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items1: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            items2=re.compile('<ul class="borderRadius tabGradientBg">.+?<li><span>(.+?)</span></li>.+?<li><span class="date">(.+?)</span></li></ul></div>.+?<ul>            <li><a href="/(.+?)" class="downloadAction".+?<li class="fileActionsFacebookSend" data-url=".+?" data-title="(.+?)">.+?<span class="bold">.+?</span>(.+?)</a>').findall(conteudo)
            for tamanhoficheiro,dataficheiro,urlficheiro, tituloficheiro,extensao in items2: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)				  
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        items3=re.compile('<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for urlficheiro,tituloficheiro, tamanhoficheiro,dataficheiro in items3: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
      mensagemprogresso.close()
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

def pastas_ref(url):
      pastas(url,name)

def paginas(link):
      try:
            idmode=3
      
            try:
                  conteudo=re.compile('<div id="listView".+?>(.+?)<div class="filerow fileItemContainer">').findall(link)[0]
                  
            except:
                  try:conteudo=re.compile('<div class="paginator clear searchListPage">(.+?)<div class="clear">').findall(link)[0]
                  except:
                        conteudo=re.compile('<div class="paginator clear friendspager">(.+?)<div class="clear">').findall(link)[0]
                        idmode=9
            try:
                  pagina=re.compile('anterior.+?<a href="/(.+?)" class="right" rel="(.+?)"').findall(conteudo)[0]
                  urlpag=pagina[0]
                  urlpag=urlpag.replace(' ','+')
                  addDir('[COLOR blue]Página ' + pagina[1] + ' >>>[/COLOR]',MainURL + urlpag,idmode,wtpath + art + 'seta.png',1,True)
            except:
                  nrpagina=re.compile('type="hidden" value="([^"]+?)" /><input type="submit" value="p.+?gina seguinte.+?" /></form>').findall(link)[0]
                  addDir('[COLOR blue]Página ' + nrpagina + ' >>>[/COLOR]',MainURL,12,wtpath + art + 'seta.png',1,True)
                  #pass
                  
      
            
      except:
            pass


########################################################### PLAYER ################################################

def analyzer(url,subtitles='',playterm=False,playlistTitle=''):
      if playlistTitle == '': mensagemprogresso.create('Abelhas.pt', traducao(40025))
      linkfinal=''
      if subtitles=='sim': conteudo=abrir_url_cookie(url)
      else:conteudo=abrir_url_cookie(url,erro=False)
      if re.search('Pode acontecer que a mensagem de confirma',conteudo):
            mensagemok('Abelhas.pt','Necessitas de activar a tua conta abelhas.')
            return
      try:
            fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            form_d = {'fileId':fileid,'__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
            endlogin=MainURL + 'action/License/Download'
            final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
      except: pass
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
            if subtitles=='sim':return linkfinal
      except:
            if subtitles=='':
                  if re.search('Por favor tenta baixar este ficheiro mais tarde.',final):
                        mensagemok('Abelhas.pt',traducao(40026))
                        return
                  else:
                        mensagemok('Abelhas.pt',traducao(40027))
                        print str(final)
                        print str(linkfinal) 
                        return
            else: return

      if playlistTitle == '': mensagemprogresso.close()
      linkfinal=linkfinal.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
      if re.search('.jpg',url) or re.search('.png',url) or re.search('.gif',url) or re.search('.bmp',url):
            if re.search('.jpg',url): extfic='temp.jpg'
            elif re.search('.png',url): extfic='temp.png'
            elif re.search('.gif',url): extfic='temp.gif'
            elif re.search('.bmp',url): extfic='temp.bmp'
            fich=os.path.join(pastaperfil, extfic)
            try:os.remove(fich)
            except:pass
            if playterm=="download":fazerdownload(extfic,linkfinal)
            else:fazerdownload(extfic,linkfinal,tipo="fotos")
            xbmc.executebuiltin("SlideShow("+pastaperfil+")")
      elif re.search('.mkv',url) or re.search('.avi',url) or re.search('.wmv',url) or re.search('.mp4',url):
            endereco=legendas(fileid,url)
            if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm,legendas=endereco)
            else: comecarvideo(name,linkfinal,playterm=playterm,legendas=endereco)
      elif re.search('.mp3',url) or re.search('.wma',url):
            if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm)
            else: comecarvideo(name,linkfinal,playterm=playterm)
      else:
            if selfAddon.getSetting('aviso-extensao') == 'true': mensagemok('Abelhas.pt',traducao(40028),traducao(40029),traducao(40030))
            if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm)			
            else: comecarvideo(name,linkfinal,playterm=playterm)

def legendas(moviefileid,url):
      url=url.replace(','+moviefileid,'').replace('.mkv','.srt').replace('.mp4','.srt').replace('.avi','.srt').replace('.wmv','.srt')
      legendas=analyzer(url,subtitles='sim')
      return legendas

def comecarvideo(name,url,playterm,legendas=None):
        playeractivo = xbmc.getCondVisibility('Player.HasMedia')
        if playterm=='download':
              fazerdownload(name,url)
              return
        thumbnail=''
        playlist = xbmc.PlayList(1)
        if not playterm and playeractivo==0: playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        #listitem.setInfo("Video", {"Title":"Balas & Bolinhos","year":2001})
        title='%s' % (name.split('[/B]')[0].replace('[B]',''))

        listitem.setInfo("Video", {"Title":title})
        listitem.setInfo("Music", {"Title":title})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        if playterm <> 'playlist':
              dialogWait = xbmcgui.DialogProgress()
              dialogWait.create('Video', 'A carregar')
        playlist.add(url, listitem)
        if playterm <> 'playlist':		
              dialogWait.close()
              del dialogWait
        if not playterm and playeractivo==0:
              xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
              xbmcPlayer.play(playlist)
        if legendas!=None: xbmcPlayer.setSubtitles(legendas)
        if playterm=='playlist': xbmc.executebuiltin("XBMC.Notification(abelhas.pt,"+traducao(40039)+",'500000',"+iconpequeno.encode('utf-8')+")")

def limparplaylist():
        playlist = xbmc.PlayList(1)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(abelhas.pt,"+traducao(40048)+",'500000',"+iconpequeno.encode('utf-8')+")")

def comecarplaylist():
        playlist = xbmc.PlayList(1)
        if playlist:
              xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
              xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append((traducao(40050), 'XBMC.RunPlugin(%s?mode=15&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40047), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems(contexto, replaceItems=False) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addCont(name,url,mode,tamanho,iconimage,total,pasta):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&tamanhof="+urllib.quote_plus(tamanho)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append((traducao(40038), 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40046), 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40047), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40040), 'XBMC.RunPlugin(%s?mode=11&url=%s&name=%s&tamanhof=%s)' % (sys.argv[0], urllib.quote_plus(url),name,tamanho)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems(contexto, replaceItems=True) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
           
######################################################## DOWNLOAD ###############################################
### THANKS ELDORADO (ICEFILMS) ###
def fazerdownload(name,url,tipo="outros"):
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','').replace(str(tamanhoparavariavel),'')
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      dialog = xbmcgui.Dialog()
      if tipo=="fotos":
            mypath=os.path.join(pastaperfil, vidname)
      else:
            downloadPath = dialog.browse(int(3), traducao(40041),'myprograms')
            if os.path.exists(downloadPath):
                  mypath=os.path.join(downloadPath,vidname)
            else: return

      if os.path.isfile(mypath) is True:
            ok = mensagemok('Abelhas.pt',traducao(40042),'','')
            return False
      else:              
            try:
                  dp = xbmcgui.DialogProgress()
                  dp.create('Abelhas.pt - ' + traducao(40043), '', name)
                  start_time = time.time()
                  try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
                  except:
                        while os.path.exists(mypath): 
                              try: os.remove(mypath); break 
                              except: pass 
                        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): return False 
                        else: raise 
                        return False
                  return True
            except: ok=mensagemok('Abelhas.pt',traducao(40044)); print 'download failed'; return False

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            #e = 'Velocidade: (%.0f Kb/s) ' % kbps_speed
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = traducao(40045) + ': %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
            #if percent=xbmc.executebuiltin("XBMC.Notification(Abelhas.pt,"+ mbs + e + ",'500000',"+iconpequeno+")")
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

######################################################## OUTRAS FUNCOES ###############################################

def caixadetexto(url,ftype=''):
      if url=='pastas': title=traducao(40010) + " - Abelhas.pt"
      elif url=='password': title="Password - Abelhas.pt"
      elif url=='pesquisa': title=traducao(40031) + " - Abelhas.pt"
      else: title="Abelhas.pt"
      keyb = xbmc.Keyboard(selfAddon.getSetting('ultima-pesquisa'), title)
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote_plus(search)
            if url=='pastas': pastas(MainURL + search,name)
            elif url=='password': return search
            elif url=='pesquisa':
                  form_d = {'FileName':encode,'submitSearchFiles':'Procurar','FileType':ftype,'IsGallery':'False'}
                  pastas(MainURL + 'action/SearchFiles',name,formcont=form_d)
            
      else: sys.exit(0)
            
def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def savefile(filename, contents,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal,filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou os temporarios de: %s" % filename

def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None


def abrir_url_cookie(url,erro=True):
      
      
      net.set_cookies(cookies)
      try:
            ref_data = {'Host': 'abelhas.pt', 'Connection': 'keep-alive', 'Referer': 'http://abelhas.pt/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            link=net.http_POST(url,ref_data).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            if erro==True: mensagemok('Abelhas.pt',str(urllib2.HTTPError(e.url, e.code, traducao(40032), e.hdrs, e.fp)),traducao(40033))
            sys.exit(0)
      except urllib2.URLError, e:
            if erro==True: mensagemok('Abelhas.pt',traducao(40032)+traducao(40033))
            sys.exit(0)
            
def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.abelhas/addon.xml')
            match=re.compile('name="Abelhas.pt"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Abelhas.pt',traducao(40034),traducao(40035),'')
            match=traducao(40036)
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
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

params=get_params()
url=None
name=None
mode=None
tamanhoparavariavel=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: tamanhoparavariavel=urllib.unquote_plus(params["tamanhof"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Name: "+str(tamanhoparavariavel)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      login_abelhas()
elif mode==1: topcolecionadores()
elif mode==2: abelhasmaisrecentes()
elif mode==3: pastas(url,name)
elif mode==4: analyzer(url)
elif mode==5: caixadetexto(url)
elif mode==6: login_abelhas()
elif mode==7: pesquisa()
elif mode==8: selfAddon.openSettings()#sacarficheiros()
elif mode==9: favoritos()
elif mode==10: analyzer(url,subtitles='',playterm='playlist')
elif mode==11: analyzer(url,subtitles='',playterm='download')
elif mode==12: proxpesquisa()
elif mode==13: comecarplaylist()
elif mode==14: limparplaylist()
elif mode==15: criarplaylist(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
