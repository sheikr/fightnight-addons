# -*- coding: utf-8 -*-

""" wareztuga.tv
    2014 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,cookielib,urllib,urllib2,os,re,sys,socket
addon_id = 'plugin.video.wt'

####################################################### CONSTANTES #####################################################

versao = '0.4.12'
MainURL = 'http://www.wareztuga.tv/'
art = '/resources/art/'
ListMovieURL = 'movies.php'; SingleMovieURL = 'movie.php'
ListSerieURL = 'series.php'; SingleSerieURL = 'serie.php'
AccountItemURL = 'account.php'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'logo32.png'
traducaoma= selfAddon.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
pastafavoritos = os.path.join(pastaperfil, "favoritos")
pastacaptcha = os.path.join(pastaperfil, "captcha")
cookie_rd = os.path.join(pastaperfil, "cookierdv4.lwp")
cookie_wt = os.path.join(pastaperfil, "cookiewt.lwp")
cookie_un = os.path.join(pastaperfil, "cookieun.lwp")
username = urllib.quote(selfAddon.getSetting('wareztuga-username'))
password = urllib.quote(selfAddon.getSetting('wareztuga-password'))
usernameunli=selfAddon.getSetting('unrestrict-username')
passwordunli = selfAddon.getSetting('unrestrict-password')
if not os.path.exists(pastacaptcha):
      os.makedirs(pastacaptcha)

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

#################################################### LOGIN WAREZTUGA #####################################################

def login_wareztuga():
      print "Sem cookie. A iniciar login"
      from t0mm0.common.net import Net
      net=Net()
      try:logintest= net.http_GET(MainURL + "login.ajax.php?username=%s&password=%s"%(username,password)).content
      except: logintest = 'Erro'
      print "Estado do login: " + logintest; print "Username: " + username
      if selfAddon.getSetting("debug-mode2") == "true": print "Password: " + password; print "URL Completo: " + MainURL + "login.ajax.php?username=" + username + "&password=" + password
      if selfAddon.getSetting('wareztuga-username')== '': ok = mensagemok(traducao(40005),traducao(40006),traducao(40007),traducao(40008)); entrarnovamente(1)
      else:    
            if re.search('0',logintest):
                  #xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+ traducao(40009) + ",'500000',"+iconpequeno.encode('utf-8')+")")
                  if selfAddon.getSetting('advancedsettings-import') == 'true': advancedxml(url)
                  net.save_cookies(cookie_wt)
                  #menu_principal_new()
                  menu_principal(1)
            elif re.search('1',logintest): ok = mensagemok(traducao(40005),traducao(40011)); entrarnovamente(1)
            elif re.search('2',logintest): ok = mensagemok(traducao(40005),traducao(40010)); entrarnovamente(1)
            elif re.search('Oops',logintest):
                  opcao= xbmcgui.Dialog().yesno(traducao(40123), traducao(40002), "", "",traducao(40182), 'OK')
                  if opcao: menu_principal(0)
                  else: login_wareztuga()
            elif re.search('Erro',logintest):
                  opcao= xbmcgui.Dialog().yesno(traducao(40123), traducao(40136), "", "",traducao(40182), 'OK')
                  if opcao: menu_principal(0)
                  else: login_wareztuga()
                
################################################### MENUS PLUGIN ######################################################

def menu_principal(ligacao):
      #if selfAddon.getSetting("mensagemfb2") == "true":
      #      ok = mensagemok('wareztuga.tv',traducao(40170), traducao(40171),'http://fb.com/xxxxxxxxxx')
      #      selfAddon.setSetting('mensagemfb2',value='false')
      if ligacao==1:
            addDir(traducao(40012),MainURL,1,wtpath + art + 'filmes.png',1,True)
            addDir(traducao(40013),'series',2,wtpath + art + 'series.png',2,True)
            addDir(traducao(40215),'animes',2,wtpath + art + 'animacao.png',2,True)
            addDir(traducao(40031),MainURL + ListMovieURL,16,wtpath + art + 'pesquisa.png',3,True)
            new=''
            if selfAddon.getSetting("mostrarnotificacoes") == "true":
                  try:
                        notifop=abrir_url_cookie(MainURL + 'faq.php')
                        notif=re.compile('<a href="notifications.php" class=".+?"><span .+?></span><span>(.+?)</span>').findall(notifop)[0]
                        if notif!='0': new='[COLOR yellow][B] (' + notif + ')[/B][/COLOR]'
                  except: pass
            seguirserie()
            addDir('[B][COLOR white]' + traducao(40015) + '[/COLOR][/B]' + new,MainURL,36,wtpath + art + 'biografia.png',4,True)
            #addDir('[B][COLOR white]' + 'Lista de Atalhos' + '[/COLOR][/B]',MainURL,23,wtpath + art + 'biografia.png',4,True)
            addDir('[B][COLOR white]' + traducao(40177) + '[/COLOR][/B]',MainURL,15,wtpath + art + 'biografia.png',5,True)
      elif ligacao==0:
            addDir(traducao(40183),MainURL,28,wtpath + art + 'refresh.png',1,True)
            addDir('[B][COLOR white]' + traducao(40137) + '[/COLOR][/B]',MainURL,9,wtpath + art + 'series.png',1,False)
      addLink("",'',wtpath + art + 'nothingx.png')
      if ligacao==1:
            disponivel=versao_disponivel()
            if disponivel==versao: addLink(traducao(40158) + versao+ ')','',wtpath + art + 'versao_disp.png')
            else: addDir(traducao(40159) + versao + ' | ' + traducao(40160) + disponivel,MainURL,13,wtpath + art + 'versao_disp.png',1,False)
      else: addLink(traducao(40161) + versao,'',wtpath + art + 'versao_disp.png')
      addDir(traducao(40018) + " | [COLOR blue][B]wareztuga.tv[/B][/COLOR]",MainURL,27,wtpath + art + 'defs.png',6,True)
      vista_menus()

def menu_conta():
      link=abrir_url_cookie(MainURL + 'faq.php')
      infoconta=re.compile('<a href="account.php" class="avatar"><img src="(.+?)" alt="(.+?)" />').findall(link)[0]
      notificacoes=re.compile('<a href="notifications.php" class=".+?"><span .+?></span><span>(.+?)</span>').findall(link)[0]
      favoritos=re.compile('<a href=".+?" class="faves"><span class="icon"></span><span>(.+?)</span>').findall(link)[0]
      agendados=re.compile('<a href=".+?" class="agends"><span class="icon"></span><span>(.+?)</span>').findall(link)[0]
      if notificacoes!='0': notific='[B][COLOR yellow]' + traducao(40032) + '[/B] ' + notificacoes + '[/COLOR]'
      else: notific='[B][COLOR white]' + traducao(40032) + '[/COLOR][/B] ' + notificacoes
      addDir(notific,MainURL + 'notifications.ajax.php',10,wtpath + art + 'refresh.png',1,True)
      addLink('[B][COLOR white]' + traducao(40033) + '[/COLOR][/B] ' + favoritos,favoritos,wtpath + art + 'favoritos.png')
      addDir(traducao(40034),MainURL + 'accountMedia.ajax.php?p=1&action=faved&cat=movies&order=date',30,wtpath + art + 'favoritos.png',1,True)
      addDir(traducao(40035),MainURL + 'accountMedia.ajax.php?p=1&action=faved&cat=series&order=date',30,wtpath + art + 'favoritos.png',1,True)
      addLink("",'',wtpath + art + 'nothingx.png')
      addLink('[B][COLOR white]' + traducao(40036) + '[/COLOR][/B] ' + agendados,agendados,wtpath + art + 'agendados.png')
      addDir(traducao(40037),MainURL + 'accountMedia.ajax.php?p=1&action=cliped&cat=movies&order=date',30,wtpath + art + 'agendados.png',1,True)
      addDir(traducao(40038),MainURL + 'accountMedia.ajax.php?p=1&action=cliped&cat=episodes&order=date',30,wtpath + art + 'agendados.png',1,True)
      addDir(traducao(40039),MainURL + 'accountMedia.ajax.php?p=1&action=subscribed&cat=series&order=date',30,wtpath + art + 'agendados.png',1,True)
      addLink("",'',wtpath + art + 'nothingx.png')
      addLink('[B][COLOR white]' + traducao(40040) + '[/COLOR][/B] ' + infoconta[1],infoconta[1],MainURL + infoconta[0])      
      vista_menus()

def menu_extra():
      addDir('[COLOR white]' + traducao(40137) + '[/COLOR]',MainURL,9,wtpath + art + 'series.png',1,False)
      addDir('[COLOR white]' + traducao(40172) + '[/COLOR]',MainURL,14,wtpath + art + 'agendados.png',1,True)
      addDir(traducao(40019),MainURL + "requestsList.ajax.php?p=1&type=movies&order=requests",34,wtpath + art + 'todos_os_filmes.png',1,True)
      addDir(traducao(40020),MainURL + "requestsList.ajax.php?p=1&type=series&order=requests",34,wtpath + art + 'todas_as_series.png',1,True)
      #addDir(traducao(40021),MainURL + "",34,wtpath + art + 'todas_as_series.png',1,True)
      addDir(traducao(40153),MainURL + 'newepisodes',16,wtpath + art + 'pesquisa.png',1,False)
      vista_menus()

def menu_filmes():
      addDir(traducao(40022),MainURL + 'pagination.ajax.php?p=1&order=name&mediaType=movies',3,wtpath + art + 'todos_os_filmes.png',1,True)
      addDir(traducao(40229),MainURL + 'pagination.ajax.php?p=1',19,wtpath + art + 'refresh.png',1,False)
      addDir(traducao(40023),MainURL + 'pagination.ajax.php?p=1&order=date&mediaType=movies',3,wtpath + art + 'ultimos_filmes_adicionados.png',1,True)
      addDir(traducao(40225),MainURL + 'pagination.ajax.php?p=1&order=rate&mediaType=movies',3,wtpath + art + 'filmes_destaque.png',1,True)
      addDir(traducao(40024),MainURL + 'pagination.ajax.php?p=1&btn=moviesfeatured&mediaType=movies',3,wtpath + art + 'filmes_destaque.png',1,True)
      #addDir('Listas [B][COLOR red]Novo![/COLOR][/B]','filmes',26,wtpath + art + 'agendados.png',1,True)
      addDir(traducao(40025),MainURL + 'pagination.ajax.php?p=1&order=views&mediaType=movies',3,wtpath + art + 'filmes_mais_vistos.png',1,True)
      addDir(traducao(40026),MainURL + 'pagination.ajax.php?p=1&btn=moviesrecommended&mediaType=movies',3,wtpath + art + 'filmes_recomendados.png',1,True)      
      addDir(traducao(40029),MainURL + ListMovieURL,11,wtpath + art + 'categoria.png',1,True)
      addDir(traducao(40030),MainURL + ListMovieURL,12,wtpath + art + 'ano.png',1,True)
      addDir('Multi-filtro',MainURL + ListMovieURL,39,wtpath + art + 'categoria.png',1,True)
      #addDir('filmes',MainURL + 'pagination.ajax.php?p=1&order=date&mediaType=movies',32,wtpath + art + 'ano.png',1,True)
      vista_menus()

def seguirserie():
      try:
            content=openfile('following.txt')
            serie=re.compile('"name":"(.+?)","url":"(.+?)"').findall(content)[0]
            seasonnumb=serie[1].split('&season=')[1]
            addTemp("[COLOR white][B]A seguir série[/B][/COLOR] (%s T%s)" % (serie[0],seasonnumb),MainURL + serie[1],7,wtpath + art + seasonnumb + '.png',1,True)
      except: pass

def instrucoeslibrary():
      mensagemaviso('Bem vindo ao modo biblioteca!\n\nEsta é a nova funcionalidade disponivel neste addon. Com esta função passa a ser possível ter o conteúdo do wareztuga na vossa biblioteca local. Com esta funcionalidade tem um acesso mais rápido aos conteúdos do site.\n\n Para começar devem activar as opções e efectuar uma actualização do conteúdo.\n\nDe seguida devem ir a Videos->Ficheiros->Adicionar Vídeos e adicionar a pasta onde se encontra a base de dados do wareztuga.\n\n[B][COLOR white]Pasta Inicial -> userdata -> addon_data -> plugin.video.wt -> Biblioteca->Filmes ou Séries e só depois confirmar[/B] (pasta defeito, se alteraram nas definições é a que escolheram)[/COLOR]\n\nDe seguida devem modificar as definições consoante a pasta que escolheram! Podem ir a configurações e definir o idioma que desejam obter para a biblioteca. Caso desejem ter séries e filmes na biblioteca, devem repetir o passo para o tipo de conteúdo em falta!\n\nO addon vai apenas verificar novos episódios nas séries subscritas e actualiza automaticamente a biblioteca. A verificação automática é feito conforme o periodo definido.')
      
def instrucoes9kw():
      mensagemaviso('O 9kw.eu é um site que permite que utilizadores resolvam o nosso captcha, bem como nos resolvamos os de outros utilizadores através de um sistema de créditos. Para utilizarem este serviço, devem criar uma key no site e preencher nas definições deste addon.\n\n\n1- Registar no site: https://www.9kw.eu/register.html\n\n2 - Activar a conta com o email recebido.\n\n3- Fazer login.\n\n4 - Aceder a https://www.9kw.eu/index.cgi?action=userapinew&source=api\n\n5 - Apontar a key da api criada e inserir nas settings do addon.\n\nAdicionalmente:\n\n6 - Resolver captchas em https://www.9kw.eu/usercaptcha.html para obter crédito para que nos sejam resolvidas as nossas captchas.')

def glib(name,url,silent=False):
      algumamudanca=False
      print "A Iniciar processo de lib"
      if silent==False:mensagemprogresso.create('wareztuga.tv', 'Aguarde...')
      else: xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,A verificar novos episódios,'500000',"+iconpequeno.encode('utf-8')+")")

      if selfAddon.getSetting('lib-firstrun2') == 'true': selfAddon.setSetting('lib-firstrun2',value='false')
      import xbmcvfs
      biblioteca=xbmc.translatePath(selfAddon.getSetting('lib-basefolder')).decode('utf-8')
      if not os.path.exists(biblioteca): os.makedirs(biblioteca)

      filmespath=os.path.join(os.path.join(biblioteca,'Filmes'))
      if not os.path.exists(filmespath): os.makedirs(filmespath)
      seriespath=os.path.join(biblioteca,'Series')
      if not os.path.exists(seriespath): os.makedirs(seriespath)
      '''
      if name=='filmes':
            url=MainURL + 'pagination.ajax.php?p=1&order=date&mediaType=movies'
            link=abrir_url(url)
            ultimapagina=re.compile('...</span><a href="javascript: moviesList.+?pagination.ajax.php.+?p=(.+?)&').findall(link)[0]
            if silent==False: mensagemprogresso.update(0, 'A criar lista')
            for i in xrange(1,int(ultimapagina)+1):
            #for i in xrange(1,3):
                  print i
                  if silent==False:mensagemprogresso.update(0,'A criar lista','Página %s de %s' % (i,ultimapagina))
                  urlpagina=MainURL + 'pagination.ajax.php?p=%s&order=date&mediaType=movies' % (i)
                  link=clean(abrir_url(urlpagina))
                  info=re.compile('<a href="movie.php(.+?)"><img src=".+?" alt=".+?" /><div class="thumb-effect" title=".+?"></div></a></div></div><div class="movie-info"><a href=".+?" class="movie-name">.+?</a><div class="clear"></div><div class="movie-detailed-info"><div class="detailed-aux" style=".+?"><span class="genre">.+?</span>.+?year.+?</span>(.+?)<span>.+?</span></span><span class="original-name"> - "(.+?)"</span>').findall(link)
                  #print info
                  #print link
                  for urlfilme,ano,nomeingles in info:
                        nomeingles=nomeingles.replace('[B]','').replace('[/B]','').replace('\\','').replace('</div><div class="officialSubs">','')
                        nomeingles = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  nomeingles)
                        conteudo=sys.argv[0]+"?url="+urllib.quote_plus(MainURL + SingleMovieURL + urlfilme)+"&mode=5&name="+urllib.quote_plus(nomeingles)
                        nomeficheiro=nomeingles + ' _' + str(ano) + '_.strm'
                        savefile(filmespath,nomeficheiro,conteudo)
      '''
      if name=='umfilme':
            link=clean(abrir_url_cookie(url))
            nomeingles=re.compile('<span class="original-name">- "(.+?)"</span>').findall(link)[0]
            ano=re.compile('<span class="year"><span> \(</span>(.+?)<span>').findall(link)[0]
            nomeingles=nomeingles.replace('[B]','').replace('[/B]','').replace('\\','').replace('</div><div class="officialSubs">','')
            nomeingles = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  nomeingles)
            conteudo=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=5&name="+urllib.quote_plus(nomeingles)
            nomeficheiro=nomeingles + ' _' + str(ano) + '_.strm'
            savefile(filmespath,nomeficheiro,conteudo)
            algumamudanca=True
      
      if name=='subs':
            print "A Iniciar processo de subscricoes"
            url=MainURL + 'accountMedia.ajax.php?p=1&action=subscribed&cat=series&order=date'
            link=clean(abrir_url_cookie(url))
            try:ultimapagina=re.compile("""><a href="javascript: myAccount\('accountMedia.ajax.php\?p=(.+?)&""").findall(link)[-1:][0]
            except:ultimapagina=1
            if silent==False: mensagemprogresso.update(0, 'A criar lista','A espera varia consoante o número de séries subscritas.')
            for i in xrange(1,int(ultimapagina)+1):
                  url=MainURL + 'accountMedia.ajax.php?p=%s&action=subscribed&cat=series&order=date' % (i)
                  link=clean(abrir_url_cookie(url))
                  if silent==False: mensagemprogresso.update(0, 'A criar lista (página %s de %s)' % (i,ultimapagina),'A espera varia consoante o número de séries subscritas.')
                  conteudo=re.compile("""<div id=".+?" class=".+?"><a href="serie.php(.+?)" title="(.+?)">""").findall(link)
                  for urlserie,nomeingles in conteudo:
                        nomeingles=nomeingles.replace('[B]','').replace('[/B]','').replace('\\','').replace('</div><div class="officialSubs">','')
                        nomeingles = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  nomeingles)
                        pastaserie=os.path.join(seriespath,nomeingles)
                        urlbase=MainURL + SingleSerieURL + urlserie
                        link=abrir_url_cookie(urlbase)
                        numerowt=re.compile('<div class="episodes-number"><span>(.+?)</span>').findall(clean(link))[0]
                        numerobiblio=openfile('epnr.txt',pastaficheiro=os.path.join(seriespath,nomeingles))
                        if numerowt!=numerobiblio:
                              algumamudanca=True
                              if not os.path.exists(pastaserie): os.makedirs(pastaserie)
                              match=re.compile('<div id="season.+?" class="season"><a href=".+?">(.+?)</a></div>').findall(link)
                              for seasonnum in match:
                                    link=clean(abrir_url_cookie(urlbase + '&season=' + seasonnum))
                                   #print link
                                    episodelist=re.compile('<div class="slide-content-bg">(.+?)<input type="hidden" id="raterDefault"').findall(link)[0]
                                    indiv=re.compile('<a href="serie.php(.+?)"><img src=".+?" alt=".+?" /><div class="thumb-shadow"></div><div class="thumb-effect"></div><div class="episode-number">(.+?)</div></a>').findall(episodelist)
                                    for urlep, epnumber in indiv:
                                          epnumber=epnumber.replace('</div><div class="officialSubs">','')
                                          conteudo=sys.argv[0]+"?url="+urllib.quote_plus(MainURL + SingleSerieURL + urlep)+"&mode=5&name="+urllib.quote_plus(nomeingles)
                                          nomeficheiro='%s S%sE%s.strm' % (nomeingles, seasonnum,epnumber)
                                          savefile(pastaserie,nomeficheiro,conteudo)
                              savefile(pastaserie,'epnr.txt',numerowt)
            
      #xbmc.executebuiltin("CleanLibrary(video)")
      print "Concluido processo de Lib"
      if silent==False:
            mensagemprogresso.close()
            if algumamudanca==True:
                  if not xbmc.getCondVisibility('Library.IsScanningVideo'): xbmc.executebuiltin("UpdateLibrary(video)")
      else:
            if algumamudanca==False: xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,Nenhum episódio novo,'500000',"+iconpequeno.encode('utf-8')+")")
            else:
                  xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,A actualizar biblioteca,'500000',"+iconpequeno.encode('utf-8')+")")
                  if not xbmc.getCondVisibility('Library.IsScanningVideo'): xbmc.executebuiltin("UpdateLibrary(video)")
      
      
def menu_series(url):
      addDir(traducao(40081),MainURL + 'pagination.ajax.php?p=1&order=name&mediaType=' + url,4,wtpath + art + 'todas_as_series.png',1,True)
      addDir(traducao(40082),MainURL + 'pagination.ajax.php?p=1&order=date&mediaType=' + url,4,wtpath + art + 'ultimas_series_adicionadas.png',1,True)
      addDir(traducao(40226),MainURL + 'pagination.ajax.php?p=1&order=rate&mediaType=' + url,4,wtpath + art + 'series_recomendadas.png',1,True)
      #addDir('Listas [B][COLOR red]Novo![/COLOR][/B]',url,26,wtpath + art + 'agendados.png',1,True)
      addDir(traducao(40083),MainURL + 'pagination.ajax.php?p=1&btn=seriesrunning&mediaType=' + url,17,wtpath + art + 'series_em_exibicao.png',1,True)
      addDir(traducao(40084),MainURL + 'pagination.ajax.php?p=1&btn=seriescompleted&mediaType=' + url,4,wtpath + art + 'series_completas.png',1,True)
      addDir(traducao(40085),MainURL + 'pagination.ajax.php?p=1&order=views&mediaType=' + url,4,wtpath + art + 'series_mais_vistas.png',1,True)
      addDir(traducao(40086),MainURL + 'pagination.ajax.php?p=1&btn=seriesrecommended&mediaType=' + url,4,wtpath + art + 'series_recomendadas.png',1,True)
      addDir(traducao(40029),MainURL + url + '.php',11,wtpath + art + 'categoria.png',1,True)
      addDir(traducao(40030),MainURL + url + '.php',12,wtpath + art + 'ano.png',1,True)
      addDir('Multi-filtro',MainURL + url + '.php',39,wtpath + art + 'categoria.png',1,True)
      #addDir('subs',MainURL + 'pagination.ajax.php?p=1&order=date&mediaType=movies',32,wtpath + art + 'ano.png',1,True)
      vista_menus()
          
def menu_categoria(url):
      if re.search('animes',url): referencia='&mediaType=animes';modo=4
      elif re.search('series',url): referencia='&mediaType=series';modo=4      
      elif re.search('movies',url): referencia='&mediaType=movies';modo=3
      addDir(traducao(40091),MainURL + 'pagination.ajax.php?p=1&order=date&genres=1' + referencia,modo,wtpath + art + 'accao.png',1,True)
      addDir(traducao(40092),MainURL + 'pagination.ajax.php?p=1&order=date&genres=17' + referencia,modo,wtpath + art + 'animacao.png',1,True)
      addDir(traducao(40093),MainURL + 'pagination.ajax.php?p=1&order=date&genres=4' + referencia,modo,wtpath + art + 'aventura.png',1,True)
      addDir(traducao(40094),MainURL + 'pagination.ajax.php?p=1&order=date&genres=5' + referencia,modo,wtpath + art + 'biografia.png',1,True)
      addDir(traducao(40095),MainURL + 'pagination.ajax.php?p=1&order=date&genres=6' + referencia,modo,wtpath + art + 'comedia.png',1,True)
      addDir(traducao(40096),MainURL + 'pagination.ajax.php?p=1&order=date&genres=2' + referencia,modo,wtpath + art + 'crime.png',1,True)
      addDir(traducao(40097),MainURL + 'pagination.ajax.php?p=1&order=date&genres=21' + referencia,modo,wtpath + art + 'desporto.png',1,True)
      addDir(traducao(40098),MainURL + 'pagination.ajax.php?p=1&order=date&genres=18' + referencia,modo,wtpath + art + 'documentario.png',1,True)
      addDir(traducao(40099),MainURL + 'pagination.ajax.php?p=1&order=date&genres=3' + referencia,modo,wtpath + art + 'drama.png',1,True)
      addDir(traducao(40100),MainURL + 'pagination.ajax.php?p=1&order=date&genres=7' + referencia,modo,wtpath + art + 'familiar.png',1,True)
      addDir(traducao(40101),MainURL + 'pagination.ajax.php?p=1&order=date&genres=8' + referencia,modo,wtpath + art + 'fantasia.png',1,True)
      addDir(traducao(40102),MainURL + 'pagination.ajax.php?p=1&order=date&genres=14' + referencia,modo,wtpath + art + 'ficcao_cientifica.png',1,True)
      addDir(traducao(40103),MainURL + 'pagination.ajax.php?p=1&order=date&genres=15' + referencia,modo,wtpath + art + 'guerra.png',1,True)
      addDir(traducao(40104),MainURL + 'pagination.ajax.php?p=1&order=date&genres=9' + referencia,modo,wtpath + art + 'historia.png',1,True)
      addDir(traducao(40105),MainURL + 'pagination.ajax.php?p=1&order=date&genres=13' + referencia,modo,wtpath + art + 'misterio.png',1,True)
      addDir(traducao(40106),MainURL + 'pagination.ajax.php?p=1&order=date&genres=11' + referencia,modo,wtpath + art + 'musical.png',1,True)
      addDir(traducao(40107),MainURL + 'pagination.ajax.php?p=1&order=date&genres=12' + referencia,modo,wtpath + art + 'romance.png',1,True)
      addDir(traducao(40108),MainURL + 'pagination.ajax.php?p=1&order=date&genres=10' + referencia,modo,wtpath + art + 'terror.png',1,True)
      addDir(traducao(40109),MainURL + 'pagination.ajax.php?p=1&order=date&genres=16' + referencia,modo,wtpath + art + 'thriller.png',1,True)
      addDir(traducao(40110),MainURL + 'pagination.ajax.php?p=1&order=date&genres=20' + referencia,modo,wtpath + art + 'western.png',1,True)
      vista_menus()

def menu_ano(url):
      if re.search('animes',url): referencia='&mediaType=animes';modo=4
      elif re.search('series',url): referencia='&mediaType=series';modo=4
      elif re.search('movies',url): referencia='&mediaType=movies';modo=3
      addDir("2015",MainURL + 'pagination.ajax.php?p=1&order=date&years=2015' + referencia,modo,wtpath + art + '2015.png',1,True)
      addDir("2014",MainURL + 'pagination.ajax.php?p=1&order=date&years=2014' + referencia,modo,wtpath + art + '2014.png',1,True)
      addDir("2013",MainURL + 'pagination.ajax.php?p=1&order=date&years=2013' + referencia,modo,wtpath + art + '2013.png',1,True)
      addDir("2012",MainURL + 'pagination.ajax.php?p=1&order=date&years=2012' + referencia,modo,wtpath + art + '2012.png',1,True)
      addDir("2011",MainURL + 'pagination.ajax.php?p=1&order=date&years=2011' + referencia,modo,wtpath + art + '2011.png',1,True)
      addDir("2010",MainURL + 'pagination.ajax.php?p=1&order=date&years=2010' + referencia,modo,wtpath + art + '2010.png',1,True)
      addDir("2009",MainURL + 'pagination.ajax.php?p=1&order=date&years=2009' + referencia,modo,wtpath + art + '2009.png',1,True)
      addDir("2008",MainURL + 'pagination.ajax.php?p=1&order=date&years=2008' + referencia,modo,wtpath + art + '2008.png',1,True)
      addDir("2007",MainURL + 'pagination.ajax.php?p=1&order=date&years=2007' + referencia,modo,wtpath + art + '2007.png',1,True)
      addDir("2006",MainURL + 'pagination.ajax.php?p=1&order=date&years=2006' + referencia,modo,wtpath + art + '2006.png',1,True)
      addDir("2000-2005",MainURL + 'pagination.ajax.php?p=1&order=date&years=2000' + referencia,modo,wtpath + art + '2000-2005.png',1,True)
      addDir("1990-1999",MainURL + 'pagination.ajax.php?p=1&order=date&years=1990' + referencia,modo,wtpath + art + '1990-1999.png',1,True)
      addDir("1980-1989",MainURL + 'pagination.ajax.php?p=1&order=date&years=1980' + referencia,modo,wtpath + art + '1980-1989.png',1,True)
      addDir("1970-1979",MainURL + 'pagination.ajax.php?p=1&order=date&years=1970' + referencia,modo,wtpath + art + '1970-1979.png',1,True)
      addDir("1960-1969",MainURL + 'pagination.ajax.php?p=1&order=date&years=1960' + referencia,modo,wtpath + art + '1960-1969.png',1,True)
      addDir("1950-1959",MainURL + 'pagination.ajax.php?p=1&order=date&years=1950' + referencia,modo,wtpath + art + '1950-1959.png',1,True)
      addDir("1900-1949",MainURL + 'pagination.ajax.php?p=1&order=date&years=1900' + referencia,modo,wtpath + art + '1900-1949.png',1,True)
      vista_menus()

def multifiltro():
      categorias=[traducao(40330),traducao(40091),traducao(40092),traducao(40093),traducao(40094),traducao(40095),traducao(40096),traducao(40097),traducao(40098),traducao(40099),traducao(40100),traducao(40101),traducao(40102),traducao(40103),traducao(40104),traducao(40105),traducao(40106),traducao(40107),traducao(40108),traducao(40109),traducao(40110)]
      catnumb=['0','1','17','4','5','6','2','21','18','3','7','8','14','15','9','13','11','12','10','16','20']
      index = xbmcgui.Dialog().select(traducao(40331), categorias)
      if index > -1:
            ano=['2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2000-2005','1990-1999','1980-1989','1970-1979','1960-1969','1950-1959','1900-1949']
            anonumb=['2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2000','1990','1980','1970','1960','1950','1900']
            index2 = xbmcgui.Dialog().select(traducao(40331), ano)
            if index2 > -1:
                  urlfinal=MainURL + 'pagination.ajax.php?p=1&order=date&years=%s&genres=%s' % (anonumb[index2],catnumb[index])
                  print urlfinal
                  print url
                  if re.search('animes',url): series_request(urlfinal + '&mediaType=animes',False)
                  elif re.search('series',url): series_request(urlfinal + '&mediaType=series',False)
                  elif re.search('movies',url): filmes_request(urlfinal + '&mediaType=movies',False)
                  

def listas(url):
      if url=='filmes':baselist='http://fightnight-xbmc.googlecode.com/svn/addons/wareztuga/listas.txt'
      elif url=='series':pass
      elif url=='animes':pass
      addLista("[B][COLOR red]O que são as listas? Como ajudar?[/COLOR][/B]",'lol',31,wtpath + art + 'agendados.png',1,False,'Breve explicação do que são as listas e como funcionam.[CR][CR]Todos podem participar!')
      listas=abrir_url(baselist)
      conteudos=re.compile('"titulo":"(.+?)","author":"(.+?)","descricao":"(.+?)","url":"(.+?)"').findall(listas)
      for titulo,author,descricao,listurl in conteudos: addLista('[B]%s[/B] (%s)' % (titulo,author),listurl,29,wtpath + art + 'agendados.png',len(conteudos),True,descricao)
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')
      xbmc.executebuiltin("Container.SetViewMode(560)")
            
def conteudolistas(url):
      lista=abrir_url(url)
      conteudos=re.compile('{"titulopt":"(.+?)","wtid":"(.+?)","opiniao":"(.+?)","url":"(.+?)"}').findall(lista)
      for titulo,wtid,opiniao,wturl in conteudos:
            #wturl=wturl.replace('wareztuga.tv','wareztuga.me')
            addLista('[B]%s[/B]' % (titulo),wturl,5,MainURL + 'images/movies_thumbs/thumb' + wtid + '.png',len(conteudos),False,opiniao)
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')
      xbmc.executebuiltin("Container.SetViewMode(560)")

## thx silen

def unrestrict_login():
        mensagemprogresso.create('wareztuga.tv', traducao(40054),traducao(40055))       
        mensagemprogresso.update(0)
        from t0mm0.common.net import Net
        net=Net()
        if selfAddon.getSetting('unrestrict-enable') == 'true':
                urlsignin='https://unrestrict.li/sign_in'
                data = net.http_POST(urlsignin,{'return':'registered','username':usernameunli,'password':passwordunli,'signin':'Sign+in'}).content
                success=re.compile('href=".+?unrestrict.li/profile">(.+?)</a>.+?href=".+?unrestrict.li/sign_out">(.+?)</a>',re.DOTALL).findall(data)
                if success:
                        net.save_cookies(cookie_un)
                        print 'Unrestrict Registered Account: login efectuado'
                if not success:
                        if re.search('adcopy_challenge',data): unrestrict_captcha(urlsignin,'login')
                        else:
                              print 'Unrestrict Registered Account: login failed'
                              xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40224)+",'500000',"+iconpequeno.encode('utf-8')+")")
                              xbmc.sleep(2)
                              sys.exit(0)

def unrestrict_link(linkescolha,thumbnail,name,fic,simounao,wturl):
        from t0mm0.common.net import Net
        net=Net()
        net.set_cookies(cookie_un)
        link = net.http_POST('https://unrestrict.li/unrestrict.php',{'link':linkescolha,'domain':'long'}).content
        import json
        download_link = json.loads(link).items()[0][0] # The response is JSON list, therfore need to iterate the list and select item[0] - item[0]
        if re.search('"invalid":"File offline."',link):
              xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40164)+",'500000',"+iconpequeno.encode('utf-8')+")")
              mensagemprogresso.close()
        elif download_link=='error':
              xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,Erro no serviço,'500000',"+iconpequeno.encode('utf-8')+")")
              return      
        else:
                if 'https://unrestrict.li' in download_link:
                    print 'UN.li Registado nao VIP'
                    try: download_link=unrestrict_captcha(download_link,'download')
                    except: raise
                mensagemprogresso.update(66)
                req = urllib2.Request(download_link)
                req.add_header('User-Agent', user_agent)
                streamlink = urllib2.urlopen(req).url
                mensagemprogresso.update(100)
                if simounao=='download':
                      mensagemprogresso.close()
                      if downloadPath=='':
                            ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
                            selfAddon.openSettings()
                            return          
                      else:
                            fezdown=fazerdownload(name,streamlink,subtitles=fic)
                            encerrarsistema()
                if simounao=='agora':
                      comecarvideo(fic,streamlink + '|User-Agent=' + urllib.quote(user_agent),name,thumbnail,wturl,True)

def unrestrict_captcha(url,referido):
        mensagemprogresso.update(33)
        from t0mm0.common.net import Net
        net=Net()
        import json
        urlsignin='https://unrestrict.li/sign_in'
        from random import randint
        captcha_img = os.path.join(pastacaptcha,str(randint(0, 9999999))+ ".png")
        try:
            response = net.http_GET(url)
            html =  response.content                    
            try:media_id=re.compile('id="link" type="hidden" value="(.+?)" />').findall(html)[0]
            except: pass
            noscript=re.compile('<iframe src=".+?solvemedia.com([^"]+?)"').findall(link)[0]
            check = net.http_GET("http://api.solvemedia.com"+ noscript).content
            hugekey=re.compile('id="adcopy_challenge" value="(.+?)">').findall(check)[0]
            captcha_headers= {'User-Agent':'Mozilla/6.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4','Host':'api.solvemedia.com','Referer':response.get_url(),'Accept':'image/png,image/*;q=0.8,*/*;q=0.5'}
            open(captcha_img, 'wb').write( net.http_GET("http://api.solvemedia.com%s"%re.compile('<img src="(.+?)"').findall(check)[0] ).content)
            try: solved,id = solvevia9kw(captcha_img)
            except:
                  solved = ''
                  id = ''
            if solved != '':
                  puzzle = solved
            else:
                  solver = InputWindow(captcha=captcha_img)
                  puzzle = solver.get()
            try:os.remove(captcha_img)
            except: pass
            if puzzle and referido=='download':
                  data={'response':urllib.quote_plus(puzzle),'challenge':hugekey,'link':media_id}
                  html = net.http_POST('https://unrestrict.li/download.php',data).content
                  download_link = json.loads(html).items()[0][1]
                  if re.search('Incorrect captcha entered',download_link):
                        if id != '':
                              try: Ninekwusercaptchacorrectback(id,"2")
                              except:pass
                        xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40227)+",'500000',"+iconpequeno.encode('utf-8')+")")
                        sys.exit(0)
                        raise
                  else:
                        if id != '':
                              try: Ninekwusercaptchacorrectback(id,"1")
                              except: pass
                        return download_link
            if puzzle and referido=='login':
                        data = net.http_POST(urlsignin,{'return':'registered','username':usernameunli,'password':passwordunli,'adcopy_response':urllib.quote_plus(puzzle),'adcopy_challenge':hugekey,'signin':'Sign+in'}).content
                        success=re.compile('href=".+?unrestrict.li/profile">(.+?)</a>.+?href=".+?unrestrict.li/sign_out">(.+?)</a>',re.DOTALL).findall(data)
                        if success:
                              net.save_cookies(cookie_un)
                              print 'Unrestrict Registered Account: login efectuado'
                        else:
                              print 'Unrestrict Registered Account: login failed'
                              xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40224)+",'500000',"+iconpequeno.encode('utf-8')+")")
                              xbmc.sleep(2)
                              sys.exit(0)
            #return puzzle,hugekey
        except: raise

class InputWindow(xbmcgui.WindowDialog):# Cheers to Bastardsmkr code already done in Putlocker PRO resolver.
    
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        xposition = 425
        yposition = 5
        hposition = 135
        wposition = 405
        self.img = xbmcgui.ControlImage(xposition,yposition,wposition,hposition,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard('','Captcha:')

    def get(self):
        self.show()
        #xbmc.sleep(150)#3000
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        else:
            self.close()
            sys.exit(0)
        self.close()
        return False

#################################################### REAL DEBRID #################################################

def realdebrid(urlvideo,thumbnail,moviename,fic,simounao,wturl):
      print "Modo RealDebrid"
      if cookie_rd is not None and os.path.exists(cookie_rd):
            if selfAddon.getSetting('realdebrid-username2') != selfAddon.getSetting('realdebrid-usernamecheck2') or selfAddon.getSetting('realdebrid-password2') != selfAddon.getSetting('realdebrid-passwordcheck2'): realdebrid_login(urlvideo,thumbnail,moviename,fic,simounao,wturl)
            else:
                  cj = cookielib.LWPCookieJar()
                  cj.load(cookie_rd)
                  verificarconta = 'https://real-debrid.com/api/account.php'
                  req = urllib2.Request(verificarconta)
                  req.add_header('User-Agent', user_agent)
                  openerdeb = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                  try:
                        response = openerdeb.open(req)
                        source = response.read()
                        response.close()
                  except:
                        response = openerdeb.open(req)
                        source = response.read()
                        response.close()
                  mensagemprogresso.update(50)
                  if source is not None and re.search('expiration', source):
                        tempomili=str(millis())
                        rdeb='https://real-debrid.com/ajax/unrestrict.php?link='+urlvideo+'&password=&remote=0&time='+ tempomili
                        conteudolink = openerdeb.open(rdeb).read()
                        if re.search('"error":4', conteudolink):
                              mensagemok(traducao(40162), traducao(40350), '', '')
                              mensagemprogresso.close()
                              return
                        if re.search('"error":5', conteudolink):
                              mensagemok(traducao(40162), traducao(40163), '', '')
                              mensagemprogresso.close()
                              return
                        if re.search('"error":10',conteudolink):
                              mensagemok(traducao(40162), traducao(40166), '', '')
                              mensagemprogresso.close()
                              return
                        if re.search('"error":11',conteudolink):
                              mensagemok(traducao(40162), traducao(40164), '', '')
                              mensagemprogresso.close()
                              return
                        if re.search('"error":0',conteudolink):
                              linkfinal =re.compile('generated_links":.+?,.+?,"(.+?)".+?"main_link"').findall(conteudolink)[0]
                              linkfinal=linkfinal.replace("\\",'')
                              if len(linkfinal) == 0: return False
                              print 'O link gerado e: ' + linkfinal
                              mensagemprogresso.update(100)
                              if simounao=='download':
                                    mensagemprogresso.close()
                                    if downloadPath=='':
                                          ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
                                          selfAddon.openSettings()
                                          return          
                                    else:
                                          fezdown=fazerdownload(moviename,linkfinal,subtitles=fic)
                                          encerrarsistema()                              
                              if simounao=='agora':
                                    comecarvideo(fic,linkfinal,moviename,thumbnail,wturl,False)
                  else:
                        realdebrid_login(urlvideo,thumbnail,moviename,fic,simounao,wturl)
                        mensagemprogresso.close()
      else: realdebrid_login(urlvideo,thumbnail,moviename,fic,simounao,wturl)
            
def realdebrid_login(urlvideo,thumbnail,moviename,fic,simounao,wturl):
      cj = cookielib.LWPCookieJar()
      verificarconta = 'https://real-debrid.com/api/account.php'
      import hashlib
      tempomili=str(millis())
      login_data = urllib.urlencode({'user' : selfAddon.getSetting('realdebrid-username2'), 'pass' : hashlib.md5(selfAddon.getSetting('realdebrid-password2')).hexdigest()})
      urlconta = 'https://real-debrid.com/ajax/login.php?' + login_data + '&captcha_challenge=&captcha_answer=&time=' + tempomili
      req = urllib2.Request(urlconta)
      req.add_header('User-Agent', user_agent)
      cj = cookielib.LWPCookieJar()
      openerdeb = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      response = openerdeb.open(req)
      source = response.read()
      response.close()
      cj.save(cookie_rd)
      print "Gravou cookie"
      if re.search('OK',source):
            rdusername=selfAddon.getSetting('realdebrid-username2')
            rdpassword=selfAddon.getSetting('realdebrid-password2')
            selfAddon.setSetting('realdebrid-usernamecheck2',value=rdusername)
            selfAddon.setSetting('realdebrid-passwordcheck2',value=rdpassword)
            xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40223)+",'500000',"+iconpequeno.encode('utf-8')+")")
            realdebrid(urlvideo,thumbnail,moviename,fic,simounao,wturl)
      else:
            mensagemok(traducao(40162), traducao(40167))
            selfAddon.setSetting(id='realdebrid-enable2', value='false')
            selfAddon.openSettings()
            
####################################### FILMES / SERIES RELACIONADO COM A CONTA #################################

def itens_conta(url):
      link=abrir_url_cookie(url)
      link2=clean(link)
      tipo=re.compile('&action=(.+?)&').findall(url)[0]
      if re.search('cat=movies',url):
            conteudo=re.compile("""<div id=".+?" class=".+?"><a href="movie.php(.+?)" title="(.+?)"><img src="(.+?)" alt=".+?" /><div class="thumb-effect"></div></a><a href=".+?" class=".+?" onclick="removeMediaContent.+?'(.+?)', (.+?), .+?"></a></div>""").findall(link2)
            for url,name,thumbnail,categoria,warezid in conteudo: addPessoal('[B]' + name + '[/B]',MainURL + SingleMovieURL + url,5,MainURL + thumbnail,warezid,tipo,categoria,True)
      elif re.search('cat=series',url):
            conteudo=re.compile("""<div id=".+?" class=".+?"><a href="serie.php(.+?)" title="(.+?)"><img src="(.+?)" alt=".+?" /><div class="thumb-effect"></div></a><a href=".+?" class=".+?" onclick="removeMediaContent.+?'(.+?)', (.+?), .+?"></a></div>""").findall(link2)
            for url,name,thumbnail,categoria,warezid in conteudo: addPessoal('[B]' + name + '[/B]',MainURL + SingleSerieURL + url,6,MainURL + thumbnail,warezid,tipo,categoria,True)
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            vista_series()
      else:
            episodios=re.compile("""<div id=".+?" class=".+?"><a href="serie.php(.+?)" title="(.+?) - (.+?)"><img src="(.+?)" alt=".+?" /><div class="thumb-effect"></div></a><a href=".+?" class=".+?" onclick="removeMediaContent.+?'(.+?)', (.+?), .+?"></a>""").findall(link2)
            for url,nomeserie,nomeepisodio,thumbnail,categoria,warezid in episodios: addPessoal('[B]' + nomeserie + '[/B] (' + nomeepisodio + ')',MainURL + SingleSerieURL + url,5,MainURL + thumbnail,warezid,tipo,categoria,True)
      try:
            pagina=re.compile("""<a .+?actual.+?>.+?<a href="javascript: myAccount.+?\'accountMedia.ajax.php.+?=(.+?)&(.+?)'""").findall(link)
            addDir('[COLOR blue]' + traducao(40042) + pagina[0][0] + ' >>>[/COLOR]',MainURL + "accountMedia.ajax.php?p=" + pagina[0][0] + '&' + pagina[0][1],30,wtpath + art + 'seta.png',1,True)
      except: pass

def notificacoes_request(url):
      link=abrir_url_cookie(url)
      link2=clean(link)
      request=re.compile('<div class="notification-label(.+?)" onclick=".+?"><span class="green-bold">(.+?)</span><span class=".+?"></span>(.+?)</div><div id="notifPrev(.+?)"').findall(link2)
      for lido,data,texto,notid in request:
            try:
                  urlnotific='faq.php'
                  texto = texto.replace('&nbsp;</span><span class="bold">',' ').replace('</span><span>&nbsp;',' ').replace('</span><span class="green-bold">&nbsp;',' ').replace('&nbsp;',' ').replace('</span>',' ').replace('<span class="green-bold">','')
                  try:
                        videoname=re.compile('<span>(.+?)<a href="(.+?)".+?>(.+?)</a><span>').findall(texto)
                        for parte1,urlnotific,parte2 in videoname: texadd= '[B]' + data + '[/B] - ' + parte1 + parte2
                  except: texadd=texto.replace('<span>','')
                  if lido == ' unchecked': texadd='[COLOR yellow]' + texadd + '[/COLOR]'
                  addDir(texadd,MainURL + urlnotific + '/////' + MainURL + 'checkNotification.ajax.php?notificationID=' + notid + '/////',8,MainURL,1,False)
            except: pass
      xbmc.executebuiltin("Container.SetViewMode(51)")

def conteudonotificacao(url,name):
      links=re.compile('(.+?)/////(.+?)/////').findall(url)[0]
      abrir_url_cookie(links[1])
      if re.search('COLOR yellow',name):
            xbmc.executebuiltin("Container.Refresh")
            xbmc.sleep(2)
      if re.search('adicionou um',name) or ('pedido relacionado com o filme',name):
            try:
                  opcao= xbmcgui.Dialog().yesno("wareztuga.tv", "Deseja abrir o conteúdo da notificação?")
                  if opcao: resolver_servidores(links[0],name)
            except: pass
      #elif re.search('pedido relacionado com a s\xc3\xa9rie',name): seriestemp_request(name,links[0])      
      #elif re.search('gostaram do',name) or re.search('gostou do',name):             
            #elif re.search('comentou no',parte1) or re.search('comentaram no',parte1): ## mostrar comentario
            ##mostrar comentario == comentario gostado??

################################################# PEDIDOS #########################################################

def pedidos_request(url):
      link=abrir_url_cookie(url)
      link2=clean(link)
      request=re.compile('<div id="req(.+?)" class="request.+?"><div class="thumb" title="(.+?)"><a href=".+?" target="_blank"><img src="(.+?)" alt=".+?"><div class="thumb-effect" title=".+?"></div></a></div><div class="reqInfo"><span class="hmReqs"><span>(.+?)</span> .+?</span><a href=".+?">(.+?)</a>').findall(link2)
      for warezid,name,thumbnail, numpedidos,meupedido in request:
            #1 elemento nao faz o grab correcto do id
            if meupedido=="Desejado":
                  name= '[COLOR yellow][B]' + name + '[/B] (' + numpedidos + traducao(40079) + ')[/COLOR]'
                  addDir(name,MainURL + 'requestsIncrement.ajax.php?reqID=' + warezid + '&action=0',8,MainURL + thumbnail,1,False)
            else: addDir('[B]' + name + '[/B] (' + numpedidos + traducao(40079) + ')',MainURL + 'requestsIncrement.ajax.php?reqID=' + warezid + '&action=1',8,MainURL + thumbnail,1,False)


######################################################## REQUEST DE FILMES #################################################
                          
def filmes_request(url,pesquisa):
      cert=''
      imdbid=''
      link=abrir_url_cookie(url)
      link2=clean(link)
      info=re.compile("""<a href="movie.php(.+?)"><img src="(.+?)" alt="(.+?)" /><div class="thumb-effect" title=".+?"></div></a></div></div><div class="movie-info"><a href=".+?" class="movie-name">.+?</a><div class="clear"></div><div class="movie-detailed-info"><div class="detailed-aux" style=".+?"><span class="genre">(.+?)</span>.+?year.+?</span>(.+?)<span>.+?</span></span><span class="original-name"> - "(.+?)"</span></div><div class="detailed-aux"><span class="director-caption">Realizador: </span><span class="director"(.+?)</span></div><div class="detailed-aux"><span class="director-caption">Elenco:</span><span class="director"(.+?)</span></div></div><div class="movie-actions.+?><a id="watched" href="javascript: movieUserAction.+?'movies.+?watched.+?;.+?>(.+?)<span class=".+?"></span></a><br /><a id="cliped" href="javascript: movieUserAction.+?'movies.+?cliped.+?;".+?>(.+?)<span class=".+?"></span></a><br /><a id="faved" href="javascript: movieUserAction.+?'movies.+?faved.+?;".+?>(.+?)<span class=".+?"></span></a></div><div class="clear"></div><div class="wtv-rating"><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span></div><div class="clear"></div><span id="movie-synopsis" class="movie-synopsis">.+?</span><span id="movie-synopsis-aux" class="movie-synopsis-aux">(.+?)</span>""").findall(link2)
      if len(info)>0 and pesquisa==True: addLink("[B][COLOR blue]" + traducao(40012) + ":[/COLOR][/B]",'',wtpath + art + 'nothingx.png')
      for url,thumbnail,name,genre,year,originalname,director,cast,visto,agendar,faved,synowt in info:                      
            if faved=='Favorito': faved=1
            else: faved=0
            if agendar=='Agendado': agendar=1
            else: agendar=0
            try:
                  cast=cast.replace('>',' ')
                  cast=cast.split(',')
            except: cast=[]
            overlay=6; nothing = '<?xml version="1.0" encoding="UTF-8"?>\n<OpenSearchDescription xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">\n  <opensearch:Query searchTerms=""/>\n  <opensearch:totalResults>0</opensearch:totalResults>\n  <movies>Nothing found.</movies>\n</OpenSearchDescription>\n'
            director=director.replace('>','')
            warezid=str(re.compile('images/movies_thumbs/thumb(.+?).png').findall(thumbnail)[0])
            if visto=="Filme visto": overlay=7
            if selfAddon.getSetting("metadata-movies10") == "true":
                  #variaveis=["rating","fanart","votes","moviedb"]
                  #emcache=cache.get('m'+warezid)
                  #print emcache
                  emcache=False
                  if not emcache:
                        try:
                              txheaders= {'User-Agent':user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
                              request='http://api.themoviedb.org/3/search/movie?api_key=6ee3768ba155b41252384a1148398b34&order=asc&year=%s&query=%s&per_page=1'%(year,urllib.quote_plus(originalname))
                              req = urllib2.Request(request,None,txheaders)
                              response=load_json(urllib2.urlopen(req).read())
                        except: pass
                        tmdbim='http://d3gtl9l2a4fn1j.cloudfront.net/t/p/'
                        try: rating=float(response['results'][0]['vote_average'])
                        except: rating=float(0.0)
                        try:fanart= tmdbim + 'w780' + response['results'][0]['backdrop_path']
                        except: fanart=''
                        try:votes=response['results'][0]['vote_count']
                        except: votes=''
                        try:moviedbid=str(response['results'][0]['id'])
                        except: moviedbid=0
                        #conteudo={"rating":rating,"fanart":fanart,"votes":votes,"moviedb":moviedbid}
                        #cache.set("m"+warezid, 'yoyo')
                  else:
                        #print emcache
                        pass
                        #print cache.get('m'+warezid)
                  if selfAddon.getSetting("englishmetadata10") == "false": addFilme('[B]' + name + '[/B] (' + year + ')',MainURL + SingleMovieURL + url,5,MainURL + thumbnail,originalname,genre,int(year),cast,director,synowt,fanart,rating,cert,cast,votes,moviedbid,imdbid,overlay,warezid,faved,agendar,len(info))
                  else:
                        genre=genre.replace('Acção','Action').replace('Animação','Animation').replace('Aventura','Adventure').replace('Biografia','Biography').replace('Comédia','Comedy').replace('Desporto','Sports').replace('Documentário','Documentary').replace('Familiar','Family').replace('Fantasia','Fantasy').replace('Ficção Científica','Science Fiction').replace('Guerra','War').replace('História','History').replace('Mistério','Mistery').replace('Romance','Novel').replace('Terror','Horror')
                        try: desc=re.compile('<overview>(.+?)</overview>').findall(response)[0]
                        except: desc='English plot not found. Portuguese: ' + synowt
                        try: englishposter=tmdbim + 'w185' + response['results'][0]['poster_path']
                        except: englishposter=MainURL + thumbnail
                        addFilme('[B]' + originalname + '[/B] (' + year + ')',MainURL + SingleMovieURL + url,5,englishposter,originalname,genre,int(year),cast,director,desc,fanart,rating,cert,cast,votes,moviedbid,imdbid,overlay,warezid,faved,agendar,len(info))
            else:
                  if selfAddon.getSetting("englishmetadata10") == "false": addFilme('[B]' + name + '[/B] (' + year + ')',MainURL + SingleMovieURL + url,5,MainURL + thumbnail,originalname,genre,int(year),cast,director,synowt,'','','','','',0,'',overlay,warezid,faved,agendar,len(info))
                  else:
                        genre=genre.replace('Acção','Action').replace('Animação','Animation').replace('Aventura','Adventure').replace('Biografia','Biography').replace('Comédia','Comedy').replace('Desporto','Sports').replace('Documentário','Documentary').replace('Familiar','Family').replace('Fantasia','Fantasy').replace('Ficção Científica','Science Fiction').replace('Guerra','War').replace('História','History').replace('Mistério','Mistery').replace('Romance','Novel').replace('Terror','Horror')
                        desc='Metadata search disabled. Portuguese: ' + synowt
                        addFilme('[B]' + originalname + '[/B] (' + year + ')',MainURL + SingleMovieURL + url,5,MainURL + thumbnail,originalname,genre,int(year),cast,director,desc,'','','','','',0,'',overlay,warezid,faved,agendar,len(info))
      paginas(MainURL + SingleMovieURL + url,link,'movies')
      xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
      vista_filmes()
      return len(info)

######################################################## REQUEST DE SERIES #################################################

def series_request(url,pesquisa):
      if re.search('&mediaType=animes',url):
            tipo='animes'
            titulo=traducao(40215)
      else:
            tipo='series'
            titulo=traducao(40013)
      link=abrir_url_cookie(url)
      link2=clean(link)
      match=re.compile("""<a href="serie.php(.+?)"><img src="(.+?)" alt="(.+?)" /><div class="thumb-effect2" title=".+?"></div></a></div><div class="episodes-number"><span>(.+?)</span> .+?</div></div><div class="movie-info"><a href=".+?" class="movie-name">.+?</a><div class="clear"></div><div class="movie-detailed-info"><span class="genre">(.+?)</span>.+?year.+?</span>(.+?)<span>.+?</span></span><span class="original-name">- (.+?)</span><br /><span class="director">(.+?)</span><span class="director-caption">.+?</span></div><div class="movie-actions.+?><a id="subscribed" href="javascript: movieUserAction.+?series.+?,.+?,.+?subscribed.+?>(.+?)<span class=".+?"></span>.+?<a id="watched" href="javascript: movieUserAction.+?series.+?, .+?, .+?watched.+?".+?>(.+?)<span class=".+?"></span>.+?<a id="faved" href="javascript: movieUserAction.+?series.+?, (.+?), .+?faved.+?".+?>(.+?)<span class=".+?"></span>.+?<div class="wtv-rating"><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span>.+?<span id="movie-synopsis" class="movie-synopsis">.+?<span id="movie-synopsis-aux" class="movie-synopsis-aux">(.+?)</span></div>""").findall(link2)
      if len(match)>0 and pesquisa==True: addLink("[B][COLOR blue]" + titulo + ":[/COLOR][/B]",'',wtpath + art + 'nothingx.png')
      for url,thumbnail,name,nrepisodios,genre,year,estado,temporadas,subsc,visto,warezid,faved,sinopse in match:
            if faved=='Favorita': faved=1
            else: faved=0
            if visto=='Série vista': overlay=7
            else: overlay=6
            if subsc=='A seguir': subsc=1
            else: subsc=0
            if selfAddon.getSetting("metadata-tvshows10") == "true":
                  try:
                        cert=''
                        rating=''
                        votes=''
                        duration=0
                        estreia=''
                        try:
                              txheaders= {'Accept': 'application/json','User-Agent':user_agent}
                              req2 = urllib2.Request('http://www.thetvdb.com/api/GetSeries.php?seriesname=%s'%(urllib.quote_plus(name)),None,txheaders)
                              response2=urllib2.urlopen(req2).read()
                        except: pass
                        try: serieid=re.compile('<seriesid>(.+?)</seriesid>').findall(response2)[0]
                        except: serieid=''
                        #req3 = urllib2.Request('http://thetvdb.com/api/97FFDC4BB0536270/series/%s/pt.xml'%(urllib.quote_plus(serieid)),None,txheaders)
                        #response3=urllib2.urlopen(req3).read()
                        #try: cert=re.compile('<ContentRating>(.+?)</ContentRating>').findall(response3)[0]
                        #except: cert=''
                        try: cadeia=re.compile('<Network>(.+?)</Network>').findall(response2)[0]
                        except: cadeia=''
                        #try: rating=float(re.compile('<Rating>(.+?)</Rating>').findall(response3)[0])
                        #except: rating=float(0.0)
                        #try: votes=re.compile('<RatingCount>(.+?)</RatingCount>').findall(response3)[0]
                        #except: votes=''
                        #try: duration=re.compile('<Runtime>(.+?)</Runtime>').findall(response3)[0]
                        #except: duration=''
                        #try: estreia=re.compile('<FirstAired>(.+?)</FirstAired>').findall(response3)[0]
                        #except: estreia=''
                        #try: fanart="http://thetvdb.com/banners/" + re.compile('<fanart>(.+?)</fanart>').findall(response3)[0]
                        try: fanart="http://thetvdb.com/banners/fanart/original/" + serieid + "-1.jpg"
                        except: fanart=''
                  except: serieid=cert=cadeia=rating=votes=duration=estreia=fanart=''
                  addSerie('[B]' + name + '[/B] (' + year + ')',MainURL + SingleSerieURL + url,6,MainURL + thumbnail,genre,int(year),[],cadeia,sinopse,fanart,rating,cert,int(nrepisodios),estreia,votes,estado,serieid,duration,subsc,overlay,faved,warezid,len(match))
            else: addSerie('[B]' + name + '[/B] (' + year + ')',MainURL + SingleSerieURL + url,6,MainURL + thumbnail,genre,int(year),[],'',sinopse,'',0,'',int(nrepisodios),'','',estado,'','',subsc,overlay,faved,warezid,len(match))
      paginas(MainURL + SingleSerieURL + url,link,tipo)
      xbmcplugin.setContent(int(sys.argv[1]), 'movies')
      if pesquisa==True: vista_filmes()
      else: vista_series()

def seriestemp_request(name,url):
      link=abrir_url_cookie(url)
      nomeserie=re.compile('<div class="thumb serie" title="(.+?)">').findall(link)[0]
      match=re.compile('<div id="season.+?" class="season"><a href=".+?">(.+?)</a></div>').findall(link)
      for numero in match:
            if len(match)==1: seriesepis_request(url + "&season=" + numero,traducao(40045) + numero)            
            else: addTemp(traducao(40045) + numero,url + "&season=" + numero,7,wtpath + art + numero + '.png',len(match),True)
      xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
      vista_temporadas()
              
def seriesepis_request(url,name):
      link=clean(abrir_url_cookie(url))
      textosubs='</div><div class="officialSubs">'
      episodelist=re.compile('<div class="slide-content-bg">(.+?)<input type="hidden" id="raterDefault"').findall(link)[0]
      match=re.compile('<a href="serie.php(.+?)"><img src="(.+?)" alt="(.+?)" /><div class="thumb-shadow"></div><div class="thumb-effect"></div><div class="episode-number">(.+?)</div></a>').findall(episodelist)
      for url,thumbnail,name,num in match:
            overlay=6
            agendar=0
            warezid=str(re.compile('images/thumbs/thumb(.+?).png').findall(thumbnail)[0])
            if re.search("""('episodes', """ + warezid + """, 'watched').+?" class="watched watchedslctd""", link): overlay=7
            if re.search("""('episodes', """ + warezid + """, 'cliped').+?" class="cliped clipedslctd""", link): agendar=1
            if re.search(textosubs,num):
                  num=num.replace(textosubs,'')
                  infonumero="[B][COLOR orange]" + str(traducao(40047)) + num + ":[/COLOR][/B] "
            else: infonumero="[B]" + str(traducao(40047)) + num + ":[/B] "
            addEpisodio( infonumero+ name,MainURL + SingleSerieURL + url,5,MainURL + thumbnail,overlay,warezid,agendar,len(match))
      proximos=re.compile('<div id="episode_nextEp(.+?)" class="item nextepisodes".+?><input type="hidden" id="date_nextEp.+?" value="(.+?)" /><div class="thumb">.+?<img src="(.+?)" alt="_nextEp.+?" />.+?<div class="episode-number">(.+?)</div>').findall(link)
      for epid,epdate,epimg,epnum in proximos:
            epname=re.compile('<div id="episodeInfo_nextEp'+epid+'" class="episode-info".+?>.+?<span class="sep"> - </span>(.+?)</div>').findall(link)[0]
            addDir("[B]" + str(traducao(40047)) + epnum + "[/B]: " + epname +' ('+epdate+')',MainURL + 'getNextEpisodesInfo.ajax.php?id=' + epid,25,MainURL + epimg,0,False)
      xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
      vista_episodios()

def infoproximoepisodio(name,url):
      conteudo=clean(abrir_url_cookie(url))
      header=re.compile('<div class="episodeInfo">(.+?)</div>').findall(conteudo)[0]
      header=header.replace('<span>','[COLOR blue][B]').replace('</span>','[/B][/COLOR]').replace('<br />','\n').replace('<b>','[COLOR blue][B]').replace('</b>','[/B][/COLOR]')
      infoextra=re.compile('<div class="generalInfo">(.+?)</div>').findall(conteudo)[0]
      infoextra=infoextra.replace('<span>','[COLOR blue][B]').replace('</span>','[/B][/COLOR]').replace('<br />','\n').replace('<b>','[COLOR blue][B]').replace('</b>','[/B][/COLOR]')
      mensagemaviso(header + '\n\n' + infoextra)

def mensagemaviso(conteudo):
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % ('INFO','wareztuga.tv',))
        window.getControl(5).setText(conteudo)
    except: pass

#################################################SERIES EM EXIBICAO ##################################################

def series_exib(url):
      link=abrir_url_cookie(url)
      match=re.compile('<a href="serie.php(.+?)>\r\n\t\t\t\t<img src="(.+?)" alt="(.+?)" />').findall(link)
      for url,thumbnail,name in match:
            episodename=url.replace('_',' ')
            try:
                  episodename=re.compile('&ep=(.+?)"').findall(episodename)[0]
                  episodename=" (" + episodename + ")"
            except:episodename=''
            url=url.replace('"','')
            addDir('[B]' + name + '[/B]' + episodename,MainURL + SingleSerieURL + url,18,MainURL + thumbnail,len(match),True)
      xbmcplugin.setContent(int(sys.argv[1]), 'movies')
      vista_series()

def series_exib_escolha(url,name):
      link=abrir_url_cookie(url)
      ano=re.compile('<span class="year"><span>.+?</span>(.+?)<span>.+?</span></span>').findall(link)[0]
      opcao= xbmcgui.Dialog().yesno("wareztuga.tv", traducao(40130), traducao(40131), traducao(40143) + ': ' + name, traducao(40144), traducao(40145))
      if opcao == 1: seriestemp_request(name,url)
      else: resolver_servidores(url,name)

################################################### SERVIDORES ######################################################
                      
def resolver_servidores(url,name,download=False,dialogselect=True):
      if selfAddon.getSetting('realdebrid-enable2') == 'true': rdaccount=True
      else: rdaccount=False
      wturl=url
      link=abrir_url_cookie(url)
      if re.search('movie.php',url):
            thumbnail=re.compile('<meta property="og:image" content="(.+?)" />').findall(link)[0]
            warezid=re.compile('<div id="movie(.+?)" class="player-aux"').findall(link)[0]
            tipo='movies'
      else:
            serie=re.compile('<title>wareztuga.tv - .+? - (.+?): Temporada (.+?), Epis.+?io (.+?)</title>').findall(link)
            for epname, temporada,episodio in serie:
                  seriename=re.compile('<div class="thumb serie" title="(.+?)">').findall(link)[0]
                  name= '[B]' + seriename + '[/B] | Temp. ' + temporada + ': Ep. '+ episodio +' - ' + epname + '-'
            thumbnail=re.compile('<input type="hidden" id="episode-selected" value="(.+?)">').findall(link)[0]
            warezid=thumbnail
            thumbnail=MainURL + 'images/thumbs/thumb' + thumbnail + '.png'
            tipo='episodes'
      link2=clean(link)
      link2=link2.replace('?wareztuga=1','wareztuga=1')
      #listadecomentarios=listarcomentarios(link)
      listadecomentarios=''
      titles = []; ligacao = []
      infoservers=clean(abrir_url_cookie(MainURL + 'getFilehosts.ajax.php?mediaID=' + warezid + '&mediaType=' + tipo))
      tempobf=''
      '''
      socks=re.compile('http://www.sockshare.com/file/(.+?)" class="vidmega"').findall(infoservers)
      if socks:
            titles.append("[B][COLOR white]Sockshare[/COLOR][/B]")
            ligacao.append('http://www.sockshare.com/file/' + socks[0])
      bayf=re.compile('http://bayfiles.net/file/(.+?)" class="bayfiles"').findall(infoservers)
      if bayf:
            titles.append("[B][COLOR orange]Bay[/COLOR][COLOR white]Files[/COLOR][/B]" + tempobf)
            ligacao.append('http://bayfiles.net/file/' + bayf[0])
      putl=re.compile('http://www.putlocker.com/file/(.+?)" class="putlocker"').findall(infoservers)
      putl+=re.compile('http://www.firedrive.com/file/(.+?)" class="putlocker"').findall(infoservers)
      if putl:
            titles.append("[B][COLOR blue]Firedrive[/B]")
            ligacao.append('http://www.firedrive.com/file/' + putl[0])
      upz=re.compile('http://www.upzin.com/(.+?)" class="upzin"').findall(infoservers)
      if upz:
            titles.append("[B][COLOR white]Upzin[/COLOR][/B]")
            ligacao.append('http://www.upzin.com/' + upz[0])
            
      prof=re.compile('profity.org/(.+?)" class="profity"').findall(infoservers)
      if prof:
            titles.append("[B][COLOR white]Profity[/COLOR][/B]")
            ligacao.append('http://profity.org/' + prof[0])

      vshare=re.compile('vshare.eu/(.+?)" class="vshare"').findall(infoservers)
      if vshare:
            titles.append("[B][COLOR white]Video[/COLOR][COLOR blue]Share[/COLOR][/B]")
            ligacao.append('http://vshare.eu/' + vshare[0])
      '''
      
      huge=re.compile('http://hugefiles.net/(.+?)" class="hugefiles"').findall(infoservers)
      if huge:
            urlserver = 'http://hugefiles.net/' + huge[0]
            titles.append("HugeFiles")
            ligacao.append(urlserver)
            if rdaccount==True:
                  titles.append("HugeFiles - RealDebrid")
                  ligacao.append(urlserver)

      king=re.compile('kingfiles.net/(.+?)" class="kingfiles"').findall(infoservers)
      if king:
            urlserver = 'http://www.kingfiles.net/' + king[0]
            titles.append("KingFiles")
            ligacao.append(urlserver)
            if rdaccount==True:
                  titles.append("KingFiles - RealDebrid")
                  ligacao.append(urlserver)

      dvideo=re.compile('&fh=([^"]+?)" class="dropvideo"').findall(infoservers)
      if dvideo:
            titles.append("Dropvideo")
            ligacao.append('http://dropvideo.com/embed/' + dvideo[0])

      czilla=re.compile('&fh=([^"]+?)" class="cloudzilla"').findall(infoservers)
      if czilla:
            titles.append("Cloudzilla")
            ligacao.append('http://www.cloudzilla.to/embed/' + czilla[0])

      vidt=re.compile('&fh=([^"]+?)" class="vidto"').findall(infoservers)
      if vidt:
            titles.append("Vidto")
            ligacao.append('http://vidto.me/embed-' + vidt[0] + '-980x535.html')

      plyd=re.compile('&fh=([^"]+?)" class="played"').findall(infoservers)
      if plyd:
            titles.append("Played")
            ligacao.append('http://played.to/embed-' + plyd[0] + '-980x535.html')


      if download==False: simounao='agora'
      else:simounao='download'
      try:imdbrate='[COLOR orange][B]IMDb:[/B] ' + re.compile('<div class="imdb-rate"><span>(.+?)</span></div>').findall(link)[0] + '[/COLOR] '
      except:imdbrate=''
      try:wtrate='| [COLOR blue][B]Site:[/B] ' + re.compile('<span class="average">(.+?)</span>').findall(link)[0]+ '/10[/COLOR] ' 
      except:wtrate=''
      try:info='| ' + traducao(40142) + '[B][COLOR white] ' + re.compile('<span class="posted-by">inserido por <span>(.+?)</span></span>').findall(link)[0]+ '[/COLOR][/B]'
      except:info=''
      titles.append(imdbrate + wtrate + info)
      ligacao.append('informacaodovideo')
      print "Preferencial: desligado"
      menu_servidores(titles,ligacao,name,thumbnail,simounao,wturl,listadecomentarios,dialogselect)
      
def listarcomentarios(link):
    comentarios=re.compile('<div class="comment-user"><div class="username"><span>(.+?)</span>.+?<div class="comment-date"><span>(.+?)</span></div></div><div class="comment-number">.+?</div></div></div><div class="clear"></div><div class="comment-body">(.+?)<div class="comment-separator"></div>').findall(link)
    texto=[]
    if comentarios=='': texto.append('\n[B]' + str(traducao(40117)) + '[/B]')
    else: texto.append('\n[B]' + str(traducao(40118)) + ':[/B]')
    for nick,tempo,comment in comentarios:
        comment=comment.replace('<div class="quote">','[B]').replace('</div><br />','[/I] - ').replace('</span></div>','').replace('<span>[B]<span>','[I]').replace('</span>','').replace('<span>','').replace('<br />','')
        texto.append('[B][COLOR blue]' + nick + '[/COLOR][/B] (' + tempo + '): ' + comment)
    texto='\n\n'.join(texto)
    return texto

def menu_servidores(titles,ligacao,name,thumbnail,simounao,wturl,listadecomentarios,dialogselect):
      if len(ligacao)==2:
            index=0
            linkescolha=ligacao[index]
            vaiparaoserver(linkescolha,thumbnail,name,simounao,wturl,index,titles)
            return
      
      #if dialogselect==True:
      if len(ligacao)==1: ok=mensagemok('wareztuga.tv', 'Nenhum stream disponivel.')
      else:
            index = xbmcgui.Dialog().select('Escolha o servidor', titles)
            if index > -1:
                  linkescolha=ligacao[index]
                  vaiparaoserver(linkescolha,thumbnail,name,simounao,wturl,index,titles)
      #else:
      #      d = janelaservidores("serverswt.xml" , wtpath, "Default",titles=titles,ligacao=ligacao,name=name,thumbnail=thumbnail,simounao=simounao,wturl=wturl,listadecomentarios=listadecomentarios)
      #      d.doModal()
      #      del d

def entrarnoserver(linkescolha,name,thumbnail,simounao,wturl):
      index=0
      titulos=['Normal']
      vaiparaoserver(linkescolha,thumbnail,name,simounao,wturl,index,titulos)
      
def vaiparaoserver(linkescolha,thumbnail,name,simounao,wturl,index,titulos):
      if simounao=='download' and downloadPath=='':
            ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
            selfAddon.openSettings()
            return
      mensagemprogresso.create('wareztuga.tv', traducao(40054),traducao(40055))
      mensagemprogresso.update(0)
      fic=legendas(wturl)
      
      if re.search('RealDebrid',titulos[index]): realdebrid(linkescolha,thumbnail,name,fic,simounao,wturl)
      else:
            if re.search('bayfiles', linkescolha): bayfiles(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('upzin',linkescolha): upzin(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('firedrive',linkescolha): firedrive(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('sockshare',linkescolha): sockshare(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('hugefiles',linkescolha): hugefiles(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('profity',linkescolha): profity(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('kingfiles',linkescolha): kingfiles(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('vshare',linkescolha): videoshare(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('dropvideo',linkescolha): dropvideo(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('cloudzilla',linkescolha): dropvideo(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('vidto',linkescolha): vidto(linkescolha,fic,name,thumbnail,simounao,wturl)
            elif re.search('played',linkescolha): played(linkescolha,fic,name,thumbnail,simounao,wturl)
            else: mensagemprogresso.close()
      
def sintomecomsorte():
      categorias=[traducao(40330),traducao(40091),traducao(40092),traducao(40093),traducao(40094),traducao(40095),traducao(40096),traducao(40097),traducao(40098),traducao(40099),traducao(40100),traducao(40101),traducao(40102),traducao(40103),traducao(40104),traducao(40105),traducao(40106),traducao(40107),traducao(40108),traducao(40109),traducao(40110)]
      catnumb=['0','1','17','4','5','6','2','21','18','3','7','8','14','15','9','13','11','12','10','16','20']
      index = xbmcgui.Dialog().select(traducao(40331), categorias)
      if index > -1:
            d = sorte("aleatorio.xml" , wtpath, "Default",catnumb=catnumb[index])
            d.doModal()
            del d

class sorte(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
          xbmcgui.WindowXML.__init__(self)
          self.catnumb = kwargs[ "catnumb" ]

    def onInit(self):
          self.contaleatorio()
          
    def onClick(self,controlId):
        if controlId == 2000: self.close()
        elif controlId == 2001:
            self.close()
            resolver_servidores(MainURL + SingleMovieURL +self.urlcont,'nada')
        elif controlId == 2002: self.contaleatorio()

    def contaleatorio(self):
          frase=['A carregar o bixo!','Vamos lá ver o que sai daqui','És esquisito?','Deixa cá ver o que se arranja','Acho que este é perfeito para ti','Milhares de coisas e andas armado em esquisito','Agora é que vai ser!','Desafio-te a ver este :)','Já estou cansado de dar sugestões','Dizem que este é bom','Eu não confiava nos meus gostos','A minha inteligência para escolher é altamente','#YOLO','É AGORA!']
          from random import randint
          self.getControl(3000).setLabel('[B][COLOR yellow]%s[/COLOR][/B]' %(frase[randint(0,len(frase)-1)]))
          self.getControl(9999).setVisible(True)
          url=MainURL + 'pagination.ajax.php?p=1&genres=%s' % (self.catnumb)
          link=abrir_url_cookie(url)
          ultimapagina=re.compile('...</span><a href="javascript: moviesList.+?pagination.ajax.php.+?p=(.+?)&').findall(link)[0]
          urlpagina=MainURL + 'pagination.ajax.php?p=%s&genres=%s' % (randint(0,int(ultimapagina)),self.catnumb)
          link=clean(abrir_url_cookie(urlpagina))
          info=re.compile("""<a href="movie.php(.+?)"><img src="(.+?)" alt="(.+?)" /><div class="thumb-effect" title=".+?"></div></a></div></div><div class="movie-info"><a href=".+?" class="movie-name">.+?</a><div class="clear"></div><div class="movie-detailed-info"><div class="detailed-aux" style=".+?"><span class="genre">(.+?)</span>.+?year.+?</span>(.+?)<span>.+?</span></span><span class="original-name"> - "(.+?)"</span></div><div class="detailed-aux"><span class="director-caption">Realizador: </span><span class="director"(.+?)</span></div><div class="detailed-aux"><span class="director-caption">Elenco:</span><span class="director"(.+?)</span></div></div><div class="movie-actions.+?><a id="watched" href="javascript: movieUserAction.+?'movies.+?watched.+?;.+?>.+?<span class=".+?"></span></a><br /><a id="cliped" href="javascript: movieUserAction.+?'movies.+?cliped.+?;".+?>.+?<span class=".+?"></span></a><br /><a id="faved" href="javascript: movieUserAction.+?'movies.+?faved.+?;".+?>.+?<span class=".+?"></span></a></div><div class="clear"></div><div class="wtv-rating"><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span><s.+?></span></div><div class="clear"></div><span id="movie-synopsis" class="movie-synopsis">.+?</span><span id="movie-synopsis-aux" class="movie-synopsis-aux">(.+?)</span>""").findall(link)
          filmeqq=randint(0,len(info)-1)
          self.urlcont=info[filmeqq][0]
          cont_imagem=MainURL + info[filmeqq][1]
          cont_genero=info[filmeqq][3]
          if selfAddon.getSetting("englishmetadata10") == "false":cont_nome=info[filmeqq][2]#PT
          else:
                cont_nome=info[filmeqq][5]#PT
                cont_genero=cont_genero.replace('Acção','Action').replace('Animação','Animation').replace('Aventura','Adventure').replace('Biografia','Biography').replace('Comédia','Comedy').replace('Desporto','Sports').replace('Documentário','Documentary').replace('Familiar','Family').replace('Fantasia','Fantasy').replace('Ficção Científica','Science Fiction').replace('Guerra','War').replace('História','History').replace('Mistério','Mistery').replace('Romance','Novel').replace('Terror','Horror')
          cont_titulo='[B]%s[/B] (%s)' % (cont_nome,info[filmeqq][4])
          cont_director=info[filmeqq][6].replace('>','')
          cont_elenco=info[filmeqq][7].replace('>','')
          cont_sinopse=info[filmeqq][8]
          self.getControl(1002).setImage(cont_imagem)
          self.getControl(1001).setLabel(cont_titulo)
          self.getControl(1003).setLabel(cont_genero)
          self.getControl(1004).setLabel('[B]%s[/B]: %s' %(traducao(40332),cont_director))
          self.getControl(1005).setLabel('[B]%s[/B]: %s' %(traducao(40333),cont_elenco))
          self.getControl(1006).setText(cont_sinopse)
          self.getControl(9999).setVisible(False)
          
class janelaservidores(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
          xbmcgui.WindowXML.__init__(self)
          self.titles = kwargs[ "titles" ]
          self.ligacao = kwargs[ "ligacao" ]
          self.name = kwargs[ "name" ]
          self.thumbnail = kwargs[ "thumbnail" ]
          self.simounao = kwargs[ "simounao" ]
          self.wturl = kwargs[ "wturl" ]
          self.listadecomentarios= kwargs[ "listadecomentarios" ]

    def onInit(self):
          listControl = self.getControl(500)
          listControl.reset()
          i=0
          if len(self.ligacao)==1: self.getControl(802).setVisible(True)
          else: self.getControl(802).setVisible(False)
          for nomesservers in self.titles:
                if re.search('informacaodovideo',self.ligacao[i]): self.getControl(800).setLabel(nomesservers)
                else:self.addListagem(nomesservers,i)
                i=i+1
          #self.setFocus(500)
          #self.getControl(803).setText(self.listadecomentarios)

    def onClick(self,controlId):
        if controlId == 500:
            listControl = self.getControl(500)
            seleccionado=listControl.getSelectedItem()
            linkescolha=seleccionado.getProperty('ligacao')
            self.close()
            entrarnoserver(linkescolha,self.name,self.thumbnail,self.simounao,self.wturl)
        elif controlId == 801: self.close()

    def addListagem(self,nome,i):
          if nome=='[B][COLOR blue]Firedrive[/B]':
                thumb=wtpath + art + 'firedrive.png'
                self.criarelemento(nome,'firedrive',i,thumb)
          elif nome=='[B][COLOR orange]Bay[/COLOR][COLOR white]Files[/COLOR][/B]':
                thumb=wtpath + art + 'bayfiles2.png'
                self.criarelemento(nome,'bayfiles',i,thumb)
          elif nome=='[B][COLOR white]Sockshare[/COLOR][/B]':
                thumb=wtpath + art + 'sockshare2.png'
                self.criarelemento(nome,'sockshare',i,thumb)
          elif nome=='[B][COLOR lime]Huge[/COLOR][COLOR green]files[/COLOR][/B]':
                thumb=wtpath + art + 'hugefiles.png'
                self.criarelemento(nome,'hugefiles',i,thumb)
          elif nome=='[B][COLOR white]Profity[/COLOR][/B]':
                thumb=wtpath + art + 'profity.png'
                self.criarelemento(nome,'profity',i,thumb)
          elif nome=='[B][COLOR white]Kingfiles[/COLOR][/B]':
                thumb=wtpath + art + 'kingfiles.png'
                self.criarelemento(nome,'kingfiles',i,thumb)
          elif nome=='[B][COLOR white]Video[/COLOR][COLOR blue]Share[/COLOR][/B]':
                thumb=wtpath + art + 'vshare.png'
                self.criarelemento(nome,'videoshare',i,thumb)

          elif nome=='Dropvideo':
                thumb=wtpath + art + 'dropvideo.png'
                self.criarelemento(nome,'videocloud',i,thumb)

          elif nome=='Cloudzilla':
                thumb=wtpath + art + 'cloudzilla.png'
                self.criarelemento(nome,'videocloud',i,thumb)

          elif nome=='Vidto':
                thumb=wtpath + art + 'vidto.png'
                self.criarelemento(nome,'videoclou',i,thumb)

          elif nome=='Played':
                thumb=wtpath + art + 'played.png'
                self.criarelemento(nome,'videocloud',i,thumb)
            
    def criarelemento(self,nome,servername,i,thumb):
          listControl = self.getControl(500)
          item = xbmcgui.ListItem(nome, iconImage = thumb)
          item.setProperty('thumb', thumb)
          item.setProperty('ligacao', self.ligacao[i])
          listControl.addItem(item)
             
def upzin(url,srt,name,thumbnail,simounao,wturl):
      mensagemprogresso.update(50)
      link1 = abrir_url(url)
      try:
            fileid=re.compile('<input type="hidden" name="fileID" value="(.+?)" />').findall(link1)[0]
            hashfile=re.compile('<input type="hidden" name="fileHash" value="(.+?)" />').findall(link1)[0]
      except: ok = mensagemok("wareztuga.tv",traducao(40053)); return
      values = {'fileID':fileid,'fileHash': hashfile}
      downloadurl='http://www.upzin.com/' + re.compile('<form id="dlInfo" method="post" action="(.+?)">').findall(link1)[0]
      headers = { 'User-Agent' : user_agent}
      data = urllib.urlencode(values)
      try:
            req = urllib2.Request(downloadurl, data, headers)
            response = urllib2.urlopen(req)
            link = response.read()
            response.close()
      except:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      code = re.compile('<a href="(.+?)" id="downloadBtn" class="downloadBtn">Download File</a>').findall(link)[0]
      mensagemprogresso.update(100)
      if simounao=='download':
            fezdown=fazerdownload(name,code,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,code,name,thumbnail,wturl,False)
                            
def firedrive(url,srt,name,thumbnail,simounao,wturl):      
      mensagemprogresso.update(33)
      link1 = abrir_url(url)
      link2 = redirect(url)
      try: hash=re.compile('type="hidden" name="confirm" value="(.+?)"').findall(link1)[0]
      except: ok = mensagemok("wareztuga.tv",traducao(40053)); return
      if re.search('captcha_code',link1):
            ##CAPTCHA##
            from t0mm0.common.net import Net
            from t0mm0.common.addon import Addon
            net = Net()
            puzzle_img = os.path.join(pastaperfil, "putcaptcha.png")
            imagemcaptcha=re.compile('<img src="/include/captcha.php.+?CAPTCHA(.+?)"').findall(link1)[0]
            headers={'Accept':'image/webp,*/*;q=0.8','Host':'www.filedrive.com','Pragma':'no-cache','Referer':url,'User-Agent':user_agent}
            open(puzzle_img, 'wb').write(net.http_GET('http://www.' + url[11:20] + '.com/include/captcha.php?_CAPTCHA'+imagemcaptcha,headers=headers).content)
            img = xbmcgui.ControlImage(450,15,400,130,puzzle_img )
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            kb = xbmc.Keyboard('', 'Introduza as letras da imagem', False)
            kb.doModal()
            capcode = kb.getText()
            try:os.remove(puzzle_img)
            except: pass
            if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '': solution = kb.getText()
               elif userInput == '':
                   mensagemok("wareztuga.tv","Nenhum texto inserido.")
                   return False
            else: return False  
            wdlg.close()
            values = {'captcha_code':capcode, 'hash': hash, 'confirm':'Continue as Free User'}
      else: values = {'confirm':hash}
      headers = { 'User-Agent' : user_agent}
      try:
            try:
                  data = urllib.urlencode(values)
                  req = urllib2.Request(link2, data, headers)
                  response = urllib2.urlopen(req)
                  link = response.read()
                  response.close()
            except urllib2.HTTPError, e:
                  mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
                  sys.exit(0)
            except urllib2.URLError, e:
                  mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
                  sys.exit(0)
      except:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      try:put1 = re.compile('<a class="ad_button" href="(.+?)">Download file</a>').findall(link)[0]
      except:
            try:put1 = re.compile("href='(.+?)'><i></i> <span trans='dd'>Direct Download</span></a>").findall(link)[0]
            except: ok = mensagemok("wareztuga.tv",traducao(40168),traducao(40169)); return
      if re.search('<h1>Server is Overloaded</h1>',link): ok = mensagemok("wareztuga.tv","Servidor sobrecarregado.","Tente novamente daqui a minutos."); return
      mensagemprogresso.update(66)      
      try: put2 = redirect(put1)
      except:
            print "Nao conseguiu obter link final. Link final e o inicial"
            put2=put1
      mensagemprogresso.update(100)
      if simounao=='download':
            fezdown=fazerdownload(name,put2,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,put2,name,thumbnail,wturl,False)

def sockshare(url,srt,name,thumbnail,simounao,wturl):      
      mensagemprogresso.update(33)
      link1 = abrir_url(url)
      link2 = redirect(url)
      try: hash=re.compile('type="hidden" value="(.+?)" name="hash"').findall(link1)[0]
      except: ok = mensagemok("wareztuga.tv",traducao(40053)); return
      if re.search('captcha_code',link1):
            ##CAPTCHA##
            from t0mm0.common.net import Net
            from t0mm0.common.addon import Addon
            net = Net()
            puzzle_img = os.path.join(pastaperfil, "putcaptcha.png")
            imagemcaptcha=re.compile('<img src="/include/captcha.php.+?CAPTCHA(.+?)"').findall(link1)[0]
            headers={'Accept':'image/webp,*/*;q=0.8','Host':'www.sockshare.com','Pragma':'no-cache','Referer':url,'User-Agent':user_agent}
            open(puzzle_img, 'wb').write(net.http_GET('http://www.' + url[11:20] + '.com/include/captcha.php?_CAPTCHA'+imagemcaptcha,headers=headers).content)
            img = xbmcgui.ControlImage(450,15,400,130,puzzle_img )
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            kb = xbmc.Keyboard('', 'Introduza as letras da imagem', False)
            kb.doModal()
            capcode = kb.getText()
            try:os.remove(puzzle_img)
            except: pass
            if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '': solution = kb.getText()
               elif userInput == '':
                   mensagemok("wareztuga.tv","Nenhum texto inserido.")
                   return False
            else: return False  
            wdlg.close()
            values = {'captcha_code':capcode, 'hash': hash, 'confirm':'Continue as Free User'}
      else: values = {'hash': hash, 'confirm':'Continue as Free User'}
      headers = { 'User-Agent' : user_agent}
      try:
            try:
                  data = urllib.urlencode(values)
                  req = urllib2.Request(link2, data, headers)
                  response = urllib2.urlopen(req)
                  link = response.read()
                  response.close()
            except urllib2.HTTPError, e:
                  mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
                  sys.exit(0)
            except urllib2.URLError, e:
                  mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
                  sys.exit(0)
      except:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      link=link.replace(' onclick="ntad()"','')
      code = re.compile('<a href="/(.+?)">Download File</a>').findall(link)
      if re.search('<h1>Server is Overloaded</h1>',link): ok = mensagemok("wareztuga.tv","Servidor sobrecarregado.","Tente novamente daqui a minutos."); return
      mensagemprogresso.update(66)
      try:put1 = 'http://www.' + url[11:20] + '.com/' + code[0]
      except: ok = mensagemok("wareztuga.tv",traducao(40168),traducao(40169)); return
      try: put2 = redirect(put1)
      except:
            print "Nao conseguiu obter link final. Link final e o inicial"
            put2=put1
      mensagemprogresso.update(100)
      if simounao=='download':
            fezdown=fazerdownload(name,put2,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,put2,name,thumbnail,wturl,False)

def bayfiles(url,srt,name,thumbnail,simounao,wturl):
      link=abrir_url(url)
      try:
            try:
                  match2=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) has recently downloaded a file. Upgrade to premium or wait (.+?) min.</strong>').findall(link)[0]
                  ok = mensagemok("wareztuga.tv",traducao(40059), ' (' + match[0][0] + '). ' + traducao(40060) + match[0][1] + traducao(40061))
                  return
            except:
                  match3=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) is already downloading. Upgrade to premium or wait.</strong>').findall(link)
                  ok = mensagemok("wareztuga.tv",traducao(40062), ' (' + match3[0] + ')')
                  return
      except:
            video_urls = []
            try: vfid = re.compile('var vfid = ([^;]+);').findall(link)[0]
            except:
                  ok = mensagemok("wareztuga.tv",traducao(40063))
                  print "Vfid não encontrado"
                  return ''
            try:urlpremium='http://'+ re.compile('<a class="highlighted-btn" href="http://(.+?)">Premium Download</a>').findall(link)[0]
            except:urlpremium=[]
            if urlpremium:
                  if simounao=='download':
                        fezdown=fazerdownload(name,urlpremium,subtitles=srt)
                        encerrarsistema()
                  elif simounao=='agora':
                        comecarvideo(srt,urlpremium,name,thumbnail,wturl,False)
            else:
                  if simounao=='agora': ok = mensagemok(traducao(40056),traducao(40057),traducao(40058))
                  try:
                        delay = re.compile('var delay = ([^;]+);').findall(link)[0]
                        delay = int(delay)
                  except: delay = 300
                  t = millis()
                  datajson=load_json(abrir_url("http://bayfiles.net/ajax_download?_=%s&action=startTimer&vfid=%s"%(t,vfid)))
                  if datajson['set']==True:
                        token=datajson['token']
                        resultado = handle_wait(delay,"wareztuga.tv",traducao(40064))
                        url_ajax = 'http://bayfiles.net/ajax_download'
                        post = "action=getLink&vfid=%s&token=%s" %(vfid,token)
                        finaldata= abrir_url(url_ajax + '?' + post)
                        patron = 'onclick="javascript:window.location.href = \'(.+?)\''
                        matches = re.compile(patron,re.DOTALL).findall(finaldata)
                        try:funcional = matches[0] #final url mp4
                        except: return
                        if simounao=='download':
                              fezdown=fazerdownload(name,funcional,subtitles=srt)
                              encerrarsistema()
                        elif simounao=='agora':
                              comecarvideo(srt,funcional,name,thumbnail,wturl,True)

def hugefiles(url,srt,name,thumbnail,simounao,wturl):
      mensagemprogresso.update(33)
      from t0mm0.common.net import Net
      net = Net()
      #stupid timeout,retry
      link=abrir_url(url)
      if re.search('/404.html',link):
            mensagemok('wareztuga.tv','Ficheiro não disponível.')
            sys.exit(0)
      from random import randint
      captcha_img = os.path.join(pastacaptcha,str(randint(0, 9999999))+ ".png")

      captchatype,hugekey=obter_captcha(url,link,captcha_img)

      try: solved,id = solvevia9kw(captcha_img)
      except:
            solved = ''
            id = ''
      if solved != '':
            puzzle = solved
      else:
            solver = InputWindow(captcha=captcha_img)
            puzzle = solver.get()
      try:os.remove(captcha_img)
      except: pass
      if puzzle:
            mensagemprogresso.update(66)
            op=re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
            usr_login=''
            rand=re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(link)[0]
            id=re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
            fname=re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
            referer=''
            ctype=re.compile('<input type="hidden" name="ctype" value="(.+?)">').findall(link)[0]
            method=re.compile('name="method_free".+?value="(.+?)"').findall(link)[0]
            
            if captchatype=="solvemedia":
                  verify_data={'adcopy_response':puzzle,'k':vk,'l':vl,'t':vt,'s':vs,'magic':vm,'adcopy_challenge':vc}
                  headers={'User-Agent':user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer':noscripturl}
                  link= net.http_POST('http://api.solvemedia.com/papi/' + vp,form_data=verify_data,headers=headers).content.encode('latin-1','ignore')
            
                  redirecturl=re.compile('URL=(.+?)"').findall(link)[0]
                  conteudo=net.http_GET(redirecturl).content
                  if re.search('&error=1',conteudo) or re.search('Try again',conteudo):form_data={}
                  else:
                        hugekey=re.compile('<textarea.+?>(.+?)<').findall(conteudo)[0]
                        form_data={'op':op,'usr_login':usr_login,'rand':rand,'id':id,'fname':fname,'referer':referer,'ctype':ctype,'adcopy_response':puzzle,'adcopy_challenge':hugekey,'method_free':method}
            elif captchatype=="recaptcha":
                  form_data={'op':op,'usr_login':usr_login,'rand':rand,'id':id,'fname':fname,'referer':referer,'ctype':ctype,'recaptcha_challenge_field':hugekey.group(1),'recaptcha_response_field':puzzle,'method_free':method}
            link= net.http_POST(url,form_data=form_data).content.encode('latin-1','ignore')
            try:streamurl=re.compile('var fileUrl = "(.+?)"').findall(link)[0]
            except:
                  if id != '': 
                        try: Ninekwusercaptchacorrectback(id,"2")
                        except: pass
                  opcao=xbmcgui.Dialog().yesno(traducao(40123),traducao(40348),'Tentar novamente?')
                  if opcao:
                        hugefiles(url,srt,name,thumbnail,simounao,wturl)
                        return
                  else:
                        sys.exit(0)
                  
            if id != '':
                  try: Ninekwusercaptchacorrectback(id,"1")
                  except: pass

            mensagemprogresso.update(100)
            if simounao=='download':
                  mensagemprogresso.close()
                  fezdown=fazerdownload(name,streamurl,subtitles=srt)
                  encerrarsistema()
            elif simounao=='agora':
                  comecarvideo(srt,streamurl,name,thumbnail,wturl,False)

      else:mensagemprogresso.close()

def profity(url,srt,name,thumbnail,simounao,wturl):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      timeout=int(re.compile('var seconds = (.+?);').findall(link)[0])
      #resultado = handle_wait(timeout,"wareztuga.tv",traducao(40349))
      resultado=True
      cookie1=urllib.quote(response.info()['Set-Cookie'].split(';')[0])
      cookie2=urllib.quote('; __atuvc=1%7C41')
      streamurl=re.compile("download-timer'\).html\(.+?<a href='(.+?)'>").findall(link)[0]
      streamurlwcook= '%s|Cookie=%s%s' % (streamurl,cookie1,cookie2)
      #if resultado:
            #abrir_url(streamurl)
            #xbmc.sleep(1000)
            #redirect(streamurlwcook)
      comecarvideo(srt,streamurlwcook,name,thumbnail,wturl,True)
      
def kingfiles(url,srt,name,thumbnail,simounao,wturl):      
      from t0mm0.common.net import Net
      net = Net()
      link=abrir_url(url)
      if re.search('/404.html',link):
            mensagemok('wareztuga.tv','Ficheiro não disponível.')
            sys.exit(0)
      op=re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
      fname=re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
      usr_login=''
      id=re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
      referer=''
      method=re.compile('name="method_free".+?value="(.+?)"').findall(link)[0]
      form_data={'op':op,'usr_login':usr_login,'id':id,'fname':fname,'referer':referer,'method_free':method}
      link= net.http_POST(url,form_data=form_data).content.encode('latin-1','ignore')
      mensagemprogresso.update(33)
      
      from random import randint
      captcha_img = os.path.join(pastacaptcha,str(randint(0, 9999999)) + ".png")

      captchatype=obter_captcha(url,link,captcha_img)
      
      try: solved,id = solvevia9kw(captcha_img)
      except:
            solved = ''
            id = ''
      if solved != '':
            puzzle = solved
      else:
            solver = InputWindow(captcha=captcha_img)
            puzzle = solver.get()
      try:os.remove(captcha_img)
      except: pass
      if puzzle:
            mensagemprogresso.update(66)
            op=re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
            rand=re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(link)[0]
            id=re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
            #fname=re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
            downdirect=re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(link)[0]
            referer=''
            method=''
            methodpremium=''

            if captchatype=="solvemedia":
                  verify_data={'adcopy_response':puzzle,'k':vk,'l':vl,'t':vt,'s':vs,'magic':vm,'adcopy_challenge':vc}
                  headers={'User-Agent':user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer':noscripturl}
                  link= net.http_POST('http://api.solvemedia.com/papi/' + vp,form_data=verify_data,headers=headers).content.encode('latin-1','ignore')
            
                  redirecturl=re.compile('URL=(.+?)"').findall(link)[0]
                  conteudo=net.http_GET(redirecturl).content
                  if re.search('&error=1',conteudo) or re.search('Try again',conteudo):form_data={}
                  else:
                        hugekey=re.compile('<textarea.+?>(.+?)<').findall(conteudo)[0]
                        form_data={'op':op,'rand':rand,'id':id,'referer':url,'adcopy_response':"manual_challenge",'adcopy_challenge':hugekey,'method_free':' ','method_premium':methodpremium,'down_direct':downdirect}
                        
            elif captchatype=="recaptcha":
                  form_data={'op':op,'rand':rand,'id':id,'fname':fname,'referer':referer,'recaptcha_challenge_field':hugekey.group(1),'recaptcha_response_field':puzzle,'method_free':method,'method_premium':methodpremium,'down_direct':downdirect}
            
            link= net.http_POST(url,form_data=form_data).content.encode('latin-1','ignore')
            try:streamurl=re.compile("var download_url = '(.+?)'").findall(link)[0]
            except:
                  if id != '':
                        try: Ninekwusercaptchacorrectback(id,"2")
                        except: pass
                  opcao=xbmcgui.Dialog().yesno(traducao(40123),traducao(40348),'Tentar novamente?')
                  if opcao:
                        kingfiles(url,srt,name,thumbnail,simounao,wturl)
                        return
                  else:
                        sys.exit(0)
                  
            mensagemprogresso.update(100)
            if id != '':
                  try: Ninekwusercaptchacorrectback(id,"1")
                  except: pass
            if simounao=='download':
                  mensagemprogresso.close()
                  fezdown=fazerdownload(name,streamurl,subtitles=srt)
                  encerrarsistema()
            elif simounao=='agora':
                  comecarvideo(srt,streamurl,name,thumbnail,wturl,False)

      else:mensagemprogresso.close()

def videoshare(url,srt,name,thumbnail,simounao,wturl):      
      from t0mm0.common.net import Net
      net = Net()
      link=abrir_url(url)
      op=re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
      fname=re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
      usr_login=''
      id=re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
      referer=''
      method=re.compile('name="method_free".+?value="(.+?)"').findall(link)[0]
      form_data={'op':op,'usr_login':usr_login,'id':id,'fname':fname,'referer':referer,'method_free':method}
      link= net.http_POST(url,form_data=form_data).content.encode('latin-1','ignore')
      streamurl=re.compile('file: "(.+?)",').findall(link)[0]
      mensagemprogresso.update(100)
      if simounao=='download':
            mensagemprogresso.close()
            fezdown=fazerdownload(name,streamurl,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,streamurl,name,thumbnail,wturl,False)

def dropvideo(url,srt,name,thumbnail,simounao,wturl):      
      link=abrir_url(url)

      try:streamurl=re.compile('var vurl2 = "(.+?)"').findall(link)[0] #dropvideo
      except: streamurl=re.compile('var vurl = "(.+?)"').findall(link)[0] #cloudzilla
      
      mensagemprogresso.update(100)
      if simounao=='download':
            mensagemprogresso.close()
            fezdown=fazerdownload(name,streamurl,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,streamurl,name,thumbnail,wturl,False)

def played(url,srt,name,thumbnail,simounao,wturl):
      link=abrir_url(url)
      streamurl=re.compile('file: "(.+?)",').findall(link)[0]
      mensagemprogresso.update(100)
      if simounao=='download':
            mensagemprogresso.close()
            fezdown=fazerdownload(name,streamurl,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,streamurl,name,thumbnail,wturl,False)


def vidto(url,srt,name,thumbnail,simounao,wturl):
      link=abrir_url(url)
      jsU = JsUnpackerV2()
      link = jsU.unpackAll(link)
      streamurl=re.compile('file:"(.+?)"').findall(link)[-1]
      mensagemprogresso.update(100)
      if simounao=='download':
            mensagemprogresso.close()
            fezdown=fazerdownload(name,streamurl,subtitles=srt)
            encerrarsistema()
      elif simounao=='agora':
            comecarvideo(srt,streamurl,name,thumbnail,wturl,False)

def obter_captcha(url,link,captcha_img):
      from t0mm0.common.net import Net
      net = Net()
      try:
            print "Solvemedia"
            captchatype="solvemedia"
            noscript=re.compile('<iframe src=".+?solvemedia.com([^"]+?)"').findall(link)[0]
            global noscripturl,vk,vl,vt,vs,vm,vc,vp,vk
            noscripturl="http://api.solvemedia.com"+ noscript
            headers={'User-Agent':user_agent,'Referer':url}
            check = net.http_GET(noscripturl,headers=headers).content
            urlimagem=str(re.compile('<img src="(.+?)"').findall(check)[0])
            vk=re.compile('<input type=hidden name="k" value="(.+?)"').findall(check)[0]
            vl=re.compile('<input type=hidden name="l" value="(.+?)"').findall(check)[0]
            vt=re.compile('<input type=hidden name="t" value="(.+?)"').findall(check)[0]
            vs=re.compile('<input type=hidden name="s" value="(.+?)"').findall(check)[0]
            vm=re.compile('<input type=hidden name="magic" value="(.+?)"').findall(check)[0]
            vc=re.compile('<input type=hidden name="adcopy_challenge".+?value="(.+?)">').findall(check)[0]
            vp=re.compile('<form method="post" action="(.+?)"').findall(check)[0]
            open(captcha_img, 'wb').write( net.http_GET("http://api.solvemedia.com"+urlimagem,headers=headers).content)
            return captchatype,False
      except:
            try:
                  print "Recaptcha"
                  captchatype="recaptcha"
                  headers={'Referer': url}
                  noscript=re.compile('src=".+?recaptcha/api/([^"]+?)">').findall(link)[0]
                  check = net.http_GET('http://www.google.com/recaptcha/api/' + noscript,headers=headers).content
                  hugekey = re.search("challenge \: \\'(.+?)\\'", check)
                  open(captcha_img, 'wb').write(net.http_GET('http://www.google.com/recaptcha/api/image?c='+hugekey.group(1)).content)
                  return captchatype,hugekey
            except:
                  mensagemok('wareztuga.tv','Erro a obter captcha.')
                  sys.exit(0)
                  return False,False
      

########################################################### PLAYER ################################################

def comecarvideo(srt,finalurl,name,thumbnail,wturl,proteccaobay):
      import socket
      socket.setdefaulttimeout(1000)
      playlist = xbmc.PlayList(1)
      playlist.clear()
      episname=True
      show=True
      if selfAddon.getSetting('download-subsexterno2') == 'true' and downloadPath=='':
            ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
            selfAddon.openSettings()
            return
      if selfAddon.getSetting('download-subsexterno2') == 'true': fazerdownload2(name,srt)
      listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)            
      if re.search('Temp.', name):
            conteudopagina=abrir_url_cookie(wturl)
            seasonurl=re.compile('<a href="([^"]+?)" class="slctd">').findall(conteudopagina)[0]
            serie=re.compile('<title>wareztuga.tv - .+? - (.+?): Temporada (.+?), Epis.+?io (.+?)</title>').findall(conteudopagina)[0]
            show=re.compile('<div class="thumb serie" title="(.+?)">').findall(conteudopagina)[0]
            season=serie[1]
            episode=serie[2]
            conteudopagina=conteudopagina.replace('(','').replace('<span>)','-')
            try:year=re.compile('<span class="year"><span> </span>(.+?)-').findall(conteudopagina)[0]
            except: year=0
            try:imdbcode=re.compile('<a href="http://www.imdb.com/title/(.+?)/').findall(conteudopagina)[0]
            except: imdbcode=''
            if imdbcode.startswith('tt'):
                  if selfAddon.getSetting('trakt-improve') == 'true':
                        try:
                              temp=abrir_url('http://api.trakt.tv/show/summaries.json/b6135e0f7510a44021fac8c03c36c81a17be35d9/%s' % (imdbcode))
                              show=re.compile('"title":"(.+?)"').findall(temp)[0]
                        except: pass
            print "Estou a ver a serie " + str(show) + " S" + serie[1] + "E" + serie[2] + " - " + serie[0] + " (" + str(year) + "/" + str(imdbcode) + ")" 
            listitem.setInfo("Video", {"title":serie[0],"year":int(year),"imdbnumber":imdbcode,"code":imdbcode,"TVShowTitle": show,"Season":int(serie[1]),"Episode":int(serie[2]),"type":"episode"})
            warezid=thumbnail.replace(MainURL + 'images/thumbs/thumb','').replace(MainURL + 'images/series_v2_thumbs/thumb','').replace('.png','').replace(MainURL + 'images/thumbs/thumb','')            
            tipo='episodes'
      else:
            name=name+'-'
            conteudopagina=abrir_url_cookie(wturl)
            seasonurl=''
            
            season=False
            episode=False
            conteudopagina=conteudopagina.replace('(','').replace('<span>)','-')
            try:year=re.compile('<span class="year"><span> </span>(.+?)-').findall(conteudopagina)[0]
            except: year=0
            try:nomeingles=re.compile('<span class="original-name">- "(.+?)"</span>').findall(conteudopagina)[0]
            except:nomeingles=''
            try:imdbcode=re.compile('<a href="http://www.imdb.com/title/(.+?)/').findall(conteudopagina)[0]
            except: imdbcode=''
            show=nomeingles
            if imdbcode.startswith('tt'):
                  if selfAddon.getSetting('trakt-improve') == 'true':
                        try:
                              temp=abrir_url('http://api.trakt.tv/movie/summaries.json/b6135e0f7510a44021fac8c03c36c81a17be35d9/%s' % (imdbcode))
                              nomeingles=re.compile('"title":"(.+?)"').findall(temp)[0]
                        except: pass
            print "Estou a ver o filme " + str(nomeingles) + " (" + str(year) + "/" + str(imdbcode) + ")" 
            listitem.setInfo("Video", {"title":nomeingles,"imdbnumber":imdbcode,"code":imdbcode,"imdb_id":imdbcode,"year":int(year),"type":"movie"})
            warezid=thumbnail.replace('http://www.wareztuga.tv/images/movies_thumbs/thumb','').replace('.png','')            
            tipo='movies'
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      
      playlist.add(finalurl, listitem)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
      player = Player(tipo=tipo,warezid=warezid,videoname=name,thumbnail=thumbnail,proteccaobay=proteccaobay,wturl=wturl,imdbcode=imdbcode,seasonurl=seasonurl,show=show,season=season,episode=episode,year=year)
      mensagemprogresso.close()
      player.play(playlist)
      
      if selfAddon.getSetting('subtitles-activate') == 'true': player.setSubtitles(srt)
      while player._playbackLock:
            player._trackPosition()
            xbmc.sleep(5000)

## THX 1CH ##
class Player(xbmc.Player):
      def __init__(self,tipo,warezid,videoname,thumbnail,proteccaobay,wturl,imdbcode,seasonurl,show,season,episode,year):
            if selfAddon.getSetting("playertype") == "0": xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            elif selfAddon.getSetting("playertype") == "1": xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
            elif selfAddon.getSetting("playertype") == "2": xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
            elif selfAddon.getSetting("playertype") == "3": xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
            else: xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            self._playbackLock = True
            self._refInfo = True
            self._totalTime = 999999
            self.tipo = tipo
            self.warezid = warezid
            self.videoname = videoname
            self.thumbnail = thumbnail
            self.proteccaobay = proteccaobay
            self.imdbcode = imdbcode
            self.wturl=wturl
            self.seasonurl=seasonurl
            self.show=show
            self.season=season
            self.episode=episode
            self.year=year
            self._lastPos = 0
            self.nomeficheiro=self.tipo + '_' + self.warezid
            if self.tipo=='episodes':
                  self.file='%s S%sE%s.strm' % (self.show, self.season,self.episode)
            else:
                  self.file=self.show + ' _' + str(self.year) + '_.strm'
            self.caminhoficheiro=os.path.join(pastaperfil, self.nomeficheiro)
            self.caminhoficheiroinfo=os.path.join(pastaperfil,self.nomeficheiro + '_info')
            print "Criou o player"
            
      def onPlayBackStarted(self):
            print "Comecou o player"
            self._totalTime = self.getTotalTime()
            #if self.tipo=='episodes':
            ##      xbmcJsonRequest({"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetTVShowDetails", "params": {"imdbnumber": self.imdbcode}})
            #elif self.tipo=='movies':
            #      xbmcJsonRequest({"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"imdbnumber": self.imdbcode}})
            if selfAddon.getSetting('marcadores') == 'true':
                  if self.proteccaobay == False:                  
                        if os.path.exists(self.caminhoficheiro):
                              print "Existe um marcador. A perguntar."
                              bookmark=openfile(self.caminhoficheiro)
                              opcao=xbmcgui.Dialog().yesno("wareztuga.tv", '',traducao(40173) + ' %s?' % (format_time(float(bookmark))),'', traducao(40174), traducao(40175))
                              if opcao: self.seekTime(float(bookmark))
            if self.show != False and self.tipo=='episodes':
                  savefile(pastaperfil,'following.txt','"name":"%s","url":"%s"' % (self.show,self.seasonurl))
                              
      def onPlayBackStopped(self):
            print "Parou o player"
            self._playbackLock = False
            playedTime = int(self._lastPos)
            watched_values = [.7, .8, .9, .95]
            min_watched_percent = watched_values[int(selfAddon.getSetting('watched-percent'))]
            print 'playedTime / totalTime : %s / %s = %s' % (playedTime, self._totalTime, playedTime/self._totalTime)
            xbmc.sleep(5001)
            if playedTime == 0 and self._totalTime == 999999: raise PlaybackFailed('XBMC falhou a comecar o playback')
            elif ((playedTime/self._totalTime) > min_watched_percent):
                  if selfAddon.getSetting('marcadores') == 'true':
                        if self.proteccaobay == False:
                              try:os.remove(self.caminhoficheiro)
                              except: pass
                              try:os.remove(self.caminhoficheiroinfo)
                              except: pass
                  if selfAddon.getSetting('watched-enable') == 'true':
                        print "A marcar como visto"
                        accaonosite(self.tipo,self.warezid,'watched')
                        try:
                              import json
                              if self.tipo=='episodes':
                                    episodeid = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"]}, "id": 1}' % (self.season, self.episode))
                                    episodeid = unicode(episodeid, 'utf-8', errors='ignore')
                                    episodeid = json.loads(episodeid)['result']['episodes']
                                    episodeid = [i for i in episodeid if i['file'].endswith(self.file)][0]
                                    episodeid = episodeid['episodeid']
                                    while xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]) or xbmc.getInfoLabel('Container.FolderPath') == '': xbmc.sleep(1000)
                                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(episodeid))
                              elif self.tipo=='movies':
                                    movieid = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                                    movieid = unicode(movieid, 'utf-8', errors='ignore')
                                    movieid = json.loads(movieid)['result']['movies']
                                    movieid = [i for i in movieid if i['file'].endswith(self.file)][0]
                                    movieid = movieid['movieid']
                                    while xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]) or xbmc.getInfoLabel('Container.FolderPath') == '': xbmc.sleep(1000)
                                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(movieid))
                        except: pass
                  else: print "Marcacao automatica desactivada"
                  naopede=encerrarsistema()
                  if not naopede:
                        if selfAddon.getSetting('opiniaonofim') == 'true':
                              if self.tipo=='movies':
                                    opcao= xbmcgui.Dialog().yesno("wareztuga.tv", traducao(40194))
                                    if opcao:
                                          xbmc.executebuiltin("XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentar'),'movies',self.warezid,str(self.wturl),'')]) + ")")
                                          xbmc.executebuiltin("XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('votar'),'movies',self.warezid,str(self.wturl),'')]) + ")")
                              elif self.tipo=='episodes':
                                    opcao= xbmcgui.Dialog().yesno("wareztuga.tv", traducao(40195))
                                    if opcao: xbmc.executebuiltin("XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentar'),'episodes',self.warezid,str(self.wturl),'')]) + ")")
            else: print 'Nao atingiu a marca das definicoes. Nao marcou como visto.'

      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'

      def _trackPosition(self):
            try: self._lastPos = self.getTime()
            except: print 'Erro quando estava a tentar definir o tempo de playback'
            if selfAddon.getSetting('marcadores') == 'true':
                  if self.proteccaobay == False:
                        if (self._lastPos>15):
                              if self._refInfo == True:
                                    savefile(pastaperfil,self.nomeficheiro + '_info',self.videoname + 'T-' + self.thumbnail + '-T-' + self.wturl + '-')
                                    self._refInfo = False
                              savefile(pastaperfil,self.nomeficheiro,str(self._lastPos))

class PlaybackFailed(Exception):
      '''XBMC falhou a carregar o stream'''

def atalhos():
      #addAtalho(name,url,mode,iconimage,interrompido,total,pasta):
      ref=0
      lista=os.listdir(pastaperfil)
      for info in lista:
            if re.search('info',info) or re.search('settings',info) or re.search('cookie',info): pass
            else:
                  ref=1
                  try:
                        caminho=openfile(info + '.txt')
                        evolucacao=openfile(info + '_info.txt')
                        addAtalho(ficheiros,caminho,24,'',len(total),False)
                        #addInterrompido(umapenas[0],umapenas[2],5,umapenas[1],info,len(lista),False)
                  except: pass
      if (ref==0): addLink('[B][COLOR white]' + traducao(40176) + '[/COLOR][/B]','','')

def guardaratalhos(name,url):
      if not os.path.exists(pastafavoritos):
          os.makedirs(pastafavoritos)
      from random import randint
      nomeficheiro=str(randint(0, 9999999))
      savefile(pastafavoritos,nomeficheiro + '.txt',url)
      savefile(pastafavoritos,nomeficheiro + '_info.txt',selfAddon.getSetting('ultima-pasta') + ' >> ' + name)
      xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,Adicionado aos atalhos,'500000',"+iconpequeno.encode('utf-8')+")")

def apagaratalhos(name,url):
      favorito=os.path.join(pastafavoritos,url)
      os.remove(favorito)
      xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,Removido dos atalhos,'500000',"+iconpequeno.encode('utf-8')+")")
      xbmc.executebuiltin("Container.Refresh")

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addInterrompido(name,url,mode,iconimage,interrompido,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      cm = []
      cm.append((traducao(40196),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('interrompido'),interrompido,'',str(url),'')]) + ")"))
      cm.append((traducao(40228), 'XBMC.RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      liz.addContextMenuItems(cm, replaceItems=True)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addAtalho(name,url,mode,iconimage,interrompido,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      cm = []
      cm.append((traducao(40196),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('interrompido'),interrompido,'',str(url),'')]) + ")"))
      liz.addContextMenuItems(cm, replaceItems=True)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      cm = []
      #cm.append(('Adicionar Atalho',"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('interrompido'),'interrompido','',str(url),'')]) + ")"))
      liz.addContextMenuItems(cm, replaceItems=True)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addLista(name,url,mode,iconimage,total,pasta,descricao):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      cm = []
      #cm.append(('Adicionar Atalho',"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('interrompido'),'interrompido','',str(url),'')]) + ")"))
      liz.addContextMenuItems(cm, replaceItems=True)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addTemp(name,url,mode,iconimage,total,pasta):      
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      if seriefanart:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&seriefanart=" + urllib.quote_plus(seriefanart)
            fanart=seriefanart
      else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            fanart="%s/fanart.jpg"%selfAddon.getAddonInfo("path")
      liz.setProperty('fanart_image', fanart)
      cm = []
      #cm.append(('Adicionar Atalho',"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('interrompido'),'interrompido','',str(url),'')]) + ")"))
      liz.addContextMenuItems(cm, replaceItems=True)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addSerie(name,url,mode,iconimage,genre,year,cast,cadeia,plot,fanart,rating,cert,nrepisodios,estreia,votes,estado,idserie,duration,subsc,overlay,faved,warezid,total):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&seriefanart=" + urllib.quote_plus(fanart)
      if overlay==6: playcount=0
      else: playcount=1
      liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name,
                                              "overlay":overlay,
                                              "playcount":playcount,
                                              "Genre": genre,
                                              "Cast": cast,
                                              "studio": cadeia,
                                              "Plot": plot,
                                              "Year": year,
                                              "OriginalTitle": name,
                                              "mpaa": cert,
                                              "premiered": estreia,
                                              "status": estado,
                                              "rating": rating,
                                              "votes": votes,
                                              "duration": duration
                                              } )
      #"Rating": rating a causar problemas
      if not fanart: fanart="%s/fanart.jpg"%selfAddon.getAddonInfo("path")
      liz.setProperty('fanart_image', fanart)
      cm = []
      cm.append((traducao(40147), 'XBMC.Action(Info)'))
      if overlay==6: cm.append((traducao(40066),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('visto'),'series',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40067),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('visto'),'series',warezid,str(url),overlay)]) + ")"))
      if faved==0: cm.append((traducao(40075), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('faved'),'series',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40076), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('faved'),'series',warezid,str(url),overlay)]) + ")"))
      #cm.append((traducao(40068), 'XBMC.Action(Info)'))
      if subsc==0: cm.append((traducao(40149), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('subscribed'),'series',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40150), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('subscribed'),'series',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40071), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentarios'),'series',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40072), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentar'),'series',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40148), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('votar'),'series',warezid,str(url),overlay)]) + ")"))
      #cm.append(('Adicionar Atalho','XBMC.RunPlugin(%s?mode=22&url=%s&name=%s)' % (sys.argv[0], name,name)))
      liz.addContextMenuItems(cm, replaceItems=True)
      try:liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
      except: pass
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=total)

def addEpisodio(name,url,mode,iconimage,overlay,warezid,agendar,total):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      if overlay==6: playcount=0
      else: playcount=1
      liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name,
                                              "overlay":overlay,
                                              "playcount":playcount} )
      #liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      if seriefanart: fanart=seriefanart
      else: fanart="%s/fanart.jpg"%selfAddon.getAddonInfo("path")
      liz.setProperty('fanart_image', fanart)
      cm = []
      if overlay==6: cm.append((traducao(40066),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('visto'),'episodes',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40067),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('visto'),'episodes',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40228), 'XBMC.RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      #cm.append((traducao(40068), 'XBMC.Action(Info)'))
      if agendar==0: cm.append((traducao(40069), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('cliped'),'episodes',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40070), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('cliped'),'episodes',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40071), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentarios'),'episodes',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40072), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentar'),'episodes',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40197), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('reportar'),'episodes',warezid,str(url),overlay)]) + ")"))
      liz.addContextMenuItems(cm, replaceItems=True)
      try:liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
      except: pass
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)

def addPessoal(name,url,mode,iconimage,warezid,tipo,categoria,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      cm = []
      if tipo=='faved': cm.append((traducao(40073), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str(tipo),categoria,warezid,str(url),'')]) + ")"))
      if tipo=='cliped': cm.append((traducao(40070), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str(tipo),categoria,warezid,str(url),'')]) + ")"))
      if tipo=='subscribed': cm.append((traducao(40151), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str(tipo),categoria,warezid,str(url),'')]) + ")"))
      cm.append((traducao(40071), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentarios'),categoria,warezid,str(url),'')]) + ")"))
      cm.append((traducao(40072), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentar'),categoria,warezid,str(url),'')]) + ")"))
      if categoria=='episodes' or categoria=='movies': cm.append((traducao(40228), 'XBMC.RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      liz.addContextMenuItems(cm, replaceItems=True)
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)

def addFilme(name,url,mode,iconimage,titorig,genre,year,cast,director,plot,fanart,rating,cert,estreia,votes,moviedbid,imdbid,overlay,warezid,faved,agendar,total):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      if overlay==6: playcount=0
      else: playcount=1
      liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      try:
            liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                    "Genre": genre,
                                                    "Director": director,
                                                    "Plot": plot,
                                                    "OriginalTitle": titorig,
                                                    "Year": year,
                                                    "Rating": rating,
                                                    "votes": votes,
                                                    "Cast": cast,
                                                    "mpaa": cert,
                                                    "aired": estreia,
                                                    "overlay":overlay,
                                                    "playcount":playcount
                                                    } )
      except: pass
      if not fanart: fanart="%s/fanart.jpg"%selfAddon.getAddonInfo("path")
      liz.setProperty('fanart_image', fanart)
      cm = []
      cm.append((traducao(40074), 'XBMC.Action(Info)'))
      cm.append((traducao(40228), 'XBMC.RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      cm.append(('Adicionar à biblioteca', 'XBMC.RunPlugin(%s?mode=32&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      if overlay==6: cm.append((traducao(40066),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('visto'),'movies',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40067),"XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('visto'),'movies',warezid,str(url),overlay)]) + ")"))
      if faved==0: cm.append((traducao(40075), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('faved'),'movies',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40076), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('faved'),'movies',warezid,str(url),overlay)]) + ")"))
      #cm.append((traducao(40068), 'XBMC.Action(Info)'))
      if agendar==0: cm.append((traducao(40069), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('cliped'),'movies',warezid,str(url),overlay)]) + ")"))
      else: cm.append((traducao(40070), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('cliped'),'movies',warezid,str(url),overlay)]) + ")"))
      if moviedbid!=0: cm.append((traducao(40077), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('trailer'),'movies',moviedbid,str(url),overlay)]) + ")"))
      cm.append((traducao(40347), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('lersinopse'),'movies',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40071), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentarios'),'movies',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40072), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('comentar'),'movies',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40078), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('votar'),'movies',warezid,str(url),overlay)]) + ")"))
      cm.append((traducao(40198), "XBMC.RunScript(" + wtpath + "/resources/lib/visto.py" + ", " + str([(str('reportar'),'movies',warezid,str(url),overlay)]) + ")"))      
      liz.addContextMenuItems(cm, replaceItems=True)
      try:liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
      except: pass
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)

####################################################### VISTAS DEFAULT ###################################################

def vista_menus():
      menuview=selfAddon.getSetting('menu-view')
      if menuview == "0": xbmc.executebuiltin("Container.SetViewMode(50)")#lista
      elif menuview == "1": xbmc.executebuiltin("Container.SetViewMode(51)")#lista grande
      elif menuview == "2": xbmc.executebuiltin("Container.SetViewMode(500)")#miniatura
      return

def vista_filmes():
      moviesview=selfAddon.getSetting('movies-view4')
      if moviesview == "0": xbmc.executebuiltin("Container.SetViewMode(50)")#lista
      elif moviesview == "1": xbmc.executebuiltin("Container.SetViewMode(51)")#lista grande
      elif moviesview == "2": xbmc.executebuiltin("Container.SetViewMode(500)")#miniatura
      elif moviesview == "3": xbmc.executebuiltin("Container.SetViewMode(501)")#posters
      elif moviesview == "4": xbmc.executebuiltin("Container.SetViewMode(508)")#fanart
      elif moviesview == "5": xbmc.executebuiltin("Container.SetViewMode(504)")#media info1
      elif moviesview == "6": xbmc.executebuiltin("Container.SetViewMode(503)")#media info2
      elif moviesview == "7": xbmc.executebuiltin("Container.SetViewMode(515)")#media info3
      return

def vista_temporadas():
      seasonsview=selfAddon.getSetting('seasons-view')
      if seasonsview == "0": xbmc.executebuiltin("Container.SetViewMode(50)")
      elif seasonsview == "1": xbmc.executebuiltin("Container.SetViewMode(51)")
      elif seasonsview == "2": xbmc.executebuiltin("Container.SetViewMode(500)")##sem certeza
      elif seasonsview == "3": xbmc.executebuiltin("Container.SetViewMode(501)")
      elif seasonsview == "4": xbmc.executebuiltin("Container.SetViewMode(503)")
      return

def vista_episodios():
      episodesview=selfAddon.getSetting('episodes-view')
      if episodesview == "0": xbmc.executebuiltin("Container.SetViewMode(50)")
      elif episodesview == "1": xbmc.executebuiltin("Container.SetViewMode(51)")
      elif episodesview == "2": xbmc.executebuiltin("Container.SetViewMode(500)")##sem certeza
      elif episodesview == "3": xbmc.executebuiltin("Container.SetViewMode(503)")
      elif episodesview == "4": xbmc.executebuiltin("Container.SetViewMode(504)")
      return

def vista_series():
      seriesview=selfAddon.getSetting('series-view2')
      if seriesview == "0": xbmc.executebuiltin("Container.SetViewMode(50)")
      elif seriesview == "1": xbmc.executebuiltin("Container.SetViewMode(51)")
      elif seriesview == "2": xbmc.executebuiltin("Container.SetViewMode(500)")##sem certeza
      elif seriesview == "3": xbmc.executebuiltin("Container.SetViewMode(501)")
      elif seriesview == "4": xbmc.executebuiltin("Container.SetViewMode(508)")
      elif seriesview == "5": xbmc.executebuiltin("Container.SetViewMode(503)")
      elif seriesview == "6": xbmc.executebuiltin("Container.SetViewMode(504)")
      elif seriesview == "7": xbmc.executebuiltin("Container.SetViewMode(515)")#media info3
      return

######################################################## DOWNLOAD ###############################################

#method1
def fazerdownload(name,url,subtitles=None):

      
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','')
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      if os.path.exists(downloadPath):
            videopath = os.path.join(downloadPath,vidname+'.mp4')
            subspath = os.path.join(downloadPath,vidname+'.srt')
            print subtitles
            if os.path.isfile(videopath) is True:
                  ok = mensagemok(traducao(40123),traducao(40124),'','')
                  return False
            else:
                  import downloader
                  downloader.download(url, videopath, 'wareztuga.tv')
                  if subtitles!=None and selfAddon.getSetting('download-subs'):
                        fazerdownload2(name,subtitles)

      else:
            ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
            selfAddon.openSettings()
            return False
            
#method2
def fazerdownload2(name,url):
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','')
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      if os.path.exists(downloadPath):
            if re.search('subs/',url): vidname = vidname+'.srt'
            else: vidname = vidname+'.mp4'
            mypath=os.path.join(downloadPath,vidname)
      else: mypath= '0'           
      if mypath == '0':
            ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
            selfAddon.openSettings()
            return False
      else:
            if os.path.isfile(mypath) is True and not re.search('subs/',url):
                  ok = mensagemok(traducao(40123),traducao(40124),'','')
                  return False
            elif os.path.isfile(mypath) is True and re.search('subs/',url): return False
            else:              
                  try:
                        dp = xbmcgui.DialogProgress()
                        dp.create(traducao(40127), '', name)
                        import time
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
                  except: ok=mensagemok(traducao(40123),traducao(40134)); print 'download failed'; return False

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
            #e = traducao(40128) + ' (%.0f Kb/s) ' % kbps_speed
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = traducao(40129) + ' %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
            #if percent=xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+ mbs + e + ",'500000',"+iconpequeno+")")
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

def activardownloads(accao):
      if accao==1:
            selfAddon.setSetting(id='download-activate', value='true')
            xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+ traducao(40140) + ",'500000',"+iconpequeno.encode('utf-8')+")")
      else:
            selfAddon.setSetting(id='download-activate', value='false')
            xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+ traducao(40141) + ",'500000',"+iconpequeno.encode('utf-8')+")")
    
def activarencerrar(accao):
      if accao==1:
            selfAddon.setSetting(id='encerrarautomatico', value='true')
            xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+ traducao(40210) + ",'500000',"+iconpequeno.encode('utf-8')+")")
      else:
            selfAddon.setSetting(id='encerrarautomatico', value='false')
            xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+ traducao(40211) + ",'500000',"+iconpequeno.encode('utf-8')+")")


######################################################## OUTRAS FUNCOES ###############################################

def encerrarsistema():
      encerraractivo=selfAddon.getSetting('encerrarautomatico')
      if encerraractivo=='true':
            resultado = handle_wait(30,"wareztuga.tv",traducao(40212))
            if resultado==True:
                  selfAddon.setSetting(id='encerrarautomatico', value='false')
                  try:
                        xbmc.executebuiltin("XBMC.Powerdown")
                        print "A encerrar todo o sistema"
                  except:
                        xbmc.executebuiltin("XBMC.Quit")
                        print "A fechar o XBMC"
                  return True
            else: return False
      else: return False

def sobrecarregado():
      ok = mensagemok(traducao(40001),traducao(40002))
      return

def savefile(caminho,filename, contents):
    try:
        destination = os.path.join(caminho, filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename

def openfile(filename,pastaficheiro=pastaperfil):
    try:
        destination = os.path.join(pastaficheiro, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % filename
        return None

def interrompidos():
      ref=0
      lista=os.listdir(pastaperfil)
      for info in lista:
            if re.search('info',info) or re.search('settings',info) or re.search('cookie',info): pass
            else:
                  ref=1
                  try:
                        ficheiros=openfile(info + '_info')
                        umapenas=re.compile('(.+?)-T-(.+?)-T-(.+?)-').findall(ficheiros)[0]
                        addInterrompido(umapenas[0],umapenas[2],5,umapenas[1],info,len(lista),False)
                  except: pass
      if (ref==0): addLink('[B][COLOR white]' + traducao(40176) + '[/COLOR][/B]','','')
      
def xbmcJsonRequest(params):
	import json
	data = json.dumps(params)
	request = xbmc.executeJSONRPC(data)
	response = json.loads(request)
	try:
		if 'result' in response: return response['result']
		return None
	except KeyError:
		Debug("[%s] %s" % (params['method'], response['error']['message']), True)
		return None            

def paginas(url,link,tipo):
      try:
            if tipo=='movies': modo=3
            elif tipo=='series': modo=4
            elif tipo=='animes': modo=4
            pagina=re.compile("""<a .+?actual.+?>.+?<a href="javascript: moviesList.+?pagination.ajax.php.+?p=(.+?)&(.+?)&mediaType.+?'.+?onclick.+?>""").findall(link)[0]
            addDir('[COLOR blue]' + traducao(40042) + pagina[0] + ' >>>[/COLOR]',MainURL + "pagination.ajax.php?p=" + pagina[0] + '&' + pagina[1] + '&mediaType=' + tipo,modo,wtpath + art + 'seta.png',1,True)
      except: pass

def format_time(seconds):
	minutes,seconds = divmod(seconds, 60)
	if minutes > 60:
		hours,minutes = divmod(minutes, 60)
		return "%02d:%02d:%02d" % (hours, minutes, seconds)
	else: return "%02d:%02d" % (minutes, seconds)

def pesquisa(url):
      if re.search('newepisodes',url): pass            
      keyb = xbmc.Keyboard(selfAddon.getSetting('ultima-pesquisa'), traducao(40152))
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote(search)
            selfAddon.setSetting('ultima-pesquisa', search)
            if re.search('newepisodes',url):
                  novosepisodios(encode,'ok')
                  return
            infofil=filmes_request(MainURL + 'pagination.ajax.php?p=1&order=date&words=' + encode + '&mediaType=movies',True)
            if infofil>0: addLink("",'',wtpath + art + 'nothingx.png')
            infoser=series_request(MainURL + 'pagination.ajax.php?p=1&order=date&words=' + encode + '&mediaType=series',True)
            if infoser>0: addLink("",'',wtpath + art + 'nothingx.png')
            series_request(MainURL + 'pagination.ajax.php?p=1&order=date&words=' + encode + '&mediaType=animes',True)
      else: sys.exit(0)
            

def novosepisodios(serie,tipo):
      try:
            link=abrir_url('http://services.tvrage.com/tools/quickinfo.php?show=' + serie)
            link=link.replace('@',' - ').replace('^',' - ')
            if re.search('No Show Results Were Found For ',link): ok= mensagemok('wareztuga.tv',traducao(40156) + serie + '.')
            else:
                  ano=re.compile('Premiered - (.+?)\n').findall(link)[0]
                  nomeserie=re.compile("Show Name - (.+?)\n").findall(link)[0]
                  ultimoep=re.compile("Latest Episode - (.+?)x(.+?) - (.+?) - (.+?)\n").findall(link)[0]
                  try:
                        proximoep=re.compile("Next Episode - (.+?)x(.+?) - (.+?) - (.+?)\n").findall(link)[0]
                        proximoep='S' + proximoep[0] + 'E' + proximoep[1] + ' - ' + proximoep[3] + ' - ' + proximoep[2]
                  except: proximoep=traducao(40157)
                  if tipo=='ok':
                        ok= mensagemok('wareztuga.tv',
                                       '[B]'+traducao(40143)+':[/B] ' + nomeserie + ' (' + ano + ')',
                                       '[B]'+traducao(40154)+':[/B] S' + ultimoep[0] + 'E' + ultimoep[1] + ' - ' + ultimoep[3] + ' - ' + ultimoep[2],
                                       '[B]'+traducao(40155)+':[/B] ' + proximoep)
                  else:
                        if proximoep==traducao(40157): pass
                        else: addDir('[B]' + traducao(40222)+ '[/B] ' + proximoep,MainURL,69,wtpath + art + 'series_em_exibicao.png',1,False)
      except: pass

def abrir_url(url):
      #print "A fazer request de: " + url
      try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            return link
      except urllib2.HTTPError, e:
            mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      except socket.timeout as e:
            mensagemok('wareztuga.tv','Timeout da página.','Tente novamente.')
            sys.exit(0)

def abrir_url_cookie(url):
      #print "A fazer request com cookie de: " + url
      from t0mm0.common.net import Net
      net=Net()
      net.set_cookies(cookie_wt)
      try:
            referencia= {'User-Agent':user_agent}
            link=net.http_GET(url,referencia).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      except socket.timeout as e:
            mensagemok('wareztuga.tv','Timeout da página.','Tente novamente.')
            sys.exit(0)
           
def accaonosite(tipo,warezid,metodo):
      url=MainURL + 'fave.ajax.php?mediaType=' + tipo + '&mediaID=' + warezid + '&action=' + metodo
      abrir_url_cookie(url)
      xbmc.executebuiltin("XBMC.Notification(wareztuga.tv," + traducao(40116) + ",'10000',"+iconpequeno.encode('utf-8')+")")
      xbmc.executebuiltin("XBMC.Container.Refresh")

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40220),MainURL,28,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40221),MainURL,20,wtpath + art + 'defs.png',1,True)
      
def advancedxml(url):
      print '###### INTRODUZIR ADVANCEDXML  ######'
      try:
            advname='advancedsettings.xml'
            dbxmlpath='http://fightnight-xbmc.googlecode.com/svn/advsettings'
            path = xbmc.translatePath(os.path.join('special://home/userdata'.decode('utf-8'),''.decode('utf-8')))
            advance=os.path.join(path.decode('utf-8'), advname.decode('utf-8'))
            try:
                  os.remove(advance)
                  print '========= REMOVING    '+str(advance.encode('utf-8'))+'    ====================================='
            except: pass
            advxmlurl=selfAddon.getSetting('advancedsettings-buffer')
            if advxmlurl == '0':  linkdoxml=dbxmlpath + '/adv0/' + advname
            elif advxmlurl == '1': linkdoxml=dbxmlpath + '/adv5/' + advname
            elif advxmlurl == '2': linkdoxml=dbxmlpath + '/adv10/' + advname
            elif advxmlurl == '3': linkdoxml=dbxmlpath + '/adv20/' + advname
            elif advxmlurl == '4': linkdoxml=dbxmlpath + '/adv30/' + advname
            link=abrir_url(linkdoxml)
            a = open(advance,"w") 
            a.write(link)
            a.close()
            print '========= WRITING NEW    '+str(advance.encode('utf-8'))+'    =========================='
      except: print '######Erro ao introduzir advancedsettings. Ignorou. ######'

def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/wareztuga/plugin.video.wt/addon.xml')
            match=re.compile('name="wareztuga.tv"\r\n       version="(.+?)"\r\n       provider-name="wareztuga">').findall(link)[0]
      except:
            ok = mensagemok('wareztuga.tv',traducao(40184),traducao(40185),'')
            match=traducao(40186)
      return match

def handle_wait(time_to_wait,title,text,segunda=''):
      ret = mensagemprogresso.create(' '+title)
      secs=0
      percent=0
      cancelled = False
      while secs < time_to_wait:
            secs = secs + 1
            percent = (secs*100)/time_to_wait
            secs_left = str((time_to_wait - secs))
            if segunda=='': remaining_display = traducao(40003)+secs_left+traducao(40004)
            else: remaining_display=segunda
            mensagemprogresso.update(percent,text,remaining_display)
            xbmc.sleep(1000)
            if (mensagemprogresso.iscanceled()):
                  cancelled = True
                  break
      if cancelled == True: return False
      else: return True

def legendas(url):
      url=url.replace(' ','')
      link=abrir_url_cookie(url + '&url=http')
      try:match=MainURL + 'subs/' + re.compile('file: "./subs/(.+?)",').findall(link)[0]
      except:
            try:match= MainURL + re.compile('captionUrl: \'./(.+?)\'').findall(link)[0]
            except:match=''
      return match

def redirect(url):
      try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent)
            response = urllib2.urlopen(req)
            gurl=response.geturl()
            return gurl
      except urllib2.HTTPError, e:
            mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)

def millis():
      import time as time_
      return int(round(time_.time() * 1000))

def load_json(data):
      def to_utf8(dct):
            rdct = {}
            for k, v in dct.items() :
                  if isinstance(v, (str, unicode)): rdct[k] = v.encode('utf8', 'ignore')
                  else: rdct[k] = v
            return rdct
      try :        
            from lib import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
      except:
            try:
                  import json
                  json_data = json.loads(data, object_hook=to_utf8)
                  return json_data
            except:
                  import sys
                  for line in sys.exc_info(): print "%s" % line
      return None

class JsUnpacker:

    def unpackAll(self, data):
        sPattern = '(eval\(function\(p,a,c,k,e,d\)\{while.*?)\s*</script>'
        return re.sub(sPattern, lambda match: self.unpack(match.group(1)), data)
    
    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data
        
    def unpack(self, sJavascript):
        aSplit = sJavascript.split(";',")
        p = str(aSplit[0])
        aSplit = aSplit[1].split(",")
        a = int(aSplit[0])
        c = int(aSplit[1])
        k = aSplit[2].split(".")[0].replace("'", '').split('|')
        e = ''
        d = ''
        sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        return sUnpacked.replace('\\', '')
    
    def __unpack(self, p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(self.__itoa(c, a)) +'\\b', k[c], p)
        return p
    
    def __itoa(self, num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

class JsUnpackerV2:

    def unpackAll(self, data):
        try:
            in_data=data
            sPattern = '(eval\\(function\\(p,a,c,k,e,d.*)'
            enc_data=re.compile(sPattern).findall(in_data)
            #print 'enc_data',enc_data, len(enc_data)
            if len(enc_data)==0:
                sPattern = '(eval\\(function\\(p,a,c,k,e,r.*)'
                enc_data=re.compile(sPattern).findall(in_data)
                #print 'enc_data packer...',enc_data

            for enc_val in enc_data:
                unpack_val=self.unpack(enc_val)
                in_data=in_data.replace(enc_val,unpack_val)
            return in_data
        except: 
            traceback.print_exc(file=sys.stdout)
            return data
        
        
    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data or 'p,a,c,k,e,r' in data
        
    def unpack(self,sJavascript,iteration=1, totaliterations=1  ):

        aSplit = sJavascript.split("rn p}('")

        p1,a1,c1,k1=('','0','0','')
        ss="p1,a1,c1,k1=(\'"+aSplit[1].split(".spli")[0]+')' 
        exec(ss)
        
        k1=k1.split('|')
        aSplit = aSplit[1].split("))'")
        e = ''
        d = ''#32823
        sUnpacked1 = str(self.__unpack(p1, a1, c1, k1, e, d,iteration))
        if iteration>=totaliterations:
            return sUnpacked1
        else:
            return self.unpack(sUnpacked1,iteration+1)

    def __unpack(self,p, a, c, k, e, d, iteration,v=1):
        while (c >= 1):
            c = c -1
            if (k[c]):
                aa=str(self.__itoaNew(c, a))
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
        return p

    def __itoa(self,num, radix):

        result = ""
        if num==0: return '0'
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result
        
    def __itoaNew(self,cc, a):
        aa="" if cc < a else self.__itoaNew(int(cc / a),a) 
        cc = (cc % a)
        bb=chr(cc + 29) if cc> 35 else str(self.__itoa(cc,36))
        return aa+bb


def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','\xC0':'À','\xC1':'Á','\xC2':'Â','\xC3':'Ã','\xC7':'Ç','\xC8':'È','\xC9':'É','\xCA':'Ê','\xCC':'Ì','\xCD':'Í','\xCE':'Î','\xD2':'Ò','\xD3':'Ó','\xD4':'Ô','\xDA':'Ú','\xDB':'Û','\xE0':'à','\xE1':'á','\xE2':'â','\xE3':'ã','\xE7':'ç','\xE8':'è','\xE9':'é','\xEA':'ê','\xEC':'ì','\xED':'í','\xEE':'î','\xF3':'ó','\xF5':'õ','\xFA':'ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

def NinekwBalance(apikey,apiurl):
	url="?action=usercaptchaguthaben&source=pythonapi&apikey=" + apikey
	req = urllib2.Request(apiurl+url)
	response = urllib2.urlopen(req).read()
	return response

def Ninekwusercaptchaupload(apikey, apiurl, filename):
	from base64 import b64encode
	png_data = open(filename, "rb")	
	data = png_data.read();	
	query_args = {'action':'usercaptchaupload', 'source':'pythonapi', 'apikey':apikey, 'base64':'1', 'file-upload-01':b64encode(data) }
	data = urllib.urlencode(query_args)
	req = urllib2.Request(apiurl,data)
	response = urllib2.urlopen(req).read()
	return response

def Ninekwusercaptchacorrectdata(apikey, apiurl, id):
	url="?action=usercaptchacorrectdata&source=pythonapi&apikey=" + apikey + "&id=" + id
	req = urllib2.Request(apiurl+url)
	response = urllib2.urlopen(req)
	solved=response.read()
	if solved == "":
			wait = 5000;
			xbmc.sleep(wait)
			for i in range(wait, 20, 1):
				try:
					req = urllib2.Request(apiurl+url)
					response = urllib2.urlopen(req)
					solved = response.read()
				except: pass
				if(solved != ""): break
				xbmc.sleep(3000)
	return solved

def Ninekwusercaptchacorrectback(id, correct):
	APIKEY = selfAddon.getSetting('API-9kw');
	APIURL = "http://www.9kw.eu/index.cgi"
	url="?action=usercaptchacorrectback&source=pythonapi&apikey=" + APIKEY + "&id=" + id + "&correct=" + correct
	req = urllib2.Request(APIURL+url)
	response = urllib2.urlopen(req)

def solvevia9kw(file):
	APIKEY = selfAddon.getSetting('API-9kw');
	APIURL = "http://www.9kw.eu/index.cgi"
	if APIKEY != "":
			balance = NinekwBalance(APIKEY,APIURL)
			print '[##9ku]balance: '+balance
			if balance >= 10:
				id = Ninekwusercaptchaupload(APIKEY,APIURL,file)
				print '[##9ku]ID: '+id
				if id <> '':
					solved = Ninekwusercaptchacorrectdata(APIKEY,APIURL,id)
					print '[##9ku]solved: '+solved
					return solved,id
				else: return "",""
			else: return "",""
	else: return "",""
            
params=get_params()
url=None
name=None
mode=None
seriefanart=None

#try: selfAddon.setSetting('ultima-pasta',value=name)
#except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: seriefanart=urllib.unquote_plus(params["seriefanart"])
except: seriefanart=False

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao;
      login_wareztuga()
      
elif mode==1: menu_filmes()
elif mode==2: menu_series(url)
elif mode==3: filmes_request(url,pesquisa)
elif mode==4: series_request(url,pesquisa)
elif mode==5:
      dialogselect=selfAddon.getSetting('dialog-select')
      if dialogselect == "0": resolver_servidores(url,name,dialogselect=True)
      elif dialogselect == "1": resolver_servidores(url,name,dialogselect=False)
elif mode==6: seriestemp_request(name,url)
elif mode==7: seriesepis_request(url,name)
elif mode==8: conteudonotificacao(url,name)
elif mode==9:
      if downloadPath=='':
            ok = mensagemok(traducao(40123),traducao(40125),traducao(40135),'')
            selfAddon.openSettings()
      else: xbmc.executebuiltin("ActivateWindow(VideoFiles," + downloadPath.encode('utf-8') + ")")
elif mode==10: notificacoes_request(url)
elif mode==11: menu_categoria(url)
elif mode==12: menu_ano(url)
elif mode==13: ok = mensagemok('wareztuga.tv',traducao(40179),traducao(40180),traducao(40181))
elif mode==14: interrompidos()
elif mode==15: menu_extra()
elif mode==16: pesquisa(url)
elif mode==17: series_exib(url)
elif mode==18: series_exib_escolha(url,name)
elif mode==19: sintomecomsorte()
elif mode==20: selfAddon.openSettings()
elif mode==21: resolver_servidores(url,name,download=True)
elif mode==22: guardaratalhos(name,url)
elif mode==23: atalhos()
elif mode==24: pass #run plugin atalho
elif mode==25: infoproximoepisodio(name,url)
elif mode==26: listas(url)
elif mode==27:
      selfAddon.openSettings()
      ok = mensagemok("wareztuga.tv",traducao(40114),traducao(40115))
      entrarnovamente(0)
      vista_menus()      
elif mode==28: login_wareztuga()
elif mode==29: conteudolistas(url)
elif mode==30: itens_conta(url)
elif mode==31: mensagemaviso('O objectivo das listas é partilhar conteúdos de forma organizada e temática, conforme os gostos de cada um.\n\nCom este espaço podemos descobrir novos titulos de forma simples e directa.\n\nContribuir para este espaço é muito fácil. Visita [B]http://bit.ly/fightnightaddons[/B] para ajudar a contribuir para este espaço. A comunidade agradece.')
elif mode==32: glib('umfilme',url)
elif mode==33: glib('sacarbd',url)
elif mode==34: pedidos_request(url)
elif mode==35: glib('subs',url)
elif mode==36: menu_conta()
elif mode==37: instrucoeslibrary()
elif mode==38: glib('subs',url,silent=True)
elif mode==39: multifiltro()
elif mode==40: instrucoes9kw()
elif mode==69: pass



xbmcplugin.endOfDirectory(int(sys.argv[1]))
