# -*- coding: utf-8 -*-

""" OKGoals
    2014 fightnight
"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,os,re,sys, urllib, urllib2

####################################################### CONSTANTES #####################################################

versao = '0.2.02'
addon_id = 'plugin.video.tvgolo'
vazio= []
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
selfAddon = xbmcaddon.Addon(id=addon_id)
traducao= selfAddon.getLocalizedString
tvgolopath = selfAddon.getAddonInfo('path')
menuescolha = xbmcgui.Dialog().select
mensagemok = xbmcgui.Dialog().ok
MainURL = 'http://www.okgoals.com/'

def horalocal(link):
      hora=re.compile('<div class="clock">Local Time: (.+?)</div>').findall(link)[0]
      addLink('[B]'+traducao(40025)+'[/B]' + hora,MainURL,'')

def menu_principal():
      addDir(traducao(40003),MainURL,2,tvgolopath+art+'ulgolos.png',1,True)
      addDir('Últimos Liga Portuguesa','http://www.goalsoftheworld.tk/goals-in-Portugal.html',10,tvgolopath+art+'liga.png',1,True)
      addDir(traducao(40004),MainURL,3,tvgolopath+art+'ugolosl2.png',1,True)
      addDir(traducao(40005),MainURL,4,tvgolopath+art+'semana.png',1,True)
      addDir(traducao(40007),MainURL + 'seasons-archive.php',5,tvgolopath+art+'epoca.png',1,True)
      addDir(traducao(40010),MainURL,8,tvgolopath+art+'lupa.png',1,True)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def ligaportuguesa(url):
      link=clean(abrir_url(url))
      conteudos= re.compile("""class='linkgoal sapo' id='(.+?)'><h3.+?><img.+?src='.+?'.+?><span.+?>(.+?)</span></h3>""").findall(link)
      from random import randint
      for endereco,titulo in conteudos:
            addDir(titulo,'http://www.goalsoftheworld.tk/getcontent.php?rand=%s&id_results=%s' % (str(randint(1, 100)),endereco),1,tvgolopath+art+'pt.png',len(conteudos),False)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def listadeligas(url):
      link=abrir_url(url)
      link=link.replace('Portuguese</a>','').replace('English</a>','')
      ligas=re.compile("""<li class='active'><a href='(.+?)' class="menulinks">.+?alt="(.+?)" src="http://www.okgoals.com/images/(.+?)"> (.+?)</span>""").findall(link)
      for endereco,liga,thumb,country in ligas: addDir('%s (%s)' % (liga.capitalize().title(),country.capitalize().title()),MainURL + endereco,2,tvgolopath+art+thumb,len(ligas),True)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def semanasanteriores(url):
      link=abrir_url(url)
      anterior=re.compile('<a href="([^"]+?)">previous weeks archive').findall(link)[0]
      anterior=anterior.replace('amp;','')
      request(MainURL + anterior)

def epocasanteriores(url):
	link=abrir_url(url)
	link=link.replace('amp;','')
	anteriores=re.compile('<a href="([^"]+?)">([^"]+?)</a><BR />').findall(link)
	for endereco,titulo in anteriores:
              addDir(titulo,MainURL + endereco,2,'',len(anteriores),True)
	xbmc.executebuiltin("Container.SetViewMode(501)")

def comedyfootball(url):
      link=abrir_url(url)
      ano=re.compile('<li><a href="../(.+?)".+?>(.+?)</a></li>').findall(link)
      for endereco,titulo in ano: addDir(titulo,MainURL + endereco,1,'',len(ano),False)

def programacaotv(url):
      link=abrir_url(url)
      link=link.replace('\\','').replace('/','').replace('x26','&').replace('&agrave;','à')
      link=clean(link)
      tv=re.compile(' x3e(.+?)x3ca').findall(link)
      for titulo in tv: addLink(titulo,MainURL,'')
      
def request(url):
      link=abrir_url(url)
      link=clean(link)
      listagolos=re.compile('<div class="listajogos"><a href="(.+?)"><img.+?src="images/(.+?)\..+?" />    (.+?)</a></div>').findall(link)
      for endereco,thumb,titulo in listagolos: addDir(titulo,MainURL + endereco,1,tvgolopath+art+thumb+'.png',len(listagolos),False)
      if re.search('football.php', url) or re.search('page-start', link): paginas(url,link)
      xbmc.executebuiltin("Container.SetViewMode(51)")


def paginas(url,link):
      try:
            try:enderecopagina=re.compile('</b> <a href="(.+?)">').findall(link)[0]
            except: enderecopagina=re.compile('</b><a href="(.+?)">').findall(link)[0]
            valorpagina=int(re.compile('page-start_from_(.+?)_archive.+?.html').findall(enderecopagina)[0])
            pagina=int((valorpagina/30)+1)
            addDir('[COLOR blue][B]%s %s >[/COLOR][/B]' % (traducao(40014),pagina),MainURL + enderecopagina,2,tvgolopath+art+'proxima.png',1,True)
      except: pass

def captura(name,url):
      link=abrir_url(url)
      linkoriginal = link
      if re.search('okgoals',url):
            goals=True
            link=clean(link)
            #ty tfouto
            link=link.replace('<div style="float:left;"><iframe','').replace('"contentjogos">','"contentjogos"></iframe>')
            ij=link.find('"contentjogos">')
            link=link[ij:]
            #ty tfouto
      else: goals=False
      titles=[]; ligacao=[]
      aliezref=int(0)
      aliez=re.compile('<iframe.+?src="http://emb.aliez.tv/(.+?)"').findall(link)
      if aliez:
            for codigo in aliez:
                  aliezref=int(aliezref + 1)
                  if len(aliez)==1: aliez2=str('')
                  else: aliez2=' #' + str(aliezref)
                  titles.append('Aliez' + aliez2)
                  ligacao.append('http://emb.aliez.tv/' + codigo)
      dailymotionref=int(0)
      dailymotion=re.compile('src="http://www.dailymotion.com/embed/video/(.+?)"',re.DOTALL|re.M).findall(link)
      if not dailymotion: dailymotion = re.compile('src="http://www.dailymotion.com/embed/video/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)
     
      if dailymotion:
            for codigo in dailymotion:
                  golo=findgolo(link,codigo)
                  golo=cleangolo(golo).replace('<','')
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Dailymotion' + golo)
                  ligacao.append('http://www.dailymotion.com/video/' + codigo)
      #fb www.tvgolo.com/match-showfull-1382558391-1304288520--50
      fbvideoref=int(0)
      fbvideo=re.compile('src="http://www.facebook.com/video/embed.+?video_id=(.+?)"',re.DOTALL|re.M).findall(link)
      if fbvideo:
           for codigo in fbvideo:
                 golo=findgolo(link,codigo)
                 golo=cleangolo(golo).replace('<','')
                 if golo: golo=' (%s)' % (golo)
                 titles.append('Facebook' + golo)
                 ligacao.append("http://www.facebook.com/video/embed?video_id=" + codigo)
      #kiwi http://www.tvgolo.com/match-showfull-1382558564-1304288520--50                  
      kiwiref=int(0)
      kiwi=re.compile('src="http://v.kiwi.kz/v2/(.+?)/"',re.DOTALL|re.M).findall(link)
      if kiwi:
            for codigo in kiwi:
                  golo=findgolo(link,codigo)
                  golo=cleangolo(golo).replace('<','')
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Kiwi'+ golo)
                  ligacao.append(codigo)
      #Falta
      longtailref=int(0)
      longtail=re.compile('flashvars=".+?".+?src="http://player.longtailvideo.com/player5.2.swf"').findall(link)
      if longtail:
            for codigo in longtail:
                  longtailref=int(longtailref+1)
                  if len(longtail)==1: longtail2=str('')
                  else: longtail2=' #' + str(longtailref)
                  titles.append('Longtail' + longtail2 + ' (' + traducao(40015) + ')')
                  ligacao.append(0)
      metauaref=int(0)
      metaua=re.compile('src="http://video.meta.ua/players/video/3.2.19k/Player.swf.+?fileID=(.+?)&').findall(link)
      if metaua:
            for codigo in metaua:
                  metauaref=int(metauaref+1)
                  if len(metaua)==1: metaua2=str('')
                  else: metaua2=' #' + str(metauaref)
                  titles.append('Meta.ua' + metaua2 + ' (' + traducao(40015) + ')')
                  ligacao.append(0)
      #http://www.tvgolo.com/match-showfull-1396982174---50
      playwire=re.compile('data-publisher-id="(.+?)" data-video-id="(.+?)"').findall(link)
      if not playwire: playwire=re.compile('http://config.playwire.com/videos/(.+?)/(.+?)/').findall(link)
      if playwire:
          for publisher,codigo in playwire:
                  if publisher=='v2': publisher='configopener'
                  golo=findgolo(link,codigo)
                  golo=cleangolo(golo).replace('<','')
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Playwire' + golo)
                  ligacao.append('http://cdn.playwire.com/v2/%s/config/%s.json' % (publisher,codigo))
            
      playwire_v2=re.compile('http://config.playwire.com/(.+?)/videos/v2/(.+?).json').findall(link)
      if playwire_v2:
          for publisher,codigo in playwire_v2:
                  golo=findgolo(link,codigo)
                  golo=cleangolo(golo).replace('<','')
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Playwire' + golo)
                  ligacao.append('http://config.playwire.com/%s/videos/v2/%s.json' % (publisher,codigo))
                  
      #rutube http://www.tvgolo.com/match-showfull-1376242370---02
      rutuberef=int(0)
      rutube=re.compile('src=".+?rutube.ru/video/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if not rutube: rutube=re.compile('value="http://video.rutube.ru/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)  
      if not rutube: rutube=re.compile('src="http://rutube.ru/video/embed/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)
      if rutube:
            for codigo in rutube:
                  golo=findgolo(link,codigo)
                  golo=cleangolo(golo).replace('<','')
                  if golo: golo=' (%s)' % (golo)
                  titles.append("Rutube" + golo)
                  ligacao.append(codigo)
      saporef=int(0)
      sapo=re.compile('src=".+?videos.sapo.pt/playhtml.+?file=(.+?)/1&"',re.DOTALL|re.M).findall(link)
      if not sapo: sapo=re.compile('src=".+?videos.sapo.pt/playhtml.+?file=(.+?)/1"',re.DOTALL|re.M).findall(link)
      if sapo:
            print sapo
            for endereco in sapo:
                  

                  if goals==True:
                        golo=findgolo(link,endereco)
                        golo=cleangolo(golo).replace('<','')
                        if golo: golo=' (%s)' % (golo)
                  else:
                        saporef=int(saporef + 1)
                        if len(sapo)==1: golo=str('')
                        else: golo=' #' + str(saporef)
                  titles.append('Videos Sapo' + golo)
                  ligacao.append(endereco)
      videaref=int(0)
      videa=re.compile('src="http://videa.hu/(.+?)"',re.DOTALL|re.M).findall(link)
      if videa:
            for codigo in videa:
                  golo=findgolo(link,codigo)
                  golo=cleangolo(golo).replace('<','')
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Videa' + golo)
                  ligacao.append('http://videa.hu/' + codigo)
      #http://www.tvgolo.com/match-showfull-1376242370---02
      vkref=int(0)
      vk=re.compile('src="http://vk.com/(.+?)"',re.DOTALL|re.M).findall(link)
      if vk:
          for codigo in vk:
                golo=findgolo(link,codigo)
                golo=cleangolo(golo).replace('<','')
                if golo: golo=' (%s)' % (golo)
                titles.append('VK' + golo)
                ligacao.append('http://vk.com/' + codigo)
      youtuberef=int(0)
      youtube=re.compile('src="http://www.youtube.com/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if not youtube: youtube=re.compile('src="//www.youtube.com/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if youtube:
        for codigo in youtube:     
              golo=findgolo(link,codigo)
              golo=cleangolo(golo).replace('<','')
              if golo: golo=' (%s)' % (golo)
              titles.append('Youtube' + golo)
              ligacao.append(codigo)
      if len(ligacao)==1: index=0
      elif len(ligacao)==0: ok=mensagemok(traducao(40000), traducao(40016)); return     
      else:
            #titles.append('');titles.append('[COLOR blue][B]'+traducao(40017)+'[/B][/COLOR]');ligacao.append(0);ligacao.append(0)
            index = menuescolha(traducao(40018), titles)
      if index > -1:
             linkescolha=ligacao[index]
             servidor=titles[index]
             if linkescolha:
                   if re.search('Rutube',servidor):
                         link=abrir_url('http://rutube.ru/api/play/options/' + linkescolha)
                         try:streamurl=re.compile('"m3u8": "(.+?)"').findall(link)[0]
                         except:streamurl=re.compile('"default": "(.+?)"').findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Aliez',servidor):
                         linkescolha=linkescolha.replace('amp;','')
                         link=abrir_url(linkescolha)
                         streamurl=re.compile("file.+?'(.+?)'").findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Playwire',servidor):
                         if re.search('configopener',linkescolha):
                               videoid=''.join(linkescolha.split('/')[-1:]).replace('.json','')
                               streamurl=redirect('http://config.playwire.com/videos/v2/%s/player.json'%videoid).replace('player.json','manifest.f4m')
                         else:
                               link=abrir_url(linkescolha)
                               try:streamurl=re.compile('"src":"(.+?)"').findall(link)[0]
                               except:streamurl=re.compile('"f4m":"(.+?)"').findall(link)[0]
                         if re.search('.f4m',streamurl):
                               titles=[]
                               ligacao=[]
                               f4m=abrir_url(streamurl)
                               baseurl=re.compile('<baseURL>(.+?)</baseURL>').findall(f4m)[0]
                               videos=re.compile('url="(.+?)".+?height="(.+?)"').findall(f4m)
                               for urlname,quality in videos:
                                     titles.append(quality + 'p')
                                     ligacao.append(urlname)
                               if len(ligacao)==1:index=0
                               else: index = menuescolha("Qualidade", titles)
                               if index > -1: streamurl='%s/%s' % (baseurl,ligacao[index])
                               else: return
                         streamurl=streamurl.replace('rtmp://streaming.playwire.com/','http://cdn.playwire.com/').replace('mp4:','')
                         comecarvideo(name,streamurl)
                   elif re.search('VK',servidor):
                         linkescolha=linkescolha.replace('amp;','')
                         link=abrir_url(linkescolha)
                         link=link.replace('\\','')
                         if re.search('No videos found.',link): ok=mensagemok("OKGoals",'Video not found')
                         else:
                               titles=[]
                               ligacao=[]
                               try:
                                     streamurl=re.compile('"url1080":"(.+?)"').findall(link)[0]
                                     titles.append("1080p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url720":"(.+?)"').findall(link)[0]
                                     titles.append("720p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url480":"(.+?)"').findall(link)[0]
                                     titles.append("480p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url360":"(.+?)"').findall(link)[0]
                                     titles.append("360p")
                                     ligacao.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url240":"(.+?)"').findall(link)[0]
                                     titles.append("240p")
                                     ligacao.append(streamurl)
                               except: pass
                               if len(ligacao)==1:index=0
                               else: index = menuescolha("Qualidade", titles)
                               if index > -1:
                                     linkescolha=ligacao[index]
                                     comecarvideo(name,linkescolha)
                   elif re.search('Sapo',servidor): comecarvideo(name,linkescolha)
                   elif re.search('Facebook',servidor):
                         link=abrir_url(linkescolha)
                         params = re.compile('"params","([\w\%\-\.\\\]+)').findall(link)[0]
                         html = urllib.unquote(params.replace('\u0025', '%')).decode('utf-8')
                         html = html.replace('\\', '')
                         streamurl = re.compile('(?:hd_src|sd_src)\":\"([\w\-\.\_\/\&\=\:\?]+)').findall(html)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Kiwi',servidor):
                         link=urllib.unquote(abrir_url('http://v.kiwi.kz/v2/'+linkescolha))
                         streamurl=re.compile('&url=(.+?)&poster').findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('videa',linkescolha):
                         referencia=re.compile('flvplayer.swf.+?v=(.+?)"').findall(linkescolha)[0]
                         link=abrir_url('http://videa.hu/flvplayer_get_video_xml.php?v='+ referencia)
                         streamurl=re.compile('<version quality="standard" video_url="(.+?)"').findall(link)[0]
                         comecarvideo(name,streamurl)
                   elif re.search('Youtube',servidor):
                         streamurl='plugin://plugin.video.youtube/?action=play_video&videoid='+codigo
                         comecarvideo(name,streamurl)
                         
                   elif re.search('dailymotion',linkescolha):
                         import urlresolver
                         sources=[]
                         hosted_media = urlresolver.HostedMediaFile(url=linkescolha)
                         sources.append(hosted_media)
                         source = urlresolver.choose_source(sources)
                         if source:
                                     linkescolha=source.resolve()
                                     if linkescolha==False:
                                           okcheck = xbmcgui.Dialog().ok
                                           okcheck(traducao(40000),traducao(40019))
                                           return
                                     else: comecarvideo(name,linkescolha)

def comecarvideo(titulo,url):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(titulo, iconImage="DefaultVideo.png", thumbnailImage=thumb)
      listitem.setInfo("Video", {"Title":titulo})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      playlist.add(url, listitem)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', os.path.join(tvgolopath,'fanart.jpg'))
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
      return ok

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', os.path.join(tvgolopath,'fanart.jpg'))
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
      return ok

def pesquisa():
      keyb = xbmc.Keyboard('', traducao(40020))
      keyb.doModal()
      if (keyb.isConfirmed()):
            mensagemok(traducao(40000),traducao(40021),'Não inclui liga PT.')
            search = keyb.getText()
            encode=urllib.quote(search)
            if encode=='': pass
            else:
                  link=abrir_url( MainURL + 'search.php?dosearch=yes&search_in_archives=yes&title=' + encode)
                  #horalocal(link)
                  jogos=re.compile('<div style="font-family:Arial, Helvetica, sans-serif; font-size:12px;"><a href="/(.+?)">(.+?)</a></div>').findall(link)
                  for endereco,titulo in jogos: addDir(titulo,MainURL + endereco,1,'',len(jogos),False)
                        
def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

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
            if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&atilde;':'ã','&ordf;':'ª','&eacute;':'é','&ccedil;':'ç','&oacute;':'ó','&acirc;':'â','&ntilde;':'ñ','&aacute;':'á','&iacute;':'í'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

def cleangolo(text):
      text=text.replace('\n', '').replace('<br />', '').replace('<br>', '').replace('/>', '').replace('<hr ', '').replace('<hr>', '').replace('</span>', '').replace('</iframe>','').replace('</script>','').replace('</a>','')
      return text

def findgolo(link, codigo):
      posicao=link.find(codigo)
      text=link[:posicao]
      begin1=text.rfind('</iframe>')
      begin2=text.rfind('</script>')
      begin3=text.rfind('</a>')
      end1=text.rfind('<iframe')
      end2=text.rfind('<script')
      end3=text.rfind('<a href="')
      trueBegin=max([begin1,begin2,begin3])
      trueEnd=max([end1,end2])
      golo=text[trueBegin:trueEnd]
      return golo

params=get_params()
url=None
name=None
mode=None
thumb=None
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: thumb=urllib.unquote_plus(params["thumb"])
except: pass

if mode==None or url==None or len(url)<1: print "Versao Instalada: v" + versao; menu_principal()
elif mode==1: captura(name,url)
elif mode==2: request(url)
elif mode==3: listadeligas(url)
elif mode==4: semanasanteriores(url)
elif mode==5: epocasanteriores(url)
elif mode==6: comedyfootball(url)
elif mode==7: ok = mensagemok(traducao(40000),traducao(40022),traducao(40023),traducao(40024))
elif mode==8: pesquisa()
elif mode==9: programacaotv(url)
elif mode==10: ligaportuguesa(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
