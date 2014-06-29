# -*- coding: utf-8 -*-

""" Fightnight Music
    2014 fightnight
"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,datetime,time,re,sys, urllib, urllib2,os

####################################################### CONSTANTES #####################################################

versao = '0.0.05'
addon_id = 'plugin.audio.fightnightmusic'
NoiseTradeURL = 'http://www.noisetrade.com/'
OptimusDiscosURL = 'http://optimusdiscos.pt/'
OptimusAlbumlistURL = 'player/albums.json'
OptimusTracklistURL = 'player/playlist/track.json'
RadiosURL = 'http://www.radios.pt/portalradio/'
RadiosNacionaisURL = 'http://www.radioonline.com.pt'
vazio= []
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
selfAddon = xbmcaddon.Addon(id=addon_id)
optimuspath = selfAddon.getAddonInfo('path')
menuescolha = xbmcgui.Dialog().select
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
downloadPath = selfAddon.getSetting('download-folder')
traducao= selfAddon.getLocalizedString
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
pastadeaddons = os.path.join(xbmc.translatePath('special://home/addons'), '')
PATH = "XBMC_NOISE"
UATRACK="UA-41082698-1"

if selfAddon.getSetting('ga_visitor')=='':
    from random import randint
    selfAddon.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))

def menu_principal():
    GA("None","menuprincipal")
    addDir('[COLOR blue][B]Radios Locais[/B][/COLOR]',NoiseTradeURL,11,"%s/resources/art/musical.png"%selfAddon.getAddonInfo("path"),1,True)
    addDir('[COLOR orange][B]NoiseTrade[/B][/COLOR]',NoiseTradeURL,9,"%s/resources/art/noisetrade.png"%selfAddon.getAddonInfo("path"),1,True)
    addDir('[COLOR orange][B]Optimus[/COLOR] [COLOR white]Discos[/B][/COLOR]',NoiseTradeURL,10,"%s/resources/art/optimusdiscos.png"%selfAddon.getAddonInfo("path"),1,True)
    addLink('','','')
    radiosnacionais(name,RadiosNacionaisURL)    
    disponivel=versao_disponivel()
    if disponivel==versao: addLink(traducao(40004)+' (' + versao+ ')','',"%s/resources/art/versao_inst.png"%selfAddon.getAddonInfo("path"))
    else: addDir(traducao(40005) + versao + traducao(40006) + disponivel,NoiseTradeURL,2,"%s/resources/art/versao_inst.png"%selfAddon.getAddonInfo("path"),1,False)
    #xbmc.executebuiltin("Container.SetViewMode(500)")

############# RADIO #########################

def radio():
    link=abrir_url(RadiosURL)
    link=clean(link)
    #addDir('[COLOR blue][B]Ouvir Radios Nacionais[/B][/COLOR]',RadiosNacionaisURL,17,'',1,True)
    #addLink("",'','')
    addDir('Pesquisar (exclui nacionais)',RadiosURL + '?distrito=0&concelho=0&tipo=0&text=',16,'',1,True)
    distritos=re.compile('id="DirectorioPesquisa1_ddlDistritos">(.+?)</select>').findall(link)[0]
    distritos=distritos.replace('<option value="0"></option>','<option value="0">Todos (exclui nacionais)</option>')
    lista=re.compile('<option value="(.+?)">(.+?)</option>').findall(distritos)
    for iddistrito,nomedistrito in lista:
        addDir(nomedistrito,RadiosURL + '?distrito=' + iddistrito,12,'',len(lista),True)
    xbmc.executebuiltin("Container.SetViewMode(501)")

def radiosnacionais(name,url):
    link=abrir_url(url)
    link=clean(link)    
    nacionais=re.compile('<div class="radiostation boxgrid">(.+?)</div>').findall(link)
    for radioindividual in nacionais:
        radiosnacionais=re.compile('<a href="http://www.radioonline.com.pt/#(.+?)".+?<img.+?src="(.+?)".+?alt="(.+?)"').findall(radioindividual)
        for idradio,imagemradio,nomeradio in radiosnacionais:
            addDir(nomeradio,idradio,15,imagemradio,len(nacionais),False)

def pesquisa_radio(name,url):
    keyb = xbmc.Keyboard('', 'Fightnight Music')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        encode=urllib.quote(search)
        if encode=='': pass
        else: listar_radios(name,url + encode)


def radio_concelhos(name,url):
    link=abrir_url(url)
    link=clean(link)
    concelhos=re.compile('id="DirectorioPesquisa1_ddlConcelhos">(.+?)</select>').findall(link)[0]
    concelhos=concelhos.replace('<option selected="selected" value="0"></option>','<option value="0">Todos</option>')
    lista=re.compile('<option value="(.+?)">(.+?)</option>').findall(concelhos)
    for idconcelho,nomeconcelho in lista:
        urlfinal=url + '&concelho=' + idconcelho
        if len(lista)==1:listar_radios(nomeconcelho,urlfinal)
        else: addDir(nomeconcelho,urlfinal + '&tipo=0',14,'',len(lista),True)
    xbmc.executebuiltin("Container.SetViewMode(501)")


def tipo_radio(name,url):
    link=abrir_url(url)
    link=clean(link)
    tiporadio=re.compile('id="DirectorioPesquisa1_ddlTipoRadio">(.+?)</select>').findall(link)[0]
    tiporadio=tiporadio.replace('<option selected="selected" value="0"></option>','<option value="0">Todos</option>')
    lista=re.compile('<option value="(.+?)">(.+?)</option>').findall(tiporadio)
    for idtipo,tiporadio in lista:
        addDir(tiporadio,url + '&tipo=' + idtipo,14,'',len(lista),True)
    xbmc.executebuiltin("Container.SetViewMode(501)")

def listar_radios(name,url):
    link=abrir_url(url)
    link=clean(link)
    radios=re.compile('<td><a href="/portalradio/conteudos/ficha/.+?radio_id=(.+?)">(.+?)</a></td><td>(.+?)</td>.+?<td align="center">').findall(link)
    for idradio,nomeradio,concelho in radios:
        addDir('[B]'+nomeradio+'[/B] ('+concelho+')',RadiosURL + 'Sintonizador/?radio_id=' + idradio + '&scope=0',15,'http://www.radio.com.pt/APR.ROLI.WEB/Images/Logos/'+ idradio +'.gif',len(radios),False)
    xbmc.executebuiltin("Container.SetViewMode(501)")
    paginasradios(url,link)

def obterurlstream(name,url):
    GA("None",name)
    mensagemprogresso.create('Fightnight Music','A carregar')
    mensagemprogresso.update(0)
    if re.search('www.radios.pt',url):
        link=abrir_url(url)
        try:
            endereco=re.compile('<param name="url" value="(.+?)"').findall(link)[0]
        except:
            xbmc.executebuiltin("XBMC.Notification(Fightnight Music,Não é possível ouvir esta rádio.,'500000',)")
            return
        idradio=url.replace('http://www.radios.pt/portalradio/Sintonizador/?radio_id=','').replace('&scope=0','')
        thumbnail='http://www.radio.com.pt/APR.ROLI.WEB/Images/Logos/'+ idradio +'.gif'
    else:
        #link=abrir_url('http://www.radioonline.com.pt/ajax/get_station_id.php?clear_s_name='+url)
        #conteudo=re.compile('"sid":"(.+?)","stype":"(.+?)","path":".+?","as":"(.+?)","pt":"(.+?)"').findall(link)[0]
        #streamtype=conteudo[1]
        #streamtype=streamtype.replace('wma','wmp')
        #urlfinal='http://www.radioonline.com.pt/ajax/player.php?sid=' + conteudo[0] + '&type=' + streamtype + '&as=' + conteudo[2] + '&ptype=' + conteudo[3]
        urlfinal='http://www.radioonline.com.pt/ajax/player.php?clear_s_name=' + url
        link=clean(abrir_url(urlfinal))
        try: player=re.compile('soundManager.createSound\({(.+?)autoLoad').findall(link)[0]
        except: player=False
        try:
            endereco=re.compile('url: "(.+?)"').findall(player)[0].replace(';','')
            if re.search('serverURL',player):
                rtmp=re.compile('serverURL: "(.+?)"').findall(player)[0]
                endereco=rtmp + ' playPath=' + endereco
        except:endereco=False
        if not endereco:
            try:endereco=re.compile('<param name="URL" value="(.+?)"').findall(link)[0]
            except: endereco=False

        if not endereco:
            xbmc.executebuiltin("XBMC.Notification(Fightnight Music,Não é possível ouvir esta rádio.,'500000',)")
            mensagemprogresso.close()
            return
        
        try:thumbnail=re.compile('<img id="station-logo-player" src="(.+?)"').findall(link)[0]
        except: thumbnail=''
        if re.search('.asx',endereco):
            nomeasx='stream.asx'
            path = xbmc.translatePath(os.path.join(pastaperfil))
            lib=os.path.join(path, nomeasx)
            downloader(endereco,lib)
            texto=openfile(nomeasx)
            endereco = xbmc.PlayList(1)
            endereco.clear()
            streams=re.compile('<ref.+?"(.+?)"/>').findall(texto)
            for musica in streams:
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
                listitem.setInfo("music", {"Title":name})
                endereco.add(musica,listitem)
        else: pass
    mensagemprogresso.close()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    listitem.setInfo("music", {"Title":name})
    xbmc.Player().play(endereco,listitem)
               
def paginasradios(url,link):
    try:
        pagina=re.compile('<div id="DirectorioPesquisa1_divPageSelector">.+?<b> (.+?)</b>  <a href=/portalradio/(.+?)>').findall(link)[0]
        nrpag=int(pagina[0])+1
        nrpag=str(nrpag)
        addDir('[COLOR blue]Próxima página (' + nrpag + ') >>>[/COLOR]',RadiosURL + pagina[1],14,'',1,True)
    except: pass


############# NOISETRADE ####################

def noisetrade_menu():
    addDir(traducao(40000),NoiseTradeURL,1,'',1,True)
    addDir(traducao(40001),NoiseTradeURL + 'searchall?s=popular',6,'',1,True)
    addDir(traducao(40002),NoiseTradeURL + 'searchall?s=newest',6,'',1,True)
    #addDir(traducao(40003),NoiseTradeURL,5,'',1,True)

def novosenotaveis(name,url):
    link=abrir_url(NoiseTradeURL)
    link=clean(link)
    notaveis=re.compile('<div class="spacer_5">(.+?)<div class="spacer_20">').findall(link)[0]
    print notaveis
    apanharalbuns(name,url,notaveis)

def apanharalbuns(name,url,link):
    if link==False: link=abrir_url(url)
    else: pass
    if name!=False:
        albuns=re.compile('<a href=".+?"><img.+?src="(.+?)".+?border="0"></a.+?div class="grid_info"><a href=".+?" class="grid_artist">(.+?)</a><a href="(.+?)" class="grid_album">(.+?)</a></div>').findall(link)
    #else: albuns=re.compile('<a href="/(.+?)"><img src="(.+?)".+?"></a><p><a.+?class="artist">(.+?)</a><br /><a.+?class="album">(.+?)</a>').findall(link)
    for thumb,artist,end,albumname in albuns:
        addAlbum('[B]' + artist + '[/B]: ' + albumname,NoiseTradeURL + end,7,'http:' + thumb,1,True,'',albumname,artist,'')
    paginas(link)
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.setContent(int(sys.argv[1]), 'albuns')

############ OPTIMUS DISCOS #################

def optimusdiscos_menu():
    link=abrir_url(OptimusDiscosURL + OptimusAlbumlistURL)
    albuns=re.compile('{"is_downloadable".+?"album_id":"(.+?)".+?"artwork":"(.+?)".+?"description":"(.+?)".+?"album":"(.+?)".+?"artist":"(.+?)".+?"year":"(.+?)"').findall(link)
    for albumid,thumb,desc,albumname,artist,year in albuns:
        addAlbum('[B]' + artist + ' - ' + albumname + '[/B] (' + year + ')',albumid,7,thumb,1,True,desc,albumname,artist,year)
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.setContent(int(sys.argv[1]), 'albuns')

def generos(name,url):
    if name=='Novidades':
        extend='?s=newest'
    else: extend=''
    addDir('[COLOR yellow][B]'+traducao(40007)+'[/B][/COLOR]',NoiseTradeURL + 'searchall' + extend,3,'',1,True)
    link=abrir_url(url)
    link=clean(link)
    todosgeneros=re.compile('<ul class="root">(.+?)</ul>').findall(link)[0]
    generosseparados=re.compile('<a href="/(.+?)" >(.+?)</a>').findall(todosgeneros)
    for end,titulo in generosseparados:
        addDir('[B]'+titulo+'[/B]','http:/' + end + extend,3,'',1,True)
    
def lista_faixas(name,url):
    GA("None",name)
    if re.search('http://www.noisetrade.com',url):
        link=abrir_url(url)
        cover=re.compile('<meta property="og:image" content="(.+?)"/>').findall(link)[0]
        addLink('[COLOR white]' + name + '[/COLOR]',url,cover)
        tracks=re.compile('<Track Number="(.+?)" Name="(.+?).mp3" MP3="(.+?)".+?/>').findall(link)
        if not tracks:tracks=re.compile('<Track Number="(.+?)" Name="(.+?)" MP3="(.+?)".+?/>').findall(link)
        if len(tracks)!=1: addDir('[COLOR yellow][B]'+traducao(40008)+'[/B][/COLOR]',url,4,cover,1,False)
        addLink("",'',cover)
        for tracknum,trackname,trackend in tracks:
            numeroref=int(tracknum)+ 1
            if len(tracks)!=1: numerostracks='#' + str(numeroref) + ' - '
            else:  numerostracks=''
            addDir(numerostracks + trackname,trackend + '-----'+url+'-----',8,cover,1,False)
    else:
        link=abrir_url(OptimusDiscosURL + OptimusTracklistURL)
        cover=re.compile('{"is_downloadable".+?"album_id":"'+url+'".+?"artwork":"(.+?)".+?"downloadurl":"(.+?)"').findall(link)[0]
        addLink('[COLOR white]' + name + '[/COLOR]',url,cover[0])
        numeroref=int(0)
        tracks=re.compile('"album_id":"' + url + '".+?"track":"(.+?)".+?"name":"(.+?)"').findall(link)
        if len(tracks)!=1: addDir('[COLOR yellow][B]Reproduzir Todas[/B][/COLOR]',url,4,cover[0],1,False)
        addDir('[COLOR yellow][B]Download de Album[/B][/COLOR]',cover[1],18,cover[0],1,False)
        addLink("",'',cover[0])
        for downloadurl,trackname in tracks:
            numeroref=int(numeroref + 1)
            if len(tracks)!=1: numerostracks='#' + str(numeroref) + ' - '
            else:  numerostracks=''
            addDir(numerostracks + trackname,downloadurl + '-----'+url+'-----',8,cover[0],1,False)

        

def reproduzirtodas(name,url):
    dp = xbmcgui.DialogProgress()
    dp.create("Fightnight Music",traducao(40009))
    dp.update(0)
    playlist = xbmc.PlayList(1)
    playlist.clear()
    if re.search('http://www.noisetrade.com',url):
        mp3serverlink=abrir_url('http://www.noisetrade.com/Scripts/site.playlist.js')
        mp3server='http:' + re.compile('mp3: "(.+?)"').findall(mp3serverlink)[0]
        link=abrir_url(url)
        cover=re.compile('<meta property="og:image" content="(.+?)"/>').findall(link)[0]
        artist=re.compile('<h1 class="artist"><a href=".+?">(.+?)</a></h1>').findall(link)[0]
        album=re.compile('<h2 class="album">(.+?)</h2>').findall(link)[0]
        tracks=re.compile('<Track Number="(.+?)" Name="(.+?).mp3" MP3="(.+?)".+?/>').findall(link)
        if not tracks:tracks=re.compile('<Track Number="(.+?)" Name="(.+?)" MP3="(.+?)".+?/>').findall(link)
        for tracknum,trackname,trackend in tracks:
            numeroref=int(tracknum)+ 1
            if len(tracks)!=1: numerostracks='#' + str(numeroref) + ' - '
            else:  numerostracks=''
            liz=xbmcgui.ListItem(numerostracks + trackname, iconImage="DefaultVideo.png", thumbnailImage=cover)
            liz.setInfo('music', {'Title':numerostracks + trackname,'Album':album,'Artist':artist})
            liz.setProperty('mimetype', 'audio/mpeg')                
            playlist.add(mp3server + trackend, liz)
            progress = len(playlist) / float(len(tracks)) * 100               
            dp.update(int(progress), traducao(40010))
            if dp.iscanceled(): return
    else:
        link=abrir_url(OptimusDiscosURL + OptimusTracklistURL)
        numeroref=int(0)
        albuminfo=re.compile('{"is_downloadable".+?"album_id":"'+url+'".+?"artwork":"(.+?)".+?"album":"(.+?)".+?"artist":"(.+?)".+?"year":"(.+?)"').findall(link)[0]
        tracks=re.compile('"album_id":"' + url + '".+?"track":"(.+?)".+?"name":"(.+?)"').findall(link)
        for downloadurl,trackname in tracks:
            numeroref=int(numeroref + 1)
            if len(tracks)!=1: numerostracks='#' + str(numeroref) + ' - '
            else:  numerostracks=''
            liz=xbmcgui.ListItem(numerostracks + trackname, iconImage="DefaultVideo.png", thumbnailImage=albuminfo[0])
	    liz.setInfo('music', {'Title':numerostracks + trackname,'Album':albuminfo[1],'Artist':albuminfo[2],'Year':int(albuminfo[3])})
	    liz.setProperty('mimetype', 'audio/mpeg')                
	    playlist.add(downloadurl, liz)
	    progress = len(playlist) / float(len(tracks)) * 100               
	    dp.update(int(progress), 'A adicionar à playlist.')
	    if dp.iscanceled(): return

        
    dp.close()
    GA("None",name)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist)


def playmusic(name,url):
    print name
    print url
    playlist = xbmc.PlayList(1)
    playlist.clear()
    GA("None",name)
    url=re.compile('(.+?)-----(.+?)-----').findall(url)[0]
    if re.search('http://www.noisetrade.com',url[1]):
            
        ##mp3 server info##      
        mp3serverlink=abrir_url('http://www.noisetrade.com/Scripts/site.playlist.js')
        mp3server='http:' + re.compile('mp3: "(.+?)"').findall(mp3serverlink)[0]
        ##track info##
        
        link=abrir_url(url[1])
        cover=re.compile('<meta property="og:image" content="(.+?)"/>').findall(link)[0]
        artist=re.compile('<h1 class="artist"><a href=".+?">(.+?)</a></h1>').findall(link)[0]
        album=re.compile('<h2 class="album">(.+?)</h2>').findall(link)[0]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=cover)
        liz.setInfo('music', {'Title':name,'Album':album,'Artist':artist})
        liz.setProperty('mimetype', 'audio/mpeg')                
        playlist.add(mp3server+url[0], liz)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    else:
        ##### VER!!! CODIGO REPETIDO DESNECESSARIAMENTE #####
        link=abrir_url(OptimusDiscosURL + OptimusTracklistURL)
        albuminfo=re.compile('{"is_downloadable".+?"album_id":"'+url[1]+'".+?"artwork":"(.+?)".+?"album":"(.+?)".+?"artist":"(.+?)".+?"year":"(.+?)"').findall(link)[0]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=albuminfo[0])
        liz.setInfo('music', {'Title':name,'Album':albuminfo[1],'Artist':albuminfo[2],'Year':int(albuminfo[3])})
        liz.setProperty('mimetype', 'audio/mpeg')                
        playlist.add(url[0], liz)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

        

def pesquisa():
    keyb = xbmc.Keyboard('', 'Fightnight Music - '+traducao(40003))
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        encode=urllib.quote_plus(search)
        if encode=='': pass
        else: apanharalbuns(False,NoiseTradeURL + 'search?q=' + encode,False)

def paginas(link):
    try:
        pagina=re.compile('<a class="paged paged_on">.+?</a><a href="/(.+?)" class="paged">(.+?)</a>').findall(link)[0]
        addDir('[COLOR blue]' + traducao(40011) + pagina[1] + ' >>>[/COLOR]',NoiseTradeURL + pagina[0],3,'',1,True)
    except: pass

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
    ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addAlbum(name,url,mode,iconimage,total,pasta,desc,albumname,artist,year):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Audio", infoLabels={ "Title": name, "Artist": artist } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def abrir_url(url):
    print "A fazer request de: " + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def versao_disponivel():
    link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.audio.fightnightmusic/addon.xml')
    match=re.compile('name="Fightnight Music"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
    return match

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
    command={'\r':'','\n':'','\t':'','&nbsp;':'','&#231;':'ç','&#201;':'É','&#233;':'é','&#250;':'ú','&#227;':'ã','&#237;':'í','&#243;':'ó','&#193;':'Á','&#205;':'Í','&#244;':'ô','&#224;':'à','&#225;':'á','&#234;':'ê','&#211;':'Ó','&#226;':'â'}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def parseDate(dateString):
    try: return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except: return datetime.datetime.today() - datetime.timedelta(days = 1) #force update

def checkGA():
    secsInHour = 60 * 60
    threshold  = 2 * secsInHour
    now   = datetime.datetime.today()
    prev  = parseDate(selfAddon.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds
    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return
    selfAddon.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    

def downloadzip(name,url):
      if downloadPath=='':
            ok = mensagemok('Fightnight Music','Escolhes uma pasta para fazer download.')
            selfAddon.openSettings()
      else:
            lib=os.path.join(downloadPath, 'album-optimus.zip')
            downloader(url,lib)
            pasta = xbmc.translatePath(os.path.join(downloadPath,''))
            xbmc.sleep(1000)
            dp = xbmcgui.DialogProgress()
            dp.create("Fightnight Music", "A extrair")
            import extract
            extract.all(lib,pasta,dp)
            os.remove(lib)

def downloader(url,dest, useReq = False):
    dp = xbmcgui.DialogProgress()
    dp.create("Fightnight Music","A fazer download...",'')

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


def openfile(filename):
    try:
        
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None
                    
def send_request_to_google_analytics(utm_url):
    try:
        req = urllib2.Request(utm_url, None,{'User-Agent':user_agent})
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = selfAddon.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + versao + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + versao + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + versao + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + versao + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
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
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+versao+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = selfAddon.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + versao + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
checkGA()

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
elif mode==1: novosenotaveis(name,url)
elif mode==2: ok = mensagemok('Fightnight Music',traducao(40012),traducao(40013),traducao(40014))
elif mode==3: apanharalbuns(name,url,False)
elif mode==4: reproduzirtodas(name,url)
elif mode==5: pesquisa()
elif mode==6: generos(name,url)
elif mode==7: lista_faixas(name,url)
elif mode==8: playmusic(name,url)
elif mode==9: noisetrade_menu()
elif mode==10: optimusdiscos_menu()
elif mode==11: radio()
elif mode==12: radio_concelhos(name,url)
elif mode==13: tipo_radio(name,url)
elif mode==14: listar_radios(name,url)
elif mode==15: obterurlstream(name,url)
elif mode==16: pesquisa_radio(name,url)
elif mode==17: radiosnacionais(name,url)
elif mode==18: downloadzip(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
